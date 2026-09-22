"""Build the educational product notebooks under products/.

The notebooks intentionally contain small, inspectable starter universes rather
than a recommendation engine. Re-run this script after editing the datasets or
notebook text below.
"""

from __future__ import annotations

import json
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRODUCTS = ROOT / "products"


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


def notebook(cells: list[dict]) -> dict:
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def table_cell(rows: list[dict], variable: str = "universe") -> dict:
    payload = json.dumps(rows, ensure_ascii=False, indent=2)
    return code(
        "import pandas as pd\n\n"
        f"{variable} = pd.DataFrame({payload})\n"
        f"{variable}"
    )


COMMON_WARNING = """> **Educational research universe—not a buy list.** Inclusion only means an instrument is useful to study. Before investing, verify current availability, legal documents, price/NAV, fees, liquidity, tax, risks, and whether it fits your goals and loss capacity. Names and classifications can change. Starter lists last reviewed: **2026-09-18**."""


def write_book(folder: str, filename: str, cells: list[dict]) -> None:
    target_dir = PRODUCTS / folder
    for child in ("data", "notes", "reports"):
        (target_dir / child).mkdir(parents=True, exist_ok=True)
        keep = target_dir / child / ".gitkeep"
        keep.touch(exist_ok=True)
    target = target_dir / filename
    target.write_text(json.dumps(notebook(cells), ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


cash_rows = [
    {"product_type": "Bank savings account", "liquidity": "Very high", "return_form": "Variable interest", "principal_risk": "Bank/LPS eligibility conditions", "research_first": "Admin fee, withdrawal access, LPS conditions"},
    {"product_type": "Time deposit", "liquidity": "Low until maturity", "return_form": "Fixed rate for tenor", "principal_risk": "Bank/LPS eligibility conditions", "research_first": "Tenor, penalty, roll-over, tax, LPS rate ceiling"},
    {"product_type": "Digital-bank deposit", "liquidity": "Low to medium", "return_form": "Often promotional/variable", "principal_risk": "Bank/LPS eligibility conditions", "research_first": "Whether rate exceeds LPS ceiling, terms after promo"},
    {"product_type": "Money-market instrument/fund", "liquidity": "High, not instant cash", "return_form": "NAV movement", "principal_risk": "Not a bank deposit and not LPS-guaranteed", "research_first": "Portfolio maturity, fees, settlement, credit quality"},
]

bonds_rows = [
    {"family": "ORI", "issuer": "Republic of Indonesia", "structure": "Conventional retail government bond", "coupon_pattern": "Fixed", "tradability": "Tradable after minimum holding period", "example": "ORI029T3 / ORI029T6 (2026 issuance example; offering may be closed)"},
    {"family": "SBR", "issuer": "Republic of Indonesia", "structure": "Savings Bond Ritel", "coupon_pattern": "Floating with floor", "tradability": "Non-tradable; limited early redemption", "example": "Use current DJPPR retail-SBN page"},
    {"family": "SR", "issuer": "Republic of Indonesia", "structure": "Retail sovereign sukuk", "coupon_pattern": "Typically fixed rental/return", "tradability": "Tradable after minimum holding period", "example": "Use current DJPPR retail-SBN page"},
    {"family": "ST", "issuer": "Republic of Indonesia", "structure": "Savings sovereign sukuk", "coupon_pattern": "Floating with floor", "tradability": "Non-tradable; limited early redemption", "example": "Use current DJPPR retail-SBN page"},
    {"family": "FR", "issuer": "Republic of Indonesia", "structure": "Wholesale fixed-rate government bond", "coupon_pattern": "Fixed", "tradability": "Secondary market", "example": "Compare yield-to-maturity and duration, not coupon alone"},
    {"family": "PBS", "issuer": "Republic of Indonesia", "structure": "Project-based sovereign sukuk", "coupon_pattern": "Series-specific", "tradability": "Secondary market", "example": "Read series terms and underlying structure"},
    {"family": "Corporate bond", "issuer": "Company/SOE/bank", "structure": "Senior or subordinated conventional debt", "coupon_pattern": "Series-specific", "tradability": "Often less liquid", "example": "Compare rating, covenants, maturity, spread, and issuer cash flow"},
    {"family": "Corporate sukuk", "issuer": "Company/SOE/bank", "structure": "e.g., ijarah or mudharabah", "coupon_pattern": "Structure-specific", "tradability": "Often less liquid", "example": "Read akad, payment waterfall, rating, and liquidity"},
]

fund_rows = [
    {"fund_name": "Mandiri Investa Pasar Uang Class A", "category_to_verify": "Money market", "what_to_compare": "Yield after fees, weighted maturity, settlement, credit quality"},
    {"fund_name": "Principal Cash Fund", "category_to_verify": "Money market", "what_to_compare": "Yield after fees, holdings, concentration, settlement"},
    {"fund_name": "Mandiri Pasar Uang Syariah Maslahat Class A", "category_to_verify": "Sharia money market", "what_to_compare": "Sharia portfolio, fees, liquidity, credit quality"},
    {"fund_name": "Mandiri Investa Dana Obligasi Seri II Class A", "category_to_verify": "Fixed income", "what_to_compare": "Duration, yield, credit exposure, drawdown"},
    {"fund_name": "Mandiri Investa Indeks Obligasi Negara Class A", "category_to_verify": "Government-bond index", "what_to_compare": "Index method, tracking difference, duration, fees"},
    {"fund_name": "Schroder Dana Prestasi Plus", "category_to_verify": "Equity", "what_to_compare": "Benchmark, active share, fees, rolling drawdown"},
    {"fund_name": "Mandiri Investa Ekuitas Dinamis", "category_to_verify": "Equity", "what_to_compare": "Mandate, sector weights, turnover, fees"},
    {"fund_name": "Panin Dana Maksima", "category_to_verify": "Equity", "what_to_compare": "Benchmark, concentration, drawdown, fees"},
    {"fund_name": "Schroder Dana Kombinasi", "category_to_verify": "Mixed", "what_to_compare": "Strategic allocation, rebalancing, benchmark, fees"},
    {"fund_name": "Mandiri Investa Syariah Berimbang", "category_to_verify": "Sharia mixed", "what_to_compare": "Allocation range, sharia screen, fees, drawdown"},
    {"fund_name": "Mandiri Indeks FTSE Indonesia ESG Class A", "category_to_verify": "Equity index/ESG", "what_to_compare": "Index rules, tracking difference, concentration, fees"},
]

etf_rows = [
    {"ticker": "R-LQ45X", "name": "Premier ETF LQ-45", "exposure_to_verify": "LQ45 equity index", "research_first": "Spread, on-screen depth, NAV discount/premium, tracking difference"},
    {"ticker": "XIIT", "name": "Premier ETF IDX30", "exposure_to_verify": "IDX30 equity index", "research_first": "Spread, liquidity, concentration, tracking difference"},
    {"ticker": "XMLF", "name": "Mandiri ETF LQ45", "exposure_to_verify": "LQ45 equity index", "research_first": "Spread, liquidity, NAV, fees"},
    {"ticker": "XCLQ", "name": "Cipta ETF Index LQ45", "exposure_to_verify": "LQ45 equity index", "research_first": "Spread, liquidity, NAV, fees"},
    {"ticker": "XIID", "name": "Premier ETF Index IDX30", "exposure_to_verify": "IDX30 equity index", "research_first": "Spread, liquidity, tracking difference, fees"},
    {"ticker": "XMGB", "name": "Majoris Government Bonds ETF Indonesia", "exposure_to_verify": "Government bonds", "research_first": "Duration, yield, spread, NAV, interest-rate sensitivity"},
    {"ticker": "XMSK", "name": "Mandiri ETF SRI-KEHATI", "exposure_to_verify": "SRI-KEHATI equity index", "research_first": "Index methodology, concentration, spread, tracking"},
    {"ticker": "XPDV", "name": "Pinnacle Core High Dividend ETF", "exposure_to_verify": "Dividend-oriented equities", "research_first": "Index rules, dividend traps, sector concentration, spread"},
]

stock_rows = [
    {"ticker": "BBCA", "company": "PT Bank Central Asia Tbk", "sector": "Financials", "field": "Private bank", "first_metrics": "NIM, CASA, cost of credit, NPL, ROE, valuation"},
    {"ticker": "BBRI", "company": "PT Bank Rakyat Indonesia (Persero) Tbk", "sector": "Financials", "field": "State-owned bank / microfinance", "first_metrics": "NIM, micro credit, CASA, CoC, NPL, ROE"},
    {"ticker": "BMRI", "company": "PT Bank Mandiri (Persero) Tbk", "sector": "Financials", "field": "State-owned diversified bank", "first_metrics": "NIM, CASA, CoC, NPL, ROE, subsidiaries"},
    {"ticker": "BBNI", "company": "PT Bank Negara Indonesia (Persero) Tbk", "sector": "Financials", "field": "State-owned corporate bank", "first_metrics": "Loan mix, NIM, CASA, CoC, NPL, ROE"},
    {"ticker": "TLKM", "company": "PT Telkom Indonesia (Persero) Tbk", "sector": "Infrastructures", "field": "Telecommunications", "first_metrics": "ARPU, subscribers, data traffic, capex, FCF"},
    {"ticker": "JSMR", "company": "PT Jasa Marga (Persero) Tbk", "sector": "Infrastructures", "field": "Toll roads", "first_metrics": "Traffic, tariff, concession life, debt, interest coverage"},
    {"ticker": "ICBP", "company": "PT Indofood CBP Sukses Makmur Tbk", "sector": "Consumer non-cyclicals", "field": "Packaged food", "first_metrics": "Volume, pricing, gross margin, FX, ROIC"},
    {"ticker": "INDF", "company": "PT Indofood Sukses Makmur Tbk", "sector": "Consumer non-cyclicals", "field": "Integrated food", "first_metrics": "Segment margin, commodity exposure, holding discount, debt"},
    {"ticker": "AMRT", "company": "PT Sumber Alfaria Trijaya Tbk", "sector": "Consumer non-cyclicals", "field": "Minimarket retail", "first_metrics": "Same-store sales, store count, inventory, margin, leases"},
    {"ticker": "KLBF", "company": "PT Kalbe Farma Tbk", "sector": "Healthcare", "field": "Pharmaceuticals and consumer health", "first_metrics": "Product mix, margin, R&D, working capital, ROIC"},
    {"ticker": "PTBA", "company": "PT Bukit Asam Tbk", "sector": "Energy", "field": "Coal mining", "first_metrics": "Volume, realized coal price, cash cost, reserves, capex"},
    {"ticker": "PGAS", "company": "PT Perusahaan Gas Negara Tbk", "sector": "Energy", "field": "Gas transmission/distribution", "first_metrics": "Volume, spread, regulation, infrastructure, debt"},
    {"ticker": "ANTM", "company": "PT Aneka Tambang Tbk", "sector": "Basic materials", "field": "Diversified mining/metals", "first_metrics": "Nickel/gold volume, realized price, cash cost, capex"},
    {"ticker": "INCO", "company": "PT Vale Indonesia Tbk", "sector": "Basic materials", "field": "Nickel mining", "first_metrics": "Production, nickel price, cash cost, projects, ownership"},
    {"ticker": "ASII", "company": "PT Astra International Tbk", "sector": "Industrials", "field": "Diversified conglomerate", "first_metrics": "Segment earnings, auto share, finance subsidiaries, NAV"},
    {"ticker": "GOTO", "company": "PT GoTo Gojek Tokopedia Tbk", "sector": "Technology", "field": "Digital ecosystem", "first_metrics": "GTV, contribution margin, cash burn, dilution, path to profit"},
]

gold_rows = [
    {"product": "ANTAM Logam Mulia physical gold", "form": "Physical bars", "main_costs": "Dealer spread, storage, assay/buyback terms", "main_risks": "Theft/loss, counterfeit channel, wide spread"},
    {"product": "UBS physical gold", "form": "Physical bars", "main_costs": "Dealer spread, storage, buyback terms", "main_risks": "Theft/loss, authenticity/channel, wide spread"},
    {"product": "Pegadaian Tabungan Emas", "form": "Custodied/digital gold balance", "main_costs": "Buy-sell spread, account/storage/printing fees", "main_risks": "Provider/terms, conversion rules, not the same as holding bars"},
    {"product": "Other regulated digital-gold service", "form": "Provider claim/custodied balance", "main_costs": "Spread, custody, withdrawal/conversion fees", "main_risks": "Verify regulator, custodian, backing, redemption, counterparty"},
]

property_rows = [
    {"vehicle": "DIRE", "meaning": "Dana Investasi Real Estat", "exposure": "Income-producing real estate through a collective investment vehicle", "research_first": "Portfolio appraisal, occupancy, WALE/lease expiry, debt, fees, distribution, liquidity"},
    {"vehicle": "DINFRA", "meaning": "Dana Investasi Infrastruktur", "exposure": "Infrastructure assets/projects through a collective investment vehicle", "research_first": "Concession/cash-flow terms, counterparty, leverage, valuation, liquidity"},
    {"vehicle": "Property-sector IDX stock", "meaning": "Listed operating/development company", "exposure": "Company equity, not direct ownership of its buildings", "research_first": "Presales, land bank, recurring income, net debt, related parties"},
    {"vehicle": "Direct property", "meaning": "Land/building ownership", "exposure": "Concentrated physical asset", "research_first": "Title, tax, maintenance, vacancy, financing, transaction cost, local market"},
]

crypto_rows = [
    {"asset_or_product": "Bitcoin (BTC)", "category": "Crypto asset", "economic_question": "Scarce digital bearer asset thesis", "major_risks": "Extreme volatility, custody, regulation, no contractual cash flow"},
    {"asset_or_product": "Ether (ETH)", "category": "Crypto asset / smart-contract network", "economic_question": "Network usage, fees, issuance and staking economics", "major_risks": "Extreme volatility, protocol/contract/custody/regulatory risk"},
    {"asset_or_product": "Stablecoin", "category": "Token intended to track a fiat currency", "economic_question": "Reserve quality and redemption mechanism", "major_risks": "Depeg, issuer/custodian, freeze, platform, regulatory risk"},
    {"asset_or_product": "Staking/lending product", "category": "Yield-bearing crypto service", "economic_question": "Where the yield comes from", "major_risks": "Slashing, smart contract, leverage, counterparty, lock-up; not a bank deposit"},
]


write_book("cash_and_deposits", "01_cash_and_deposits_landscape.ipynb", [
    md(f"# Cash and Deposits — Indonesia\n\n{COMMON_WARNING}\n\nUse this notebook to separate emergency liquidity from return-seeking assets. Deposit rates are deliberately **not hard-coded** because offers and the LPS guarantee-rate ceiling change."),
    table_cell(cash_rows),
    md("## Decision fields\n\nFor each account record bank, product, opening date, rate, rate-expiry date, effective yield after admin fee and tax, withdrawal restrictions, LPS eligibility, and the official page retrieved date. Never store account numbers or credentials here."),
    code("comparison_columns = [\n    'provider', 'product', 'annual_rate', 'promo_expiry', 'admin_fee',\n    'tax_assumption', 'effective_yield', 'tenor', 'early_withdrawal_penalty',\n    'lps_eligible', 'source_url', 'retrieved_at'\n]\ncomparison_columns"),
    md("## Primary sources\n\n- LPS for guarantee conditions and the current guarantee-rate ceiling\n- OJK for institution licensing/status\n- The bank's official product terms\n\nDo not infer LPS coverage merely from a bank logo or promotional rate."),
])

write_book("bonds_and_sukuk", "02_bonds_and_sukuk_universe.ipynb", [
    md(f"# Bonds and Sukuk — Indonesia\n\n{COMMON_WARNING}\n\nA high coupon is not automatically a high expected return: price, maturity, yield, duration, credit risk, call terms, tax, and liquidity all matter."),
    table_cell(bonds_rows),
    code("def approximate_current_yield(annual_coupon_cash, clean_price):\n    return annual_coupon_cash / clean_price\n\n# This is only current yield—not yield to maturity.\napproximate_current_yield(6.0, 100.0)"),
    md("## Research checklist\n\n1. Download the official memorandum/prospectus and record retrieval date.\n2. Identify issuer, series, maturity, coupon/imbalan formula, payment dates, tradability, early-redemption/call terms, tax, minimum order, and settlement.\n3. For traded bonds calculate dirty price, accrued interest, yield to maturity, duration, and plausible sale spread.\n4. For corporate debt analyze rating, seniority, covenants, refinancing, and default recovery—not just the coupon."),
    md("## Primary sources\n\n- [DJPPR retail SBN](https://djppr.kemenkeu.go.id/sbnritel)\n- [DJPPR issuance-result summaries](https://djppr.kemenkeu.go.id/ringkasanhasilpenerbitan)\n- [ORI029T3/T6 issuance notice—historical 2026 example](https://djppr.kemenkeu.go.id/rencanapenjualanobligasinegararitelseriori029t3danori029t6)\n- IDX/KSEI and the official prospectus for listed/corporate instruments"),
])

write_book("mutual_funds", "03_mutual_funds_universe.ipynb", [
    md(f"# Reksa Dana / Mutual Funds — Indonesia\n\n{COMMON_WARNING}\n\nThe names below form a varied reading list. KSEI registration does not by itself prove that a fund is currently open, offered by your platform, suitable, or superior."),
    table_cell(fund_rows),
    code("universe.groupby('category_to_verify', dropna=False).size().rename('example_count').to_frame()"),
    md("## Compare within category\n\nUse total return after fees, rolling volatility and drawdown, portfolio holdings, duration/credit quality where relevant, concentration, benchmark appropriateness, tracking difference for index funds, AUM, subscription/redemption terms, and tax treatment. Do not compare an equity fund with a money-market fund using return alone."),
    md("## Primary sources\n\n- [KSEI registered mutual-fund list](https://web.ksei.co.id/services/registered-securities/mutual-funds?setLocale=id-ID)\n- [OJK mutual-fund education and category overview](https://sikapiuangmu.ojk.go.id/FrontEnd/images/FileDownload/203_3%20Pasar%20Modal-compressed.pdf)\n- Fund prospectus, fund fact sheet, and official investment-manager page\n\nAlways confirm the exact share class; two classes of the same fund can have different fees."),
])

write_book("etfs", "04_indonesia_etf_universe.ipynb", [
    md(f"# Exchange-Traded Funds — Indonesia\n\n{COMMON_WARNING}\n\nAn ETF can track an index reasonably while still being costly to trade if its bid–ask spread or market depth is poor."),
    table_cell(etf_rows),
    code("equity_like = universe[universe['exposure_to_verify'].str.contains('equity|IDX|LQ45|SRI', case=False, regex=True)]\nequity_like[['ticker', 'name', 'exposure_to_verify']]"),
    md("## Minimum pre-trade study\n\nRecord exchange status, latest prospectus, index methodology, AUM, management fee, tracking difference, indicative NAV if available, bid, ask, spread percentage, depth at several levels, normal daily traded value, creation-unit mechanism, and tax/fees. Observe several trading days; a one-minute snapshot is weak evidence."),
    md("## Primary sources\n\n- [KSEI mutual-fund/ETF register](https://web.ksei.co.id/services/registered-securities/mutual-funds?setLocale=id-ID)\n- [IDX market data](https://www.idx.co.id/id/data-pasar/)\n- The ETF prospectus, fund fact sheet, and index provider methodology"),
])

write_book("stocks", "05_indonesia_stock_universe.ipynb", [
    md(f"# Indonesia Stock Research Universe\n\n{COMMON_WARNING}\n\nThis notebook has **two layers**: (1) the complete official KSEI registered-share snapshot, and (2) a deliberately small 16-company learning universe. The registry is not a buy list and is not identical to the number of active IDX-listed companies."),
    code("from pathlib import Path\nimport json\nimport pandas as pd\n\ndef locate(relative_path):\n    candidates = [Path(relative_path), Path('products/stocks') / relative_path]\n    for candidate in candidates:\n        if candidate.exists():\n            return candidate\n    raise FileNotFoundError(f'Could not locate {relative_path}; tried {candidates}')\n\nmaster_path = locate('data/processed/ksei_registered_share_securities_2026-09-22.csv')\nmanifest_path = locate('data/manifests/ksei_stock_universe_2026-09-22.json')\nregistered_securities = pd.read_csv(master_path)\nmanifest = json.loads(manifest_path.read_text())\n\nsummary = pd.Series({\n    'KSEI registered share securities': len(registered_securities),\n    'Standard four-letter tickers in registry': int(registered_securities['has_standard_four_letter_ticker'].sum()),\n    'IDX listed companies (official reference period)': manifest['idx_listed_company_reference_count'],\n    'Registry minus listed-company reference': len(registered_securities) - manifest['idx_listed_company_reference_count'],\n    'Registry snapshot date': manifest['snapshot_date'],\n    'IDX reference period': manifest['idx_listed_company_reference_period'],\n}, name='value').to_frame()\nsummary"),
    md("## Layer 1 — Complete registered-share master\n\nThe 984 rows below are the complete KSEI **registered share securities** snapshot retrieved on 2026-09-22. This is broader than active IDX-listed ordinary companies: it can include preferred or special classes and registrations whose current status must be checked on the linked KSEI detail page. KSEI's count and IDX's company count therefore must not be substituted for each other."),
    code("registered_securities[['ticker', 'registry_name', 'registrar', 'registry_nominal', 'detail_url']].head(25)"),
    code("query = 'BANK'\nregistered_securities[\n    registered_securities['registry_name'].str.contains(query, case=False, na=False)\n][['ticker', 'registry_name', 'detail_url']].head(30)"),
    md("## Layer 2 — Curated learning universe\n\nThese 16 recognizable companies were chosen to teach different business models and sector-specific metrics. They cover only a small fraction of the market. Large or famous does not mean cheap, safe, liquid, or suitable."),
    table_cell(stock_rows, variable="curated_learning_universe"),
    code("official_company_reference = manifest['idx_listed_company_reference_count']\nmissing_from_registry = sorted(set(curated_learning_universe['ticker']) - set(registered_securities['ticker']))\nassert not missing_from_registry, f'Curated tickers missing from KSEI registry: {missing_from_registry}'\n\npd.Series({\n    'curated_companies': len(curated_learning_universe),\n    'official_IDX_company_reference': official_company_reference,\n    'curated_coverage_percent': round(100 * len(curated_learning_universe) / official_company_reference, 2),\n    'IDX_IC_sectors_represented': curated_learning_universe['sector'].nunique(),\n}, name='value').to_frame()"),
    code("curated_learning_universe.groupby(['sector', 'field']).size().rename('companies').to_frame()"),
    md("## What is still absent from the curated layer\n\nIDX-IC has 11 broad sectors. The curated sample currently represents 8 and omits **Consumer Cyclicals**, **Properties & Real Estate**, and **Transportation & Logistic**. Future additions should be chosen for learning value and data quality, not merely to make the list longer."),
    md("## How to compare banks properly\n\nFor BBCA, BBRI, BMRI, and BBNI, build a point-in-time panel from audited reports and official disclosures. Compare loan growth, CASA ratio, NIM, cost-to-income, gross/net NPL, loan-at-risk, cost of credit, CET1/CAR, ROA, ROE, book value per share, P/B, and dividend payout. Align periods and definitions; never mix standalone and consolidated figures silently."),
    code("bank_tickers = ['BBCA', 'BBRI', 'BMRI', 'BBNI']\nbanks = curated_learning_universe[curated_learning_universe['ticker'].isin(bank_tickers)].copy()\nbanks[['ticker', 'company', 'field', 'first_metrics']]"),
    md("## Primary sources, scope, and data route\n\n- [KSEI registered-shares list](https://web.ksei.co.id/services/registered-securities/shares?setLocale=en-US) supplies the complete 984-security snapshot and one detail URL per code.\n- [IDX exchange-activities table](https://www2.idx.co.id/en/market-data/statistical-reports/digital-statistic/monthly/idx-trading-activities/indonesia-stock-exchange-activities?filter=eyJ5ZWFyIjoiMjAyNiIsIm1vbnRoIjoiNyIsInF1YXJ0ZXIiOjAsInR5cGUiOiJtb250aGx5In0%3D) reports 962 listed companies for July 2026.\n- [IDX stock-price table](https://www.idx.co.id/id/data-pasar/laporan-statistik/digital-statistic/monthly/trading-summary/table-of-stock-price) is the desired official source for current IDX-IC sector/subsector and market data, but its automated endpoint returned 403 during this snapshot.\n- [IDX Data Services](https://data.idx.co.id/) provides official licensed real-time, delayed, end-of-day, and historical products.\n- Issuer reports, [OJK data](https://data.ojk.go.id/SJKPublic/Dataset/Dataset), and [BI SEKI](https://www.bi.go.id/en/statistik/ekonomi-keuangan/seki/Default.aspx) support company, banking, and macro analysis.\n\nThe master CSV intentionally preserves KSEI terminology. It does **not** invent an IDX-IC sector for all 984 entries. Refresh classifications and current exchange/status before screening or analysis. Store publication date as well as period end to prevent look-ahead bias."),
])

write_book("gold", "06_gold_product_map.ipynb", [
    md(f"# Gold Product Map — Indonesia\n\n{COMMON_WARNING}\n\nGold has no contractual cash flow. Your result depends heavily on IDR gold-price movement and the actual buy–sell spread."),
    table_cell(gold_rows),
    code("def round_trip_break_even_pct(buy_price, immediate_buyback_price):\n    return (buy_price / immediate_buyback_price - 1) * 100\n\nround_trip_break_even_pct(1_100_000, 1_000_000)"),
    md("## Compare on the same date and unit\n\nRecord brand/provider, grams, buy price, buyback price, round-trip spread, all fees, delivery/conversion rules, storage, authenticity verification, regulator/licence where applicable, and source timestamp. Small bars often carry larger percentage spreads."),
    md("## Primary sources\n\nUse official ANTAM Logam Mulia, UBS, Pegadaian, and regulator/provider terms. Archive the quoted buy and buyback pages because prices change intraday."),
])

write_book("property_and_funds", "07_property_reits_and_infrastructure.ipynb", [
    md(f"# Property, DIRE, and Infrastructure Funds — Indonesia\n\n{COMMON_WARNING}\n\nA property-company share, DIRE, DINFRA, and a directly owned house are economically and legally different products."),
    table_cell(property_rows),
    md("## Analysis fields\n\nFor DIRE/DINFRA: exact registered product name/ticker, asset list, independent valuation date, occupancy/utilization, tenant or offtaker concentration, lease/concession expiry, debt maturity, interest coverage, fees, distribution history, bid–ask spread, and traded value. For direct property: title/legal due diligence, financing, tax, maintenance, insurance, vacancy, management time, and realistic transaction costs."),
    md("## Primary sources\n\n- [IDX DIRE & DINFRA overview](https://www.idx.co.id/id/produk/dire-dinfra)\n- OJK/KSEI registration and the product's latest prospectus\n- Issuer or manager reports and independent appraisals\n\nFetch the live registered/listed product list before naming a currently purchasable DIRE or DINFRA; availability and liquidity can change."),
])

write_book("crypto_assets", "08_crypto_asset_map.ipynb", [
    md(f"# Crypto-Asset Map — High-Risk Module\n\n{COMMON_WARNING}\n\nThis is a speculative-risk module, not a core portfolio prescription. Crypto can lose most or all of its value, and platform failure can prevent withdrawal even when the token still trades elsewhere."),
    table_cell(crypto_rows),
    md("## Gate before any allocation\n\nVerify the current Indonesian regulator and authorized-provider status, asset eligibility, custody arrangement, withdrawal test, fees/spread, wallet/address controls, tax, and incident history. Understand the asset independently of the platform. Never paste seed phrases, private keys, API secrets, or account identifiers into this project."),
    code("risk_questions = [\n    'What contractual cash flow or economic service supports value?',\n    'Who holds the private keys?',\n    'Can the asset be withdrawn on-chain?',\n    'What happens if the platform becomes insolvent?',\n    'What is the maximum loss in IDR and can I survive it?',\n    'Which current official rule and authorized-provider list did I verify?'\n]\nrisk_questions"),
    md("## Primary sources\n\nUse current OJK regulations and authorized-provider/asset lists, the provider's legal terms, and primary protocol documentation. Rules changed during Indonesia's regulatory transition, so do not rely on old articles or screenshots."),
])

print("Built 8 product notebooks under", PRODUCTS)
