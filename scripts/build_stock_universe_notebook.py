"""Build the Indonesia stock-universe notebook from dated source snapshots."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "products/stocks/05_indonesia_stock_universe.ipynb"


def md(text: str) -> dict:
    return {
        "cell_type": "markdown",
        "id": hashlib.sha1(("markdown\0" + text).encode()).hexdigest()[:12],
        "metadata": {},
        "source": text.splitlines(keepends=True),
    }


def code(text: str) -> dict:
    return {
        "cell_type": "code",
        "id": hashlib.sha1(("code\0" + text).encode()).hexdigest()[:12],
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": text.splitlines(keepends=True),
    }


cells = [
    md(
        """# Indonesia Stock Universe — official registry plus market snapshot

> **Educational research universe—not a buy list.** This notebook separates an official KSEI security registry from a Yahoo Finance daily-price snapshot. Registration, price availability, size, or sector membership does not establish suitability, liquidity, or current tradability.

The table is point-in-time: KSEI fields and Yahoo prices have explicit retrieval dates. Yahoo's latest daily bar can be delayed, stale, or missing. Bulk Yahoo downloads remain under the Git-ignored `private/` directory because free access is not an open-data redistribution licence."""
    ),
    code(
        """from pathlib import Path
import json
import re
import pandas as pd

pd.set_option('display.max_columns', 40)
pd.set_option('display.float_format', lambda value: f'{value:,.2f}')

# Objective: locate the same artifact from either the repository root or notebook directory.
def locate(relative_path, private=False):
    candidates = [Path(relative_path), Path('products/stocks') / relative_path]
    if private:
        candidates.extend([
            Path('../../private') / relative_path,
            Path('private') / relative_path,
        ])
    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()
    raise FileNotFoundError(f'Could not locate {relative_path}; tried {candidates}')

master_path = locate('data/processed/ksei_registered_share_securities_2026-09-22.csv')
manifest_path = locate('data/manifests/ksei_stock_universe_2026-09-22.json')
price_path = locate('market_data/yahoo/idx_latest_prices_2026-09-22.csv', private=True)
price_manifest_path = locate('market_data/yahoo/idx_latest_prices_2026-09-22.json', private=True)
metadata_path = locate('market_data/yahoo/idx_company_metadata_2026-09-22.csv', private=True)
metadata_manifest_path = locate('market_data/yahoo/idx_company_metadata_2026-09-22.json', private=True)

registered = pd.read_csv(master_path)
ksei_manifest = json.loads(manifest_path.read_text())
prices = pd.read_csv(price_path)
price_manifest = json.loads(price_manifest_path.read_text())
company_metadata = pd.read_csv(metadata_path)
metadata_manifest = json.loads(metadata_manifest_path.read_text())
len(registered), len(prices), len(company_metadata)"""
    ),
    md(
        """## Coverage and scope

KSEI registered share securities are broader than active ordinary shares listed on IDX. Because KSEI's detail endpoint was throttled during this refresh, the **current market-data layer** means four-letter KSEI candidates for which Yahoo returned a recent daily price. That is a transparent operational definition, not an official listed-company count. A missing Yahoo row is retained as missing and never converted to a zero price."""
    ),
    code(
        """summary = pd.Series({
    'KSEI registered share securities': len(registered),
    'standard four-letter ticker candidates': int(registered['ticker'].astype(str).str.fullmatch(r'[A-Z]{4}').sum()),
    'Yahoo price candidates requested': price_manifest['requested_ticker_count'],
    'Yahoo daily prices available': int((prices['price_status'] == 'available').sum()),
    'Yahoo daily prices missing': int((prices['price_status'] != 'available').sum()),
    'Yahoo company metadata available': int((company_metadata['metadata_status'] == 'available').sum()),
    'Yahoo company metadata errors after retry': int((company_metadata['metadata_status'] != 'available').sum()),
    'KSEI snapshot date': ksei_manifest['snapshot_date'],
    'Yahoo retrieval time UTC': price_manifest['retrieved_at_utc'],
}, name='value').to_frame()
summary"""
    ),
    md(
        """## Build the current research table

Yahoo supplies provider-reported `sharesOutstanding`, `floatShares`, and `marketCap`. The notebook also calculates `market_cap_recomputed_idr = sharesOutstanding × latest unadjusted close` as a consistency check. These fields can have different effective timestamps and are not official IDX or audited values."""
    ),
    code(
        """current = registered.loc[
    registered['ticker'].astype(str).str.fullmatch(r'[A-Z]{4}')
].merge(
    prices.loc[prices['price_status'].eq('available')],
    on='ticker',
    how='inner',
    validate='one_to_one',
    suffixes=('_ksei', '_yahoo'),
)
current = current.merge(
    company_metadata.drop_duplicates('ticker'),
    on='ticker',
    how='left',
    validate='one_to_one',
    suffixes=('', '_metadata'),
)
current['market_cap_recomputed_idr'] = current['sharesOutstanding'] * current['close_idr']
current['market_cap_trillion_idr'] = current['marketCap'] / 1e12
current['market_cap_recomputed_trillion_idr'] = current['market_cap_recomputed_idr'] / 1e12
current['market_cap_difference_pct'] = 100 * (
    current['market_cap_recomputed_idr'] / current['marketCap'] - 1
)
current['price_age_days_at_snapshot'] = (
    pd.Timestamp(ksei_manifest['snapshot_date']) - pd.to_datetime(current['price_date'])
).dt.days.astype('Int64')

sector_column = 'sector'
current[sector_column] = current[sector_column].fillna('Unclassified by Yahoo')
current['industry'] = current['industry'].fillna('Unclassified by Yahoo')
current.shape"""
    ),
    md(
        """## Sector and industry catalogue

These are **Yahoo sector and industry classifications**, not IDX-IC. They are useful for navigation and comparison but must not be presented as the exchange's official taxonomy. The notebook will adopt IDX-IC only after a reproducible official IDX extract becomes available."""
    ),
    code(
        """sector_summary = (
    current.groupby(sector_column, dropna=False)
    .agg(
        securities=('ticker', 'size'),
        with_price=('close_idr', 'count'),
        industries=('industry', 'nunique'),
        with_issued_shares=('sharesOutstanding', 'count'),
        market_cap_coverage=('marketCap', 'count'),
        reported_market_cap_idr=('marketCap', 'sum'),
    )
    .sort_values(['reported_market_cap_idr', 'securities'], ascending=False)
)
sector_summary['reported_market_cap_trillion_idr'] = sector_summary['reported_market_cap_idr'] / 1e12
sector_summary"""
    ),
    md("## Largest securities by estimated market capitalization"),
    code(
        """display_columns = [
    'ticker', 'registry_name', sector_column, 'industry', 'price_date', 'close_idr',
    'sharesOutstanding', 'floatShares', 'market_cap_trillion_idr',
    'market_cap_recomputed_trillion_idr', 'market_cap_difference_pct', 'volume_shares'
]
largest_by_market_cap = current.dropna(subset=['marketCap']).sort_values(
    ['marketCap', 'ticker'], ascending=[False, True]
)
largest_by_market_cap[display_columns].head(50)"""
    ),
    md(
        """## Highest nominal share prices

A high rupiah price per share does **not** make a company larger or more expensive by valuation. Share price depends on the number of issued shares and past splits. Use the market-cap table for size and valuation ratios for relative valuation."""
    ),
    code(
        """highest_share_prices = current.dropna(subset=['close_idr']).sort_values(
    ['close_idr', 'ticker'], ascending=[False, True]
)
highest_share_prices[[
    'ticker', 'registry_name', sector_column, 'price_date', 'close_idr',
    'volume_shares', 'sharesOutstanding', 'floatShares', 'market_cap_trillion_idr'
]].head(50)"""
    ),
    md("## Browse every current security, organized by sector and size"),
    code(
        """all_current_stocks = current.sort_values(
    [sector_column, 'marketCap', 'close_idr', 'ticker'],
    ascending=[True, False, False, True],
    na_position='last',
)
all_current_stocks[[
    'ticker', 'registry_name', sector_column, 'price_status', 'price_date',
    'close_idr', 'sharesOutstanding', 'floatShares', 'market_cap_trillion_idr',
    'volume_shares', 'currency', 'exchange', 'detail_url'
]]"""
    ),
    md("## Coverage exceptions requiring review"),
    code(
        """coverage_exceptions = current.loc[
    current['sharesOutstanding'].isna()
    | current['marketCap'].isna()
    | current[sector_column].eq('Unclassified by Yahoo')
].copy()
coverage_exceptions[[
    'ticker', 'registry_name', sector_column, 'industry', 'metadata_status',
    'price_date', 'close_idr', 'sharesOutstanding', 'marketCap', 'detail_url'
]].sort_values(['metadata_status', 'ticker'])"""
    ),
    md(
        """## Interpretation rules

- The table is a research inventory, not a recommendation or order list.
- KSEI registration and Yahoo price availability do not guarantee current IDX listing, normal liquidity, or immediate purchasability.
- Yahoo's last daily bar is not an official real-time IDX quote; verify the price before any decision.
- Yahoo market capitalization and share counts are provider metadata; verify important figures against dated issuer and IDX disclosures.
- Nominal price should never be used alone to decide whether a stock is “cheap.” Compare business quality, balance sheet, cash flow, per-share fundamentals, valuation, governance, liquidity, and risk.
- A historical backtest needs point-in-time membership, delistings, suspensions, corporate actions, costs, and publication dates; this current snapshot must not be projected backward."""
    ),
    md(
        """## Sources and reproducible refresh

- KSEI registered-share master: `scripts/fetch_ksei_stock_universe.py`
- Yahoo daily snapshot: `scripts/fetch_yahoo_stock_snapshot.py`
- Yahoo sector, industry, market-cap, and share metadata: `scripts/fetch_yahoo_company_snapshot.py`
- Official IDX monthly stock-price table was attempted for IDX-IC classification, but its table endpoint remained stuck at “Loading Data” and the Excel action did not produce a file. KSEI detail enrichment was also throttled. Yahoo classifications are therefore retained and labelled honestly rather than misrepresented as IDX-IC.
- Yahoo's actual data rights are separate from the Apache-licensed `yfinance` client. The bulk Yahoo cache remains under `private/`.

Refresh prices with:

```bash
PYTHONNOUSERSITE=1 uv run --isolated --with 'numpy<2' --with yfinance \\
  python scripts/fetch_yahoo_stock_snapshot.py --as-of YYYY-MM-DD

PYTHONNOUSERSITE=1 uv run --isolated --with 'numpy<2' --with yfinance \\
  python scripts/fetch_yahoo_company_snapshot.py --as-of YYYY-MM-DD --workers 6
```
"""
    ),
]

notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {"name": "python", "version": "3"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

TARGET.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(TARGET)
