"""Fetch and normalize Indonesia's registered-share universe from KSEI.

KSEI is an official Indonesian capital-market institution. Its public registry
lists share securities and provides one detail page per security. The detail
page is needed to distinguish active ordinary shares on IDX from preferred,
special-class, inactive, or non-IDX registrations.

This script preserves:
* the raw registry HTML;
* parsed detail records with a SHA-256 hash of every source response;
* the complete registered-share CSV;
* the filtered active ordinary IDX universe CSV; and
* a provenance and validation manifest.

It deliberately does not invent IDX-IC classifications. KSEI's ``Activity
Sector`` is retained as ``ksei_activity_sector`` and must not be confused with
the current IDX-IC sector/subsector hierarchy.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
from io import StringIO
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import requests
from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = ROOT / "products" / "stocks" / "data"
REGISTRY_URL = "https://web.ksei.co.id/services/registered-securities/shares?setLocale=en-US"
DETAIL_URL = "https://web.ksei.co.id/services/registered-securities/shares/lc/{code}"
USER_AGENT = "financial-learning-research/1.0 (+public KSEI registry; noncommercial education)"


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def normalized_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def request_bytes(url: str, timeout: int, attempts: int = 4) -> bytes:
    last_error: Exception | None = None
    headers = {"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml"}
    for attempt in range(attempts):
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            return response.content
        except requests.RequestException as exc:
            last_error = exc
            if attempt + 1 < attempts:
                time.sleep(1.5 * (2**attempt))
    raise RuntimeError(f"Failed after {attempts} attempts: {url}: {last_error}")


def parse_registry(html: bytes) -> pd.DataFrame:
    tables = pd.read_html(StringIO(html.decode("utf-8", errors="replace")))
    if len(tables) != 1:
        raise ValueError(f"Expected one KSEI registry table, found {len(tables)}")
    frame = tables[0].rename(
        columns={
            "No.": "registry_number",
            "Code": "ticker",
            "Description": "registry_name",
            "Registrars": "registrar",
            "Nominal": "registry_nominal",
        }
    )
    frame["ticker"] = frame["ticker"].astype(str).str.strip().str.upper()
    if frame["ticker"].duplicated().any():
        duplicates = frame.loc[frame["ticker"].duplicated(), "ticker"].tolist()
        raise ValueError(f"Duplicate KSEI codes: {duplicates[:10]}")
    return frame


def parse_detail(code: str, payload: bytes, retrieved_at: str) -> dict[str, Any]:
    soup = BeautifulSoup(payload, "html.parser")
    definition_list = soup.select_one("dl.deflist")
    if definition_list is None:
        raise ValueError(f"No detail definition list found for {code}")
    labels = definition_list.find_all("dt", recursive=False)
    values = definition_list.find_all("dd", recursive=False)
    fields = {
        normalized_text(label.get_text(" ", strip=True)).rstrip(":"): normalized_text(
            value.get_text(" ", strip=True)
        )
        for label, value in zip(labels, values, strict=False)
    }
    expected_code = fields.get("Short Code", "").upper()
    if expected_code and expected_code != code:
        raise ValueError(f"Detail code mismatch: requested {code}, received {expected_code}")
    return {
        "ticker": code,
        "security_name": fields.get("Security name"),
        "issuer": fields.get("Issuer"),
        "isin": fields.get("ISIN Code"),
        "security_type": fields.get("Type"),
        "listing_date_raw": fields.get("Listing Date"),
        "stock_exchange": fields.get("Stock Exchange"),
        "status": fields.get("Status"),
        "nominal_raw": fields.get("Nominal"),
        "current_amount_raw": fields.get("Current Amount"),
        "currency": fields.get("Currency"),
        "form": fields.get("Form"),
        "effective_date_isin_raw": fields.get("Effective Date ISIN"),
        "ksei_activity_sector": fields.get("Activity Sector"),
        "number_of_securities_raw": fields.get("Number of Securities"),
        "detail_url": DETAIL_URL.format(code=code),
        "detail_retrieved_at_utc": retrieved_at,
        "detail_content_sha256": sha256_bytes(payload),
    }


def fetch_detail(code: str, timeout: int, retrieved_at: str) -> dict[str, Any]:
    payload = request_bytes(DETAIL_URL.format(code=code), timeout=timeout)
    return parse_detail(code, payload, retrieved_at)


def ordinary_share_mask(series: pd.Series) -> pd.Series:
    normalized = series.fillna("").str.casefold()
    return normalized.isin({"saham biasa", "common stock", "ordinary shares", "ordinary share"})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--as-of", required=True, help="Snapshot label in YYYY-MM-DD format")
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument(
        "--registry-only",
        action="store_true",
        help="Create the complete KSEI registry snapshot without crawling 984 detail pages",
    )
    parser.add_argument("--idx-reference-count", type=int)
    parser.add_argument("--idx-reference-period")
    parser.add_argument("--idx-reference-url")
    parser.add_argument(
        "--reuse-existing-raw",
        action="store_true",
        help="Parse an existing dated raw registry snapshot without downloading it again",
    )
    parser.add_argument(
        "--resume-details",
        action="store_true",
        help="Reuse successfully parsed details from the dated JSON and fetch only missing codes",
    )
    args = parser.parse_args()

    datetime.strptime(args.as_of, "%Y-%m-%d")
    retrieved_at = datetime.now(timezone.utc).isoformat()
    raw_dir = DATA_ROOT / "raw"
    processed_dir = DATA_ROOT / "processed"
    manifest_dir = DATA_ROOT / "manifests"
    for directory in (raw_dir, processed_dir, manifest_dir):
        directory.mkdir(parents=True, exist_ok=True)

    registry_path = raw_dir / f"ksei_registered_shares_{args.as_of}.html"
    if args.reuse_existing_raw:
        if not registry_path.exists():
            raise FileNotFoundError(f"Raw registry snapshot does not exist: {registry_path}")
        registry_html = registry_path.read_bytes()
    else:
        registry_html = request_bytes(REGISTRY_URL, timeout=args.timeout)
        registry_path.write_bytes(registry_html)
    registry = parse_registry(registry_html)

    if args.registry_only:
        registry.insert(0, "snapshot_date", args.as_of)
        registry.insert(1, "source_url", REGISTRY_URL)
        registry.insert(2, "retrieved_at_utc", retrieved_at)
        registry["detail_url"] = registry["ticker"].map(
            lambda code: DETAIL_URL.format(code=code)
        )
        registry["has_standard_four_letter_ticker"] = registry["ticker"].str.fullmatch(
            r"[A-Z]{4}"
        )
        full_path = processed_dir / f"ksei_registered_share_securities_{args.as_of}.csv"
        registry.to_csv(full_path, index=False)
        manifest = {
            "snapshot_date": args.as_of,
            "retrieved_at_utc": retrieved_at,
            "source_name": "KSEI Registered Securities - Shares",
            "source_url": REGISTRY_URL,
            "source_authority": "PT Kustodian Sentral Efek Indonesia (KSEI)",
            "raw_registry_file": str(registry_path.relative_to(ROOT)),
            "raw_registry_sha256": sha256_bytes(registry_html),
            "complete_registry_csv": str(full_path.relative_to(ROOT)),
            "registered_security_count": int(len(registry)),
            "standard_four_letter_ticker_count": int(
                registry["has_standard_four_letter_ticker"].sum()
            ),
            "detail_enrichment_status": "not_attempted_registry_only",
            "idx_listed_company_reference_count": args.idx_reference_count,
            "idx_listed_company_reference_period": args.idx_reference_period,
            "idx_listed_company_reference_url": args.idx_reference_url,
            "units": "one row per KSEI registered share security code",
            "currency": "nominal values are IDR on the source table",
            "timezone": "source page does not state a timezone; retrieval timestamp is UTC",
            "revision_or_vintage": args.as_of,
            "license": "No reusable-data license identified on the source page; retained for research provenance",
            "scope_warning": (
                "KSEI registered share securities are not identical to IDX listed companies. "
                "The registry may include special classes, preferred shares, and securities "
                "whose current exchange/status must be checked on their KSEI detail pages."
            ),
        }
        manifest_path = manifest_dir / f"ksei_stock_universe_{args.as_of}.json"
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(
            json.dumps(
                {
                    "registered": len(registry),
                    "standard_four_letter_tickers": int(
                        registry["has_standard_four_letter_ticker"].sum()
                    ),
                    "manifest": str(manifest_path.relative_to(ROOT)),
                },
                indent=2,
            )
        )
        return

    details_path = raw_dir / f"ksei_share_details_{args.as_of}.json"
    details: list[dict[str, Any]] = []
    if args.resume_details and details_path.exists():
        loaded = json.loads(details_path.read_text(encoding="utf-8"))
        if not isinstance(loaded, list):
            raise ValueError(f"Expected a list in {details_path}")
        details = loaded
    completed_codes = {str(row["ticker"]) for row in details}
    remaining_codes = [code for code in registry["ticker"] if code not in completed_codes]
    errors: list[dict[str, str]] = []
    total = len(remaining_codes)
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(fetch_detail, code, args.timeout, retrieved_at): code
            for code in remaining_codes
        }
        for completed, future in enumerate(concurrent.futures.as_completed(futures), start=1):
            code = futures[future]
            try:
                details.append(future.result())
            except Exception as exc:  # retain all failures in the manifest
                errors.append({"ticker": code, "error": str(exc)})
            if completed % 25 == 0 or completed == total:
                details.sort(key=lambda row: row["ticker"])
                details_path.write_text(
                    json.dumps(details, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )
                print(
                    f"details {completed}/{total}; retained={len(details)}; errors={len(errors)}",
                    flush=True,
                )

    details.sort(key=lambda row: row["ticker"])
    details_path.write_text(
        json.dumps(details, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    detail_frame = pd.DataFrame(details)
    full = registry.merge(detail_frame, on="ticker", how="left", validate="one_to_one")
    full.insert(0, "snapshot_date", args.as_of)
    full.insert(1, "registry_source_url", REGISTRY_URL)
    full.insert(2, "registry_retrieved_at_utc", retrieved_at)
    full["is_active_idx_ordinary_share"] = (
        full["status"].fillna("").str.casefold().eq("active")
        & full["stock_exchange"].fillna("").str.upper().eq("IDX")
        & ordinary_share_mask(full["security_type"])
        & full["ticker"].str.fullmatch(r"[A-Z]{4}")
    )

    full_path = processed_dir / f"ksei_registered_share_securities_{args.as_of}.csv"
    full.to_csv(full_path, index=False)
    active = full.loc[full["is_active_idx_ordinary_share"]].copy()
    active_path = processed_dir / f"idx_active_ordinary_share_universe_{args.as_of}.csv"
    active.to_csv(active_path, index=False)

    type_counts = full["security_type"].fillna("<missing>").value_counts().to_dict()
    status_counts = full["status"].fillna("<missing>").value_counts().to_dict()
    exchange_counts = full["stock_exchange"].fillna("<missing>").value_counts().to_dict()
    manifest = {
        "snapshot_date": args.as_of,
        "retrieved_at_utc": retrieved_at,
        "source_name": "KSEI Registered Securities - Shares",
        "source_url": REGISTRY_URL,
        "source_authority": "PT Kustodian Sentral Efek Indonesia (KSEI)",
        "raw_registry_file": str(registry_path.relative_to(ROOT)),
        "raw_registry_sha256": sha256_bytes(registry_html),
        "parsed_detail_file": str(details_path.relative_to(ROOT)),
        "complete_registry_csv": str(full_path.relative_to(ROOT)),
        "active_idx_ordinary_share_csv": str(active_path.relative_to(ROOT)),
        "registered_security_count": int(len(full)),
        "detail_success_count": int(len(details)),
        "detail_error_count": int(len(errors)),
        "active_idx_ordinary_share_count": int(len(active)),
        "security_type_counts": type_counts,
        "status_counts": status_counts,
        "exchange_counts": exchange_counts,
        "errors": errors,
        "units": "one row per registered share security code",
        "currency": "IDR where supplied by KSEI",
        "timezone": "source page does not state a timezone; retrieval timestamp is UTC",
        "revision_or_vintage": args.as_of,
        "license": "No reusable-data license identified on the source page; retained for research provenance",
        "scope_warning": (
            "The complete KSEI registry is not identical to the count of IDX listed companies. "
            "The filtered universe requires Active status, IDX exchange, ordinary-share type, "
            "and a four-letter ticker. KSEI Activity Sector is not IDX-IC."
        ),
    }
    manifest_path = manifest_dir / f"ksei_stock_universe_{args.as_of}.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print(json.dumps({
        "registered": len(full),
        "details": len(details),
        "errors": len(errors),
        "active_idx_ordinary": len(active),
        "manifest": str(manifest_path.relative_to(ROOT)),
    }, indent=2))
    if errors:
        raise SystemExit("Detail fetch was incomplete; inspect manifest errors and rerun")


if __name__ == "__main__":
    main()
