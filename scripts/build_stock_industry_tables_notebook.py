"""Build the market-cap-sorted Indonesia stock industry tables notebook."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "products/stocks/06_industry_market_cap_tables.ipynb"


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
        """# Indonesian stocks grouped by industry and sorted by market capitalization

> **Educational research universe—not a buy list.** This notebook places every stock with available company metadata into a separate industry table and sorts each table from the largest to the smallest provider-reported market capitalization.

The classifications are **Yahoo Finance industries, not official IDX-IC industries**. Market capitalization, shares outstanding, float shares, and classifications are provider metadata that can be stale or incorrect. Verify important figures against dated issuer and IDX disclosures before making a decision.

The source snapshots are dated 2026-09-22. Bulk Yahoo data remain in the Git-ignored `private/` directory because Yahoo data rights are separate from the open-source `yfinance` client."""
    ),
    code(
        """from pathlib import Path
import json
import pandas as pd
from IPython.display import Markdown, display

pd.set_option('display.max_columns', 30)
pd.set_option('display.max_rows', 200)

# Objective: locate repository artifacts when executed from the root or notebook directory.
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

snapshot_date = '2026-09-22'
registry_path = locate(f'data/processed/ksei_registered_share_securities_{snapshot_date}.csv')
registry_manifest_path = locate(f'data/manifests/ksei_stock_universe_{snapshot_date}.json')
price_path = locate(f'market_data/yahoo/idx_latest_prices_{snapshot_date}.csv', private=True)
price_manifest_path = locate(f'market_data/yahoo/idx_latest_prices_{snapshot_date}.json', private=True)
metadata_path = locate(f'market_data/yahoo/idx_company_metadata_{snapshot_date}.csv', private=True)
metadata_manifest_path = locate(f'market_data/yahoo/idx_company_metadata_{snapshot_date}.json', private=True)

registry = pd.read_csv(registry_path)
registry_manifest = json.loads(registry_manifest_path.read_text())
prices = pd.read_csv(price_path)
price_manifest = json.loads(price_manifest_path.read_text())
metadata = pd.read_csv(metadata_path)
metadata_manifest = json.loads(metadata_manifest_path.read_text())

len(registry), len(prices), len(metadata)"""
    ),
    md(
        """## Coverage and definitions

The grouping universe consists of KSEI four-letter ticker candidates for which Yahoo returned company metadata. Stocks without Yahoo metadata cannot be assigned to a Yahoo industry and are reported as coverage exceptions rather than silently inserted into an invented category.

An “industry” below is the provider's descriptive industry field. It is more granular than its sector field. The five metadata-covered stocks with no industry value are retained under **Unclassified by Yahoo**."""
    ),
    code(
        """coverage = pd.Series({
    'KSEI registered share securities': len(registry),
    'standard four-letter ticker candidates': int(registry['ticker'].astype(str).str.fullmatch(r'[A-Z]{4}').sum()),
    'Yahoo price candidates requested': int(price_manifest['requested_ticker_count']),
    'Yahoo daily prices available': int(prices['price_status'].eq('available').sum()),
    'Yahoo daily prices missing': int(prices['price_status'].ne('available').sum()),
    'Yahoo company metadata rows available': int(metadata['metadata_status'].eq('available').sum()),
    'stocks with a named Yahoo industry': int(metadata['industry'].notna().sum()),
    'stocks unclassified by Yahoo': int(metadata['industry'].isna().sum()),
    'named Yahoo industries': int(metadata['industry'].nunique(dropna=True)),
    'metadata rows with market capitalization': int(metadata['marketCap'].notna().sum()),
    'snapshot date': snapshot_date,
    'Yahoo metadata retrieval UTC': metadata_manifest['retrieved_at_utc'],
}, name='value').to_frame()
coverage"""
    ),
    md("## Build and validate the industry universe"),
    code(
        """# Objective: merge the dated registry, price, and company snapshots without duplicating tickers.
universe = metadata.loc[metadata['metadata_status'].eq('available')].copy()
universe = universe.merge(
    registry[['ticker', 'registry_name', 'detail_url']],
    on='ticker',
    how='left',
    validate='one_to_one',
)
universe = universe.merge(
    prices.loc[prices['price_status'].eq('available'), [
        'ticker', 'price_date', 'close_idr', 'volume_shares', 'price_status'
    ]],
    on='ticker',
    how='left',
    validate='one_to_one',
)

universe['industry_group'] = universe['industry'].fillna('Unclassified by Yahoo')
universe['company_name'] = (
    universe['longName']
    .fillna(universe['shortName'])
    .fillna(universe['registry_name'])
)
universe['market_cap_idr_billion'] = universe['marketCap'] / 1e9
universe['market_cap_idr_trillion'] = universe['marketCap'] / 1e12
universe['float_pct_of_outstanding'] = 100 * universe['floatShares'] / universe['sharesOutstanding']

assert universe['ticker'].is_unique
assert len(universe) == int(metadata['metadata_status'].eq('available').sum())
assert universe['marketCap'].notna().all()
assert universe['industry_group'].notna().all()
universe.shape"""
    ),
    md(
        """## Industry catalogue

The catalogue is sorted by aggregate provider-reported market capitalization. This ordering is only for navigation; it does not rank industry attractiveness."""
    ),
    code(
        """industry_summary = (
    universe.groupby('industry_group', dropna=False)
    .agg(
        stock_count=('ticker', 'size'),
        sector_count=('sector', 'nunique'),
        total_market_cap_idr=('marketCap', 'sum'),
        median_market_cap_idr=('marketCap', 'median'),
        price_coverage=('close_idr', 'count'),
        issued_shares_coverage=('sharesOutstanding', 'count'),
        float_shares_coverage=('floatShares', 'count'),
    )
    .sort_values(['total_market_cap_idr', 'stock_count'], ascending=[False, False])
)
industry_summary['total_market_cap_idr_trillion'] = industry_summary['total_market_cap_idr'] / 1e12
industry_summary['median_market_cap_idr_billion'] = industry_summary['median_market_cap_idr'] / 1e9
industry_summary[[
    'stock_count', 'sector_count', 'total_market_cap_idr_trillion',
    'median_market_cap_idr_billion', 'price_coverage',
    'issued_shares_coverage', 'float_shares_coverage'
]]"""
    ),
    md("## Create one market-cap-sorted table for every industry"),
    code(
        """# Objective: create complete, non-overlapping industry tables sorted by market cap and ticker.
display_columns = [
    'rank_in_industry', 'ticker', 'company_name', 'sector', 'industry_group',
    'price_date', 'close_idr', 'market_cap_idr_billion',
    'market_cap_idr_trillion', 'sharesOutstanding', 'floatShares',
    'float_pct_of_outstanding', 'volume_shares', 'detail_url'
]

industry_order = industry_summary.index.tolist()
industry_tables = {}
for industry_name in industry_order:
    table = (
        universe.loc[universe['industry_group'].eq(industry_name)]
        .sort_values(['marketCap', 'ticker'], ascending=[False, True], na_position='last')
        .copy()
    )
    table.insert(0, 'rank_in_industry', range(1, len(table) + 1))
    industry_tables[industry_name] = table[display_columns].reset_index(drop=True)

combined_tickers = [
    ticker
    for table in industry_tables.values()
    for ticker in table['ticker'].tolist()
]
assert len(combined_tickers) == len(universe)
assert len(set(combined_tickers)) == len(universe)
assert set(combined_tickers) == set(universe['ticker'])
assert all(
    table['market_cap_idr_billion'].is_monotonic_decreasing
    for table in industry_tables.values()
)

validation = pd.Series({
    'industry tables created': len(industry_tables),
    'stocks across all tables': len(combined_tickers),
    'unique stocks across all tables': len(set(combined_tickers)),
    'stocks in source universe': len(universe),
    'duplicate ticker assignments': len(combined_tickers) - len(set(combined_tickers)),
    'all tables market-cap sorted descending': all(
        table['market_cap_idr_billion'].is_monotonic_decreasing
        for table in industry_tables.values()
    ),
}, name='value').to_frame()
validation"""
    ),
    md(
        """## All industry tables

Within every table, rank 1 has the largest provider-reported market capitalization in that industry. Market capitalization is shown in both **Rp billion** and **Rp trillion**. `float_pct_of_outstanding` is calculated from Yahoo's reported float shares and shares outstanding; it is not a substitute for an official IDX free-float disclosure."""
    ),
    code(
        """# Objective: display every industry as a visually separate, complete table.
for industry_name, table in industry_tables.items():
    industry_market_cap = table['market_cap_idr_trillion'].sum()
    display(Markdown(
        f'### {industry_name}  '
        f'\\n{len(table):,} stocks; combined reported market cap: '
        f'Rp{industry_market_cap:,.2f} trillion'
    ))
    formatted = table.style.format({
        'close_idr': '{:,.0f}',
        'market_cap_idr_billion': '{:,.2f}',
        'market_cap_idr_trillion': '{:,.4f}',
        'sharesOutstanding': '{:,.0f}',
        'floatShares': '{:,.0f}',
        'float_pct_of_outstanding': '{:,.2f}%',
        'volume_shares': '{:,.0f}',
    }, na_rep='—')
    display(formatted)"""
    ),
    md("## Stocks that could not enter an industry table"),
    code(
        """# Objective: retain price-coverage failures as an explicit audit table.
exception_columns = ['ticker', 'yahoo_symbol', 'price_status', 'error']
missing_price_metadata = prices.loc[
    prices['price_status'].ne('available')
].reindex(columns=exception_columns).merge(
    registry[['ticker', 'registry_name', 'detail_url']],
    on='ticker',
    how='left',
    validate='one_to_one',
).sort_values('ticker')

missing_price_metadata"""
    ),
    md(
        """## Interpretation and refresh rules

- These tables organize a dated research snapshot; they are not recommendations.
- Yahoo industry labels are not IDX-IC. Do not describe them as official exchange sectors or industries.
- A large market capitalization does not imply good value, high liquidity, good governance, or low risk.
- A small nominal share price does not mean that a stock is cheap.
- Provider-reported market capitalization can use share counts and prices from different effective times.
- Verify material figures against issuer financial statements, IDX disclosures, and official share-registration information.
- Missing-price candidates remain visible in the exception table and are not silently discarded.
- Historical analysis requires point-in-time membership, delistings, suspensions, corporate actions, costs, taxes, spreads, and publication dates.

Rebuild this notebook after refreshing the dated KSEI, price, and metadata snapshots:

```bash
python3 scripts/build_stock_industry_tables_notebook.py
```

The notebook deliberately reads Yahoo bulk snapshots from `private/`; it will not execute on a fresh public clone until the user creates those snapshots with the repository's fetch scripts."""
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
