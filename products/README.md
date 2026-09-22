# Financial Product Library

This folder organizes the learning project by **what is being studied**. The
top-level `learning/`, `planning/`, `analysis/`, and `execution/` folders remain
the cross-product workflow; for example, a portfolio comparison can combine
stocks, bonds, funds, and cash.

| Product folder | Starter notebook | What it answers |
|---|---|---|
| `cash_and_deposits/` | `01_cash_and_deposits_landscape.ipynb` | Liquidity, deposit structure, fees, tax, and LPS checks |
| `bonds_and_sukuk/` | `02_bonds_and_sukuk_universe.ipynb` | ORI, SBR, SR, ST, FR, PBS, and corporate debt categories |
| `mutual_funds/` | `03_mutual_funds_universe.ipynb` | Money-market, bond, equity, mixed, index, and sharia examples |
| `etfs/` | `04_indonesia_etf_universe.ipynb` | Indonesian ETF names/tickers and liquidity checks |
| `stocks/` | `05_indonesia_stock_universe.ipynb` | Complete KSEI registered-share snapshot plus a curated Indonesian company learning universe |
| `gold/` | `06_gold_product_map.ipynb` | Physical and custodied gold formats and their real costs |
| `property_and_funds/` | `07_property_reits_and_infrastructure.ipynb` | DIRE, DINFRA, property shares, and direct property |
| `crypto_assets/` | `08_crypto_asset_map.ipynb` | High-risk crypto categories, custody, and regulatory checks |

Every product folder also has `data/`, `notes/`, and `reports/` subfolders.
Raw source files belong in that product's `data/` folder; interpretation notes
go in `notes/`; finished comparisons go in `reports/`.

## Important boundary

The example instruments are an educational research universe, **not a buy
list**. A name appearing in a notebook is not a claim that it is currently
available, fairly valued, liquid, safe, or appropriate for a particular person.
Always refresh official sources, read the latest legal documents, and assess
goals, time horizon, currency needs, liquidity, and capacity for loss.

## Rebuild

From the Finance project folder:

```bash
python3 scripts/build_product_notebooks.py
```

The builder keeps the starter universes inspectable and reproducible. Later,
live or downloaded data should be saved with source URL, retrieval timestamp,
release/effective date, period, units, currency, timezone, revision/vintage,
licence, file hash, and notes.

The stock master snapshot has a separate acquisition command:

```bash
python3 scripts/fetch_ksei_stock_universe.py \
  --as-of YYYY-MM-DD \
  --registry-only
```

KSEI registered share securities and IDX listed companies are related but not
identical populations. The stock notebook and its manifest preserve that scope
difference rather than silently treating the counts as interchangeable.
