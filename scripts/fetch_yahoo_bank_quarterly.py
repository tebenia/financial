"""Fetch quarterly fundamentals and recent prices for large Indonesian banks.

Raw provider data are intentionally written below the Git-ignored ``private/``
tree. Yahoo is useful for a reproducible comparison layer, but it is not the
authoritative filing source; the generated manifest records this limitation.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd
import yfinance as yf


ROOT = Path(__file__).resolve().parents[1]


# Objective: convert a Yahoo statement matrix into a tidy period-metric table.
def tidy_statement(statement: pd.DataFrame, ticker: str, statement_type: str) -> pd.DataFrame:
    if statement.empty:
        return pd.DataFrame(columns=["ticker", "statement", "period_end", "metric", "value"])
    records: list[dict] = []
    for period in statement.columns:
        for metric, value in statement[period].items():
            if pd.notna(value):
                records.append({
                    "ticker": ticker,
                    "statement": statement_type,
                    "period_end": pd.Timestamp(period).date().isoformat(),
                    "metric": str(metric),
                    "value": value,
                })
    return pd.DataFrame.from_records(records).sort_values(["period_end", "metric"])


# Objective: normalize multi-ticker Yahoo prices into one row per ticker-date.
def tidy_prices(history: pd.DataFrame, symbols: list[str]) -> pd.DataFrame:
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
        frame["ticker"] = symbol.removesuffix(".JK")
        keep = ["date", "ticker", "open", "high", "low", "close", "adj_close", "volume"]
        for column in keep:
            if column not in frame:
                frame[column] = pd.NA
        rows.append(frame[keep].dropna(subset=["adj_close"]))
    return pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--as-of", required=True, help="Retrieval date YYYY-MM-DD")
    parser.add_argument("--metadata-date", default="2026-09-22")
    parser.add_argument("--top", type=int, default=15)
    args = parser.parse_args()

    as_of = datetime.strptime(args.as_of, "%Y-%m-%d").date()
    cache = ROOT / "private/market_data/yahoo"
    metadata_path = cache / f"idx_company_metadata_{args.metadata_date}.csv"
    metadata = pd.read_csv(metadata_path)
    banks = (
        metadata.loc[
            metadata["metadata_status"].eq("available")
            & metadata["industry"].eq("Banks - Regional")
        ]
        .sort_values("marketCap", ascending=False)
        .head(args.top)
        .copy()
    )
    symbols = banks["yahoo_symbol"].tolist()

    statements: list[pd.DataFrame] = []
    coverage: list[dict] = []
    errors: dict[str, str] = {}
    for row in banks.itertuples(index=False):
        ticker = row.ticker
        try:
            security = yf.Ticker(row.yahoo_symbol)
            income = security.quarterly_income_stmt
            balance = security.quarterly_balance_sheet
            statements.extend([
                tidy_statement(income, ticker, "income_statement"),
                tidy_statement(balance, ticker, "balance_sheet"),
            ])
            periods = sorted(
                set(pd.to_datetime(income.columns).date.astype(str))
                | set(pd.to_datetime(balance.columns).date.astype(str))
            )
            coverage.append({
                "ticker": ticker,
                "long_name": row.longName,
                "market_cap_at_metadata_date": row.marketCap,
                "periods": periods,
                "income_metric_count": int(len(income.index)),
                "balance_metric_count": int(len(balance.index)),
            })
        except Exception as exc:  # provider failures must not erase other banks
            errors[ticker] = f"{type(exc).__name__}: {exc}"

    if not statements:
        raise RuntimeError(f"No statements returned; provider errors: {errors}")
    fundamentals = pd.concat(statements, ignore_index=True)
    fundamentals_path = cache / f"idx_bank_quarterly_fundamentals_{args.as_of}.csv"
    fundamentals.to_csv(fundamentals_path, index=False)

    prices_raw = yf.download(
        symbols + ["^JKSE"],
        start=(as_of - timedelta(days=3 * 366)).isoformat(),
        end=(as_of + timedelta(days=1)).isoformat(),
        auto_adjust=False,
        actions=False,
        repair=False,
        group_by="column",
        threads=True,
        progress=False,
    )
    prices = tidy_prices(prices_raw, symbols + ["^JKSE"])
    prices_path = cache / f"idx_large_bank_prices_{args.as_of}.csv"
    prices.to_csv(prices_path, index=False)

    manifest = {
        "as_of_date": args.as_of,
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "provider": "Yahoo Finance via yfinance",
        "selection": f"Top {args.top} Yahoo Banks - Regional issuers by marketCap in {args.metadata_date} snapshot",
        "metadata_source": str(metadata_path.relative_to(ROOT)),
        "symbols": symbols,
        "coverage": coverage,
        "errors": errors,
        "fundamentals_file": str(fundamentals_path.relative_to(ROOT)),
        "prices_file": str(prices_path.relative_to(ROOT)),
        "limitations": [
            "Yahoo is a secondary provider, not the authoritative issuer or IDX filing source.",
            "Yahoo exposes only a limited number of quarterly periods and field coverage differs by issuer.",
            "Bank-specific prudential ratios such as CASA, NIM, NPL, LAR, CAR, LDR, and cost of credit are not consistently available.",
            "Reported periods may be restated, differ in consolidation scope, or contain provider mapping errors.",
            "Market-cap selection uses a current snapshot and therefore creates survivorship and look-ahead bias for historical comparisons.",
        ],
    }
    manifest_path = cache / f"idx_bank_quarterly_fundamentals_{args.as_of}.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "banks_requested": len(symbols),
        "banks_with_statement_coverage": len(coverage),
        "statement_rows": len(fundamentals),
        "price_rows": len(prices),
        "errors": errors,
        "latest_price_date": str(pd.to_datetime(prices["date"]).max().date()),
    }, indent=2))


if __name__ == "__main__":
    main()
