"""Fetch Yahoo company metadata for price-covered IDX ticker candidates.

Writes to the Git-ignored private cache.  The client library is open source;
the retrieved Yahoo data has separate personal-use terms.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import yfinance as yf


ROOT = Path(__file__).resolve().parents[1]
FIELDS = [
    "symbol",
    "shortName",
    "longName",
    "sector",
    "industry",
    "marketCap",
    "sharesOutstanding",
    "impliedSharesOutstanding",
    "floatShares",
    "regularMarketPrice",
    "previousClose",
    "currency",
    "exchange",
    "fullExchangeName",
    "quoteType",
    "firstTradeDateEpochUtc",
]


def fetch_one(symbol: str, attempts: int = 3) -> dict[str, object]:
    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            info = yf.Ticker(symbol).get_info()
            row = {field: info.get(field) for field in FIELDS}
            row["yahoo_symbol"] = symbol
            row["metadata_status"] = "available" if info else "missing"
            return row
        except Exception as exc:
            last_error = exc
            if attempt + 1 < attempts:
                time.sleep(1.5 * (attempt + 1))
    return {
        "yahoo_symbol": symbol,
        "metadata_status": "error",
        "error": f"{type(last_error).__name__}: {last_error}",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--as-of", required=True)
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    datetime.strptime(args.as_of, "%Y-%m-%d")

    cache_dir = ROOT / "private/market_data/yahoo"
    prices_path = cache_dir / f"idx_latest_prices_{args.as_of}.csv"
    output_path = cache_dir / f"idx_company_metadata_{args.as_of}.csv"
    manifest_path = cache_dir / f"idx_company_metadata_{args.as_of}.json"
    prices = pd.read_csv(prices_path)
    requested = prices.loc[prices["price_status"].eq("available"), "yahoo_symbol"].tolist()

    rows: list[dict[str, object]] = []
    if args.resume and output_path.exists():
        prior = pd.read_csv(output_path)
        prior = prior.loc[prior["metadata_status"].eq("available")].copy()
        rows = prior.where(pd.notna(prior), None).to_dict("records")
    completed = {
        str(row["yahoo_symbol"])
        for row in rows
        if row.get("metadata_status") == "available"
    }
    remaining = [symbol for symbol in requested if symbol not in completed]
    retrieved_at = datetime.now(timezone.utc).isoformat()

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(fetch_one, symbol): symbol for symbol in remaining}
        for count, future in enumerate(concurrent.futures.as_completed(futures), start=1):
            rows.append(future.result())
            if count % 25 == 0 or count == len(remaining):
                frame = pd.DataFrame(rows)
                frame["ticker"] = frame["yahoo_symbol"].str.removesuffix(".JK")
                frame["retrieved_at_utc"] = retrieved_at
                frame.sort_values("ticker").to_csv(output_path, index=False)
                print(
                    f"metadata {count}/{len(remaining)}; retained={len(frame)}",
                    flush=True,
                )

    frame = pd.read_csv(output_path)
    manifest = {
        "snapshot_date": args.as_of,
        "retrieved_at_utc": retrieved_at,
        "provider": "Yahoo Finance via yfinance",
        "requested_count": len(requested),
        "status_counts": frame["metadata_status"].value_counts(dropna=False).to_dict(),
        "fields": FIELDS,
        "output_file": str(output_path.relative_to(ROOT)),
        "license": (
            "yfinance is Apache-licensed software; Yahoo data rights are separate. "
            "This bulk metadata snapshot remains under the Git-ignored private directory."
        ),
        "limitations": [
            "Yahoo sector and industry are not IDX-IC classifications.",
            "Market capitalization and share counts are provider metadata and require validation.",
            "Different fields can have different effective timestamps.",
        ],
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest["status_counts"], indent=2))


if __name__ == "__main__":
    main()
