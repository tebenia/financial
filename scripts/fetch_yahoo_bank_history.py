"""Fetch adjusted daily history for the metadata-covered Indonesian bank universe.

The retrieved Yahoo data are written under the Git-ignored ``private/`` tree.
The open-source yfinance client and the retrieved data have separate terms.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd
import yfinance as yf


ROOT = Path(__file__).resolve().parents[1]


# Objective: normalize yfinance's multi-ticker wide output into one tidy row per ticker-date.
def to_tidy(history: pd.DataFrame, symbols: list[str]) -> pd.DataFrame:
    rows: list[pd.DataFrame] = []
    for symbol in symbols:
        if isinstance(history.columns, pd.MultiIndex):
            if symbol not in history.columns.get_level_values(1):
                continue
            frame = history.xs(symbol, axis=1, level=1, drop_level=True).copy()
        else:
            frame = history.copy()
        frame = frame.rename_axis("date").reset_index()
        frame.columns = [str(column).lower().replace(" ", "_") for column in frame.columns]
        frame["yahoo_symbol"] = symbol
        frame["ticker"] = symbol.removesuffix(".JK")
        wanted = [
            "date",
            "ticker",
            "yahoo_symbol",
            "open",
            "high",
            "low",
            "close",
            "adj_close",
            "volume",
        ]
        for column in wanted:
            if column not in frame:
                frame[column] = pd.NA
        frame = frame[wanted].dropna(subset=["adj_close"])
        rows.append(frame)
    if not rows:
        raise RuntimeError("Yahoo returned no usable adjusted-price rows")
    return pd.concat(rows, ignore_index=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--as-of", required=True, help="Metadata snapshot date YYYY-MM-DD")
    parser.add_argument("--years", type=int, default=10)
    args = parser.parse_args()
    as_of = datetime.strptime(args.as_of, "%Y-%m-%d").date()

    cache_dir = ROOT / "private/market_data/yahoo"
    metadata_path = cache_dir / f"idx_company_metadata_{args.as_of}.csv"
    metadata = pd.read_csv(metadata_path)
    banks = metadata.loc[
        metadata["metadata_status"].eq("available")
        & metadata["industry"].eq("Banks - Regional")
    ].copy()
    symbols = sorted(banks["yahoo_symbol"].dropna().unique().tolist())
    requested_symbols = symbols + ["^JKSE"]

    start = as_of.replace(year=as_of.year - args.years)
    end_exclusive = as_of + timedelta(days=1)
    history = yf.download(
        requested_symbols,
        start=start.isoformat(),
        end=end_exclusive.isoformat(),
        auto_adjust=False,
        actions=False,
        repair=False,
        group_by="column",
        threads=True,
        progress=False,
    )
    tidy = to_tidy(history, requested_symbols)
    output_path = cache_dir / f"idx_bank_adjusted_history_{args.as_of}.csv"
    tidy.to_csv(output_path, index=False)

    counts = tidy.groupby("ticker").agg(
        first_date=("date", "min"),
        last_date=("date", "max"),
        observations=("date", "size"),
    ).reset_index()
    counts["first_date"] = counts["first_date"].astype(str)
    counts["last_date"] = counts["last_date"].astype(str)
    missing = sorted(set(symbols) - set(tidy["yahoo_symbol"].unique()))
    manifest = {
        "snapshot_date": args.as_of,
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "provider": "Yahoo Finance via yfinance",
        "industry_filter": "Yahoo industry == Banks - Regional",
        "requested_bank_count": len(symbols),
        "requested_symbols": requested_symbols,
        "returned_ticker_count_including_benchmark": int(tidy["ticker"].nunique()),
        "missing_bank_symbols": missing,
        "start_date": start.isoformat(),
        "end_date_inclusive": args.as_of,
        "benchmark": "^JKSE",
        "price_field_for_total_return": "adj_close",
        "output_file": str(output_path.relative_to(ROOT)),
        "coverage": counts.to_dict("records"),
        "license": (
            "yfinance is Apache-licensed software; Yahoo data rights are separate. "
            "This historical snapshot remains under the Git-ignored private directory."
        ),
        "limitations": [
            "The current Yahoo industry membership creates survivorship bias.",
            "Yahoo adjusted prices are not an official IDX total-return series.",
            "Thin trading and stale prices can understate measured volatility.",
            "Recently listed banks do not have a comparable full history.",
        ],
    }
    manifest_path = cache_dir / f"idx_bank_adjusted_history_{args.as_of}.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "bank_symbols_requested": len(symbols),
        "tickers_returned_including_benchmark": int(tidy["ticker"].nunique()),
        "rows": len(tidy),
        "missing": missing,
        "output": str(output_path),
    }, indent=2))


if __name__ == "__main__":
    main()
