"""Fetch a dated, non-adjusted Yahoo Finance snapshot for IDX ticker candidates.

The downloaded Yahoo data is intended for personal research and education.  By
default this script writes under ``private/`` so a bulk vendor snapshot is not
accidentally published.  The public repository can retain this retrieval code,
the source/coverage manifest, and the executed notebook's small derived tables.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import yfinance as yf


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_UNIVERSE = (
    ROOT
    / "products/stocks/data/processed"
    / "ksei_registered_share_securities_2026-09-22.csv"
)
YAHOO_NOTICE = "https://github.com/ranaroussi/yfinance#legal-stuff"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def latest_rows(download: pd.DataFrame, symbols: list[str]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for symbol in symbols:
        try:
            frame = download.xs(symbol, axis=1, level="Ticker").dropna(
                subset=["Close"], how="all"
            )
        except (KeyError, TypeError):
            frame = pd.DataFrame()
        if frame.empty:
            rows.append({"yahoo_symbol": symbol, "price_status": "missing"})
            continue
        last = frame.iloc[-1]
        rows.append(
            {
                "yahoo_symbol": symbol,
                "price_status": "available",
                "price_date": frame.index[-1].date().isoformat(),
                "open_idr": last.get("Open"),
                "high_idr": last.get("High"),
                "low_idr": last.get("Low"),
                "close_idr": last.get("Close"),
                "adj_close_idr": last.get("Adj Close"),
                "volume_shares": last.get("Volume"),
            }
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--as-of", required=True, help="Snapshot label in YYYY-MM-DD format")
    parser.add_argument("--universe", type=Path, default=DEFAULT_UNIVERSE)
    parser.add_argument("--batch-size", type=int, default=80)
    parser.add_argument("--period", default="10d")
    parser.add_argument("--pause", type=float, default=1.0)
    args = parser.parse_args()
    datetime.strptime(args.as_of, "%Y-%m-%d")

    universe = pd.read_csv(args.universe)
    candidate_mask = universe["ticker"].astype(str).str.fullmatch(r"[A-Z]{4}")
    tickers = universe.loc[candidate_mask, "ticker"].drop_duplicates().tolist()
    symbols = [f"{ticker}.JK" for ticker in tickers]
    retrieved_at = datetime.now(timezone.utc).isoformat()

    output_dir = ROOT / "private" / "market_data" / "yahoo"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"idx_latest_prices_{args.as_of}.csv"
    manifest_path = output_dir / f"idx_latest_prices_{args.as_of}.json"

    records: list[dict[str, object]] = []
    batch_count = math.ceil(len(symbols) / args.batch_size)
    for batch_number, start in enumerate(range(0, len(symbols), args.batch_size), start=1):
        batch = symbols[start : start + args.batch_size]
        try:
            downloaded = yf.download(
                batch,
                period=args.period,
                interval="1d",
                auto_adjust=False,
                actions=False,
                repair=False,
                progress=False,
                threads=True,
                group_by="column",
                timeout=30,
            )
            records.extend(latest_rows(downloaded, batch))
        except Exception as exc:
            records.extend(
                {
                    "yahoo_symbol": symbol,
                    "price_status": "batch_error",
                    "error": f"{type(exc).__name__}: {exc}",
                }
                for symbol in batch
            )
        print(f"price batch {batch_number}/{batch_count}", flush=True)
        if batch_number < batch_count:
            time.sleep(args.pause)

    prices = pd.DataFrame(records)
    prices.insert(0, "ticker", prices["yahoo_symbol"].str.removesuffix(".JK"))
    prices.insert(2, "retrieved_at_utc", retrieved_at)
    prices = prices.sort_values("ticker").reset_index(drop=True)
    prices.to_csv(output_path, index=False)

    status_counts = prices["price_status"].value_counts(dropna=False).to_dict()
    manifest = {
        "snapshot_date": args.as_of,
        "retrieved_at_utc": retrieved_at,
        "provider": "Yahoo Finance via yfinance",
        "provider_notice": YAHOO_NOTICE,
        "source_ticker_pattern": "{KSEI four-letter code}.JK",
        "source_universe_file": str(args.universe.resolve()),
        "requested_ticker_count": len(symbols),
        "status_counts": status_counts,
        "period": args.period,
        "interval": "1d",
        "auto_adjust": False,
        "actions": False,
        "repair": False,
        "currency_expected": "IDR",
        "exchange_timezone_expected": "Asia/Jakarta",
        "output_file": str(output_path.relative_to(ROOT)),
        "output_sha256": sha256_file(output_path),
        "license": (
            "yfinance is open-source software, but Yahoo data rights are separate. "
            "Keep this bulk snapshot private and consult Yahoo terms."
        ),
        "limitations": [
            "Latest available daily bar is not guaranteed to be real-time.",
            "A missing Yahoo symbol does not prove that a KSEI security is unlisted.",
            "Prices are unadjusted; market-cap calculations require a separately sourced "
            "issued-share count for the matching share class and effective date.",
        ],
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output_path), **status_counts}, indent=2))


if __name__ == "__main__":
    main()
