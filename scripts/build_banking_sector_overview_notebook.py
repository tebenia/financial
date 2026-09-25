"""Build the Indonesian financial-sector and banking-market overview notebook."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "products/stocks/07_indonesia_banking_sector_overview.ipynb"


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
        """# Indonesian financial sector and banking market

> **A market study, not a buy list.** This notebook explains the structure, history, economics, risks, analytical metrics, and historical stock behaviour of Indonesian banking. It does not identify a universally “best” bank or promise future returns.

The analysis uses official OJK, Bank Indonesia, BPS, LPS, and issuer sources for institutional and financial facts. Historical stock comparisons use Yahoo adjusted-price data through **22 September 2026** and current Yahoo industry membership. Those comparisons contain survivorship, classification, liquidity, and provider-data limitations."""
    ),
    md(
        """## 1. Where banking fits in the financial sector

Indonesia's financial sector is an interconnected system:

```text
Households and companies
        |
        +-- Banks: deposits, payments, loans, treasury and transaction services
        +-- Capital markets: shares, government/corporate bonds, sukuk and funds
        +-- Insurance and pensions: protection and long-duration savings
        +-- Finance companies: vehicle, equipment, consumer and working-capital finance
        +-- Fintech/P2P/BNPL: specialised digital credit and payment interfaces
        `-- Payment infrastructure: BI-FAST, cards, transfers, QRIS and e-money

                         Regulators and safety net
        Bank Indonesia -- OJK -- LPS -- Ministry of Finance/KSSK
```

Banks are central because deposits are money-like liabilities, bank credit finances consumption and production, and banks connect payments, government securities, foreign exchange, insurance, asset management, and capital markets. This makes banking profitable in normal conditions but systemically sensitive when confidence, liquidity, or credit quality breaks.

As of July 2026, OJK reported Rp9,135 trillion of bank loans and Rp10,336 trillion of third-party deposits. For scale, OJK separately reported insurance assets of Rp1,172.9 trillion, pension-fund assets of Rp1,699.99 trillion, finance-company receivables of Rp513.05 trillion, and online-lending balances of Rp105.63 trillion. Banking is therefore not the whole financial sector, but it is its dominant balance-sheet intermediary.

Source: [OJK August 2026 financial-sector update](https://iru.ojk.go.id/iru/WebSite/ArticleList/View/1060_Press_Release_August_2026_of_The_Board_of_Commissioners%E2%80%99_Meeting_Financial_Services_Sector_Performance_And_Intermediation_Remain_Solid,_Supporting_Accelerated_Economic_Growth)."""
    ),
    md(
        """## 2. A short history of Indonesian banking

| Period | Structural change | Investor lesson |
|---|---|---|
| Before the 1980s | State banks dominated and often had specialised development mandates. | Ownership, policy mandates, and credit allocation have always mattered. |
| 1983–1988 deregulation | Interest-rate and licensing liberalisation culminated in **Pakto 88**, which made it much easier to establish banks and branches. | Competition and credit expanded rapidly, but governance and risk capacity did not always keep pace. |
| 1997–1998 Asian crisis | Rupiah depreciation, maturity/currency mismatches, connected lending, weak capital, and collapsing confidence produced bank closures and restructuring. | A bank can appear profitable until funding and credit losses interact; capital and governance matter more than reported growth. |
| 1998–2005 restructuring | Recapitalisation, consolidation, asset resolution, and stronger prudential rules rebuilt the system. LPS began operating in 2005, replacing the crisis-era blanket guarantee with a formal deposit-insurance framework. | The modern franchise value of major banks partly reflects post-crisis consolidation and stronger regulation. |
| 2004 onward | The Indonesian Banking Architecture promoted stronger capital, supervision, governance, and competitive structure. | Scale, capital, and risk management became durable strategic advantages. |
| 2011–2014 | The OJK law created integrated financial supervision; bank microprudential supervision transferred from BI to OJK on 31 December 2013, while BI retained macroprudential and monetary roles. | Bank analysis requires understanding both institution-level OJK rules and system-level BI policy. |
| 2010s | Mobile banking, branchless banking, payments, and ecosystem strategies increased the value of cheap transaction deposits and technology. | A digital interface is valuable only if it creates deposits, transactions, sound loans, and sustainable unit economics. |
| 2021 onward | The BSI merger created a national-scale Islamic bank. POJK 12/2021 reframed bank groups by core capital and formalised digital-bank provisions; conventional banks also accelerated digital transformations. | Mergers and “digital bank” stories can change growth expectations faster than profits, producing major valuation cycles. |

Primary references: [Bank Indonesia history](https://www.bi.go.id/id/tentang-bi/sejarah-bi/default.aspx), [BI on the 2004 Banking Architecture](https://www.bi.go.id/id/publikasi/kajian/Documents/562fcb847f5046b8802094b73a80c0dbKSKDes2003.pdf), [LPS history and the post-crisis safety net](https://lps.go.id/konten/unggahan/2023/07/AR-2013-LPS.pdf), [OJK transfer of bank supervision](https://ojk.go.id/id/kanal/pasar-modal/berita-dan-kegiatan/siaran-pers/Pages/siaran-pers-bi-alihkan-fungsi-pengaturan-dan-pengawasan-perbankan-kepada-ojk.aspx), [POJK 12/2021](https://www.ojk.go.id/id/regulasi/Documents/Pages/Bank-Umum/POJK%2012%20-%2003%20-2021.pdf), and [BSI merger history](https://ir.bankbsi.co.id/articles_of_association.html)."""
    ),
    md(
        """## 3. How a bank makes money

A simplified bank income statement is:

```text
Interest income from loans and securities
- interest paid on deposits and wholesale funding
= net interest income
+ fees, payments, wealth, treasury and other non-interest income
- operating expenses and technology
- expected credit-loss provisions
- tax
= net profit
```

The central economic engine is not simply “lend at 10%, pay depositors 4%, keep 6%.” Banks must hold liquidity and capital, absorb defaults, fund branches and technology, meet regulation, and compete for deposits and borrowers.

### Why banking can be attractive to shareholders

- **Structural credit demand:** A growing, formalising economy needs mortgages, working-capital loans, investment finance, payments, and savings products.
- **Deposit franchise:** Current and savings accounts (`CASA`) can be stable and inexpensive. Transaction-led banks can fund loans more cheaply than banks dependent on deposits purchased at high rates.
- **Scale and data:** Large networks and digital ecosystems spread technology, compliance, and product-development costs across many customers.
- **Recurring relationships:** Salary accounts, merchant payments, supply chains, mortgages, and corporate cash management create switching costs and cross-selling opportunities.
- **Moderate financial leverage:** A sound bank can turn a modest return on assets into an attractive return on equity, provided capital and credit risk remain controlled.
- **Dividends:** Mature banks can distribute substantial cash after funding growth and regulatory capital.
- **Economic optionality:** Better financial inclusion, formalisation, digital payments, and rising household wealth expand the addressable market.

### Why banking can be dangerous

- **Leverage:** A small percentage loss on a large loan book can consume a meaningful share of equity.
- **Asset–liability mismatch:** Loans are long and illiquid; deposits can leave quickly.
- **Credit-cycle lag:** Fast loan growth looks good before defaults appear. Losses often emerge 12–36 months later.
- **Confidence:** Even a solvent bank can face a liquidity crisis if depositors or wholesale lenders lose confidence.
- **Opaque accounting:** Restructuring, evergreening, collateral values, related-party lending, and optimistic staging can delay recognition of problems.
- **Policy exposure:** Rates, reserve requirements, macroprudential incentives, directed programmes, ownership rules, and dividend expectations affect earnings and capital.
- **Technology and fraud:** Cyber incidents, outages, scams, data misuse, and anti-money-laundering failures create financial and reputational losses.
- **Valuation risk:** An excellent bank purchased at an excessive price can be a poor stock investment."""
    ),
    md(
        """## 4. The Indonesian banking market today

OJK's July 2026 snapshot describes a profitable and well-capitalised system, but aggregate strength does not mean every bank is equally safe.

| System indicator | July 2026 | Interpretation |
|---|---:|---|
| Loan growth | 13.58% YoY | Strong intermediation; investment loans grew 25.13%, much faster than consumer loans at 5.38%. |
| Outstanding loans | Rp9,135 tn | Large exposure to the domestic economic and credit cycle. |
| Deposit growth | 11.21% YoY | Funding grew slightly slower than loans; composition and price matter. |
| Third-party deposits | Rp10,336 tn | The system's principal funding base. |
| Gross NPL | 2.10% | Reported impaired loans are contained in aggregate. |
| Net NPL | 0.81% | Provisions absorb much of recognised NPL exposure. |
| Loan at Risk | 8.39% | Broader early-warning measure; more informative than NPL alone. |
| ROA | 2.45% | Strong aggregate profitability for a banking system. |
| CAR | 23.84% | Large capital buffer in aggregate, but bank-level composition differs. |
| AL/DPK | 23.10% | Liquid assets substantially exceed the 10% threshold. |
| LCR | 187.5% | High-quality liquid-asset coverage is strong in aggregate. |

By 23 September 2026, BI had held the BI-Rate at **5.75%** while prioritising rupiah stability; August inflation was **3.19% YoY**, and the rupiah was Rp17,855/USD on 22 September. BPS reported real GDP growth of **5.29% YoY** in Q2 2026. These conditions support nominal credit growth but also create funding-cost, currency, and borrower-affordability pressure. Sources: [OJK](https://iru.ojk.go.id/iru/WebSite/ArticleList/View/1060_Press_Release_August_2026_of_The_Board_of_Commissioners%E2%80%99_Meeting_Financial_Services_Sector_Performance_And_Intermediation_Remain_Solid,_Supporting_Accelerated_Economic_Growth), [Bank Indonesia September 2026 decision](https://www.bi.go.id/id/publikasi/ruang-media/news-release/Pages/sp_2819326.aspx), and [BPS Q2 2026 GDP](https://www.bps.go.id/id/pressrelease/2026/08/05/2605/ekonomi-indonesia-triwulan-II-2026-tumbuh-5-29-persen--y-on-y-.html-Ekonomi)."""
    ),
    md(
        """## 5. What moves bank profits and bank shares

### External factors

| Driver | Transmission into banks |
|---|---|
| BI policy rate and yield curve | Reprices loans, deposits, securities, hedges, and valuation multiples. The effect depends on how quickly assets and liabilities reprice. |
| Rupiah and global rates | Affect foreign funding, capital flows, imported inflation, corporate borrowers, and investor risk premiums. |
| GDP, employment, wages, and consumption | Drive loan demand, transaction volumes, and borrowers' repayment capacity. |
| Commodity cycle | Influences corporate credit, regional economies, contractors, government revenue, and household income. |
| Property and vehicle cycles | Affect collateral, mortgages, multifinance subsidiaries, consumer credit, and construction exposure. |
| Fiscal and state policy | State banks may benefit from government ecosystems and programmes but can also face policy-related allocation or payout pressure. |
| Regulation | Capital, liquidity, provisioning, consumer protection, data, ownership, and digital rules change economics and competitive barriers. |
| Competition | Deposit wars raise funding costs; fintech and digital banks pressure fees and customer acquisition economics. |
| Shocks | Pandemics, disasters, geopolitical stress, and fraud can affect liquidity, credit, operations, and market valuations simultaneously. |

### Internal factors

- Deposit franchise: CASA mix, deposit concentration, cost of funds, retention, and transaction activity
- Loan mix: corporate, commercial, SME, micro, mortgage, consumer, cards, BNPL, and sector concentration
- Underwriting: vintage performance, restructurings, collateral, related parties, and risk-adjusted pricing
- Asset quality: NPL/NPF, Loan at Risk, Stage 2 loans, write-offs, recoveries, and coverage
- Profitability: NIM/net imbalan, fees, cost of credit, efficiency, ROA, and sustainable ROE
- Capital and liquidity: CET1/Tier 1, CAR, LDR/FDR, LCR, NSFR, and maturity gaps
- Governance: controlling shareholder, board independence, related-party transactions, audit quality, and regulatory history
- Technology: active users, transaction volume, uptime, fraud losses, acquisition cost, and conversion to deposits or profitable credit
- Capital allocation: dividends, retained earnings, rights issues, acquisitions, dilution, and subsidiary funding
- Valuation and market structure: P/B, P/E, dividend yield, free float, liquidity, index weight, and foreign ownership"""
    ),
    md(
        """## 6. Metrics that deserve priority

No single ratio is sufficient. A bank can report a high NIM because it takes more credit risk, a high ROE because it holds less capital, or a low NPL because it has recently grown fast and losses have not matured.

| Metric | Basic interpretation | What to ask next |
|---|---|---|
| Loan growth | Expansion of earning assets | Is growth faster than deposits, capital, underwriting capacity, or the market? |
| CASA ratio | Low-cost current and savings deposits / deposits | Are accounts active and diversified, or concentrated and rate-sensitive? |
| Cost of funds | Price paid for deposits and funding | Is the bank buying growth with expensive deposits? |
| NIM / net imbalan | Net interest income relative to earning assets | Is the margin structural, rate-driven, or compensation for risk? |
| Gross and net NPL/NPF | Recognised problem credit | Are restructurings, write-offs, and Stage 2 loans rising? |
| Loan at Risk | NPL plus other stressed/restructured exposures | Does the broader risk pool contradict a reassuring NPL number? |
| Cost of credit | Provisions relative to loans | Is current profit relying on unusually low provisions? |
| Coverage ratio | Provisions relative to NPL/NPF | Is collateral realistic and are reserves sufficient? |
| ROA | Profit generated per unit of assets | More comparable across differently leveraged banks than ROE alone. |
| ROE | Profit generated on shareholder equity | Compare with cost of equity, capital adequacy, and one-off gains. |
| Cost-to-income / BOPO | Operating efficiency | Is improvement caused by durable productivity or deferred investment? |
| LDR/FDR | Loans or financing relative to deposits | Very low can indicate unused liquidity; very high can indicate funding pressure. |
| CAR and Tier 1/CET1 | Loss-absorbing capital relative to risk-weighted assets | Examine capital quality, buffers, and growth requirements. |
| LCR / NSFR | Short- and longer-term liquidity resilience | Look for depositor concentration and encumbered assets. |
| P/B | Market value relative to book equity | Interpret together with sustainable ROE and growth. |
| P/E | Price relative to earnings | Normalise provisions, treasury gains, recoveries, and tax effects. |
| Dividend yield/payout | Cash returned to shareholders | Is the payout compatible with capital needs and growth? |

A useful valuation identity is:

```text
Justified price-to-book approximately (sustainable ROE - long-run growth)
                                / (cost of equity - long-run growth)
```

It is not a precise pricing formula. It explains why a bank that sustainably earns far above its cost of equity deserves a higher P/B, while a bank earning below its cost of equity may remain below book value. Forecast quality is the hard part."""
    ),
    md(
        """## 7. Bank archetypes—not interchangeable businesses

| Archetype | Typical strength | Typical risk |
|---|---|---|
| Large state-owned universal banks | Scale, government/corporate ecosystems, distribution, liquidity, dividends | Policy influence, large corporate exposures, payout decisions, cyclicality |
| Large transaction-led private bank | Strong CASA, payments, conservative underwriting, high ROA | Premium valuation and concentration in a successful franchise |
| Foreign-backed/mid-sized universal banks | Governance, capital, niche corporate/consumer capabilities | Lower stock liquidity, controlling-owner actions, slower loan growth |
| Mortgage specialist | Long-duration customer relationship and housing policy tailwind | Interest-rate mismatch, property concentration, high LDR and credit duration |
| Microfinance specialist | High yields, financial-inclusion growth, granular loans | Borrower vulnerability, field-cost intensity, climate/income shocks, high credit cost |
| Regional development bank | Local government ecosystem and payroll deposits | Geographic/governance concentration and thin stock trading |
| Islamic bank | Structural demand, religious ecosystem, differentiated funding and products | Product concentration, integration/execution, benchmark-rate competition, distinct NPF/FDR metrics |
| Digital/turnaround bank | Low branch requirement, rapid customer acquisition, ecosystem optionality | High acquisition cost, unseasoned loans, dilution, execution risk, narrative-driven valuation |

Comparison must be matched to business model. A mortgage bank should not be judged by exactly the same margin, duration, and credit-cost expectations as a transaction bank or an unsecured digital lender."""
    ),
    md("## 8. Listed-bank market structure and concentration"),
    code(
        """from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display

pd.set_option('display.max_columns', 40)
pd.set_option('display.float_format', lambda value: f'{value:,.4f}')
plt.style.use('seaborn-v0_8-whitegrid')

# Objective: locate public and private artifacts from the repository root or notebook directory.
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
metadata_path = locate(f'market_data/yahoo/idx_company_metadata_{snapshot_date}.csv', private=True)
history_path = locate(f'market_data/yahoo/idx_bank_adjusted_history_{snapshot_date}.csv', private=True)
history_manifest_path = locate(f'market_data/yahoo/idx_bank_adjusted_history_{snapshot_date}.json', private=True)

metadata = pd.read_csv(metadata_path)
history = pd.read_csv(history_path, parse_dates=['date'])
history_manifest = json.loads(history_manifest_path.read_text())
banks = metadata.loc[
    metadata['metadata_status'].eq('available')
    & metadata['industry'].eq('Banks - Regional')
].copy()

len(banks), history['ticker'].nunique()"""
    ),
    code(
        """bank_market_cap = banks['marketCap'].sum()
market_structure = pd.Series({
    'Yahoo-classified listed bank names': len(banks),
    'Combined provider market cap (Rp tn)': bank_market_cap / 1e12,
    'Largest name share': banks.nlargest(1, 'marketCap')['marketCap'].sum() / bank_market_cap,
    'Top four share': banks.nlargest(4, 'marketCap')['marketCap'].sum() / bank_market_cap,
    'Top ten share': banks.nlargest(10, 'marketCap')['marketCap'].sum() / bank_market_cap,
    'Top twenty share': banks.nlargest(20, 'marketCap')['marketCap'].sum() / bank_market_cap,
}, name='value').to_frame()
market_structure"""
    ),
    code(
        """largest_banks = banks.nlargest(15, 'marketCap').copy()
largest_banks['market_cap_rp_tn'] = largest_banks['marketCap'] / 1e12
largest_banks['share_of_listed_bank_market_cap'] = largest_banks['marketCap'] / bank_market_cap
largest_banks[[
    'ticker', 'longName', 'market_cap_rp_tn', 'share_of_listed_bank_market_cap'
]].reset_index(drop=True).style.format({
    'market_cap_rp_tn': '{:,.2f}',
    'share_of_listed_bank_market_cap': '{:.2%}',
})"""
    ),
    md(
        """The provider snapshot is highly concentrated: the four largest names account for roughly three quarters of the combined listed-bank market capitalisation. This means banking-sector indices and broad Indonesian equity portfolios can be heavily driven by a few banks.

The 49-name count is a Yahoo classification, not an official OJK population. For example, a financial holding company can be labelled as a regional bank, and suspended or unavailable KSEI candidates may be absent. Market capitalisation is a provider estimate as of the snapshot, not an audited accounting figure."""
    ),
    md("## 9. Measuring rise, steadiness, and fluctuation"),
    code(
        """# Objective: compute comparable path-dependent return and risk measures over a fixed window.
def performance_metrics(prices, start, end):
    rows = []
    start = pd.Timestamp(start)
    end = pd.Timestamp(end)
    for ticker, group in prices.groupby('ticker'):
        window = (
            group.loc[group['date'].between(start, end)]
            .sort_values('date')
            .drop_duplicates('date')
            .dropna(subset=['adj_close'])
        )
        if len(window) < 2:
            continue
        daily_return = window['adj_close'].pct_change().dropna()
        monthly_return = (
            window.set_index('date')['adj_close']
            .resample('ME').last().pct_change().dropna()
        )
        wealth = window['adj_close'] / window['adj_close'].iloc[0]
        drawdown = wealth / wealth.cummax() - 1
        elapsed_days = (window['date'].iloc[-1] - window['date'].iloc[0]).days
        rows.append({
            'ticker': ticker,
            'first_date': window['date'].iloc[0],
            'last_date': window['date'].iloc[-1],
            'observations': len(window),
            'elapsed_years': elapsed_days / 365.25,
            'total_return': window['adj_close'].iloc[-1] / window['adj_close'].iloc[0] - 1,
            'cagr': (window['adj_close'].iloc[-1] / window['adj_close'].iloc[0]) ** (365.25 / elapsed_days) - 1,
            'annualized_volatility': daily_return.std() * np.sqrt(252),
            'maximum_drawdown': drawdown.min(),
            'positive_month_fraction': (monthly_return > 0).mean(),
            'zero_return_day_fraction': daily_return.eq(0).mean(),
            'median_daily_trading_value_idr': (window['close'] * window['volume']).median(),
        })
    return pd.DataFrame(rows)


five_year_start = '2021-09-22'
analysis_end = '2026-09-22'
metrics_5y = performance_metrics(history, five_year_start, analysis_end).merge(
    metadata[['ticker', 'longName', 'marketCap']], on='ticker', how='left'
)
metrics_5y['full_window'] = metrics_5y['first_date'].le(
    pd.Timestamp(five_year_start) + pd.Timedelta(days=14)
)
metrics_5y['stability_score'] = metrics_5y['cagr'] / metrics_5y['annualized_volatility']

# A transparent comparison subset—not a claim that excluded banks are uninvestable.
metrics_5y['mature_liquid_subset'] = (
    metrics_5y['full_window']
    & metrics_5y['marketCap'].ge(5e12)
    & metrics_5y['median_daily_trading_value_idr'].ge(1e9)
    & metrics_5y['zero_return_day_fraction'].lt(0.30)
    & metrics_5y['ticker'].ne('^JKSE')
    & metrics_5y['ticker'].ne('PNLF')  # financial holding company, not an operating bank
)

method_summary = pd.Series({
    'five-year start': five_year_start,
    'end': analysis_end,
    'bank tickers requested': history_manifest['requested_bank_count'],
    'bank symbols missing from history': len(history_manifest['missing_bank_symbols']),
    'full-window banks': int(metrics_5y.loc[metrics_5y['ticker'].ne('^JKSE'), 'full_window'].sum()),
    'mature/liquid comparison subset': int(metrics_5y['mature_liquid_subset'].sum()),
    'minimum current market cap': 'Rp5 trillion',
    'minimum median daily value': 'Rp1 billion',
    'maximum zero-return trading days': '30%',
}, name='value').to_frame()
method_summary"""
    ),
    md(
        """**Definitions**

- Total return and CAGR use Yahoo `Adj Close`, intended to adjust for splits and cash distributions.
- Annualised volatility is daily-return standard deviation × √252.
- Maximum drawdown is the worst fall from a previous adjusted-price peak.
- Positive-month fraction measures how often month-end return was positive.
- Zero-return days expose apparently “stable” but stale/thin trading.
- “Mature/liquid subset” requires a full five-year window, current market cap of at least Rp5 trillion, median daily value of at least Rp1 billion, and fewer than 30% zero-return days. These are transparent study filters, not regulatory definitions.

Five years begins near the 2021 digital-bank enthusiasm. Ten years starts before it. Results are therefore entry-date dependent."""
    ),
    code(
        """comparison_columns = [
    'ticker', 'longName', 'total_return', 'cagr', 'annualized_volatility',
    'maximum_drawdown', 'positive_month_fraction',
    'zero_return_day_fraction', 'median_daily_trading_value_idr'
]
subset_5y = metrics_5y.loc[metrics_5y['mature_liquid_subset']].copy()

top_risers_5y = subset_5y.sort_values('cagr', ascending=False)[comparison_columns]
top_risers_5y.style.format({
    'total_return': '{:.1%}',
    'cagr': '{:.1%}',
    'annualized_volatility': '{:.1%}',
    'maximum_drawdown': '{:.1%}',
    'positive_month_fraction': '{:.1%}',
    'zero_return_day_fraction': '{:.1%}',
    'median_daily_trading_value_idr': 'Rp{:,.0f}',
})"""
    ),
    code(
        """steady_positive_5y = (
    subset_5y.loc[subset_5y['cagr'].gt(0)]
    .sort_values(['stability_score', 'maximum_drawdown'], ascending=[False, False])
)
steady_positive_5y[[
    'ticker', 'longName', 'cagr', 'annualized_volatility',
    'maximum_drawdown', 'positive_month_fraction', 'stability_score'
]].style.format({
    'cagr': '{:.1%}',
    'annualized_volatility': '{:.1%}',
    'maximum_drawdown': '{:.1%}',
    'positive_month_fraction': '{:.1%}',
    'stability_score': '{:.2f}',
})"""
    ),
    code(
        """most_volatile_5y = subset_5y.sort_values('annualized_volatility', ascending=False)
most_volatile_5y[[
    'ticker', 'longName', 'total_return', 'cagr', 'annualized_volatility',
    'maximum_drawdown', 'positive_month_fraction'
]].style.format({
    'total_return': '{:.1%}',
    'cagr': '{:.1%}',
    'annualized_volatility': '{:.1%}',
    'maximum_drawdown': '{:.1%}',
    'positive_month_fraction': '{:.1%}',
})"""
    ),
    code(
        """fig, ax = plt.subplots(figsize=(10, 7))
plot_data = subset_5y.copy()
ax.scatter(
    100 * plot_data['annualized_volatility'],
    100 * plot_data['cagr'],
    s=np.clip(plot_data['marketCap'] / 2e11, 25, 500),
    alpha=0.65,
)
for row in plot_data.itertuples():
    ax.annotate(row.ticker, (100 * row.annualized_volatility, 100 * row.cagr),
                xytext=(4, 3), textcoords='offset points', fontsize=9)
ax.axhline(0, color='black', linewidth=0.8)
ax.set_title('Five-year return versus volatility: mature/liquid comparison subset')
ax.set_xlabel('Annualised daily volatility (%)')
ax.set_ylabel('Adjusted-price CAGR (%)')
plt.tight_layout()
plt.show()"""
    ),
    md(
        """## 10. What the five-year evidence says

For the fixed 22 September 2021–22 September 2026 window and the transparent mature/liquid filter:

- **BNGA and NISP combine the strongest CAGRs with the lowest volatility and shallowest drawdowns in the subset.** This is the clearest “rise plus steadiness” result for this particular window.
- **BDMN, BMRI, and BBNI** also produced strong adjusted returns, but with higher volatility and deeper drawdowns.
- **BBCA and BBRI remain high-quality, highly liquid franchises, but their five-year stock returns were much less impressive than their reputations might suggest.** Entry valuation and the ending market environment matter.
- **ARTO and BBHI** sit at the opposite extreme: narrative-driven digital-bank valuations produced very high volatility and drawdowns above 90% from the window's peaks. A business can improve while a stock performs badly if the starting valuation was too optimistic.
- **BRIS** improved operationally after the merger, but its five-year adjusted stock return was negative from this starting point. Merger excitement and valuation can run ahead of realised earnings.
- **BTPS and BBKP** show that a recognised niche or a large shareholder is not enough when credit cost, profitability, capital actions, or turnaround execution disappoints.

This is descriptive evidence, not causal proof. A causal claim requires dated earnings, valuation, corporate-action, regulatory, and news-event analysis."""
    ),
    md("## 11. Why some of the steadier risers did well"),
    md(
        """### BNGA — improving quality plus earnings delivery

CIMB Niaga's official highlights show gross NPL improving from **3.46% in 2021 to 1.81% in 2025**, while CASA balances and pre-tax income increased. That combination—better asset quality, growing inexpensive deposits, earnings delivery, and dividends—can support both book-value growth and valuation rerating. It is more persuasive than price momentum alone. [CIMB Niaga financial highlights](https://investor.cimbniaga.co.id/fn_highlights.html).

### NISP — multi-year efficiency and franchise improvement

OCBC's disclosed series shows ROE rising from **8.33% in 2021 to 12.25% in 2025**, BOPO improving from **76.50% to 69.63%**, and CASA rising from **50.65% to 57.96%**. Gross NPL remained below 2% in 2025. The stock's five-year steadiness is consistent with gradual profitability, efficiency, funding, and asset-quality improvement—not necessarily rapid loan growth. [OCBC financial information](https://www.ocbc.id/en/tentang-ocbc/hubungan-investor/informasi-keuangan).

### BDMN — rerating from a lower base

Danamon's five-year stock result was strong but less smooth than BNGA/NISP. A foreign strategic shareholder, franchise integration, consumer/automotive exposure through its ecosystem, dividends, and a starting valuation below premium large-bank levels can create rerating potential. This is an interpretation, not proof that any single factor caused the return; validate it against annual reports and historical P/B, ROE, and payout data. [Danamon annual reports](https://www.danamon.co.id/en/tentang-danamon/Informasi-Investor/Annual-and-Sustainability-Reports).

### BMRI and BBNI — large-bank earnings and capital return

Mandiri's 2025 bank-only ROE was **23.2%**, gross NPL **0.96%**, and loans grew **13.4%**, supporting a strong franchise and dividend capacity. BNI's five-year stock return benefited from asset-quality repair and rerating, although its 2025 ROE, NIM, and efficiency softened: disclosed ROE was 12.7%, NIM 3.8%, and cost-to-income 46.5%. That contrast explains why price return must be checked against the current earnings trajectory. Sources: [Mandiri 2025 annual report](https://www.bankmandiri.co.id/documents/20143/571784404/%5BFINAL%2B-%2B2904%5D%2BANNUAL%2BREPORT%2BBMRI%2B2025.pdf/f8ea17e5-d44d-5593-6332-38437caad9f8) and [BNI financial reports](https://bni.co.id/en-us/investors/financial-reports)."""
    ),
    md("## 12. Quality franchises can still give disappointing stock returns"),
    md(
        """BCA illustrates valuation discipline. Its 2025 fundamentals were exceptional: CASA **83.7%**, ROA **3.9%**, ROE **23.3%**, CAR **29.8%**, gross NPL **1.7%**, and LDR **76.8%**. Yet its five-year adjusted-price CAGR in this sample was modest because stock return depends on the price paid, later valuation, and market endpoint—not quality alone. [BCA 2025 annual report](https://www.bca.co.id/-/media/Feature/Report/File/S8/Laporan-Tahunan/2026/20260212-BCA-AR-2025-EN.pdf).

BRI illustrates cycle sensitivity. Its micro and ultra-micro franchise can earn high margins, but smaller borrowers are vulnerable to income and climate shocks. BRI's 2025 disclosures show CASA at **70.89%** and NIM at **6.54%**, but gross NPL at **3.29%**, ROA at **3.26%**, ROE at **16.84%**, and BOPO at **71.50%**. The high margin must be read together with credit cost and operating intensity. [BRI 2025 annual report](https://www.ir-bri.com/newsroom/AnnualReport2025-BBRI-att2_%281%29.pdf).

BSI illustrates the difference between business progress and entry valuation. In 2025, BSI reported assets of Rp456.19 trillion, profit of Rp7.57 trillion, gross NPF of **1.81%**, and ROE of **16.85%**. Those are meaningful post-merger improvements, but an investor who entered when expectations were already very high could still suffer a negative return. [BSI 2025 annual report](https://ir.bankbsi.co.id/misc/AR/AR2025-ID/index.html)."""
    ),
    md("## 13. Why digital and turnaround banks were highly volatile"),
    md(
        """The 2020–2021 digital-bank cycle combined genuine structural change with speculative valuation:

1. Investors capitalised distant customer-growth and ecosystem expectations before profitability was proven.
2. Small public floats and corporate actions amplified price moves.
3. Rights issues increased capital but could dilute existing shareholders.
4. Rapid unsecured or digital credit created unseasoned asset-quality risk.
5. Rising discount rates reduced the present value of distant profits.
6. When growth, ROE, or ecosystem monetisation lagged expectations, valuation compression overwhelmed operational progress.

Allo Bank's official history records the 2021 takeover, renaming, and a large rights issue; its 2021–2022 reports show the scale of the accompanying share-price cycle. Bank Raya later reported improving 2024 operations—NPL declined to 3.22%, ROE rose to only 1.59%, and profit reached Rp50.89 billion—but a recovering business does not restore an earlier speculative valuation automatically. Bank Neo Commerce likewise reported a 2025 profit turnaround, yet the stock path still reflects prior losses, dilution, risk, and expectations. Sources: [Allo Bank 2021 annual report](https://hanoman.allobank.com/container/media/investor-relation/sub/hvyaqX_BBHI-Annual%20Report%202021.pdf), [Bank Raya 2024 performance](https://bankraya.co.id/articles/news/kinerja-bank-raya-tumbuh-pesat-di-2024-pertumbuhan-berkualitas-bisnis-digital-semakin-kuat-ditopang-optimalisasi-sinergi-dalam-ekosistem-bri-group), and [Bank Neo Commerce 1H2025 results](https://www.bankneocommerce.co.id/en/news/bank-neo-commerce-bbyb-posts-rp276-billion-in-profit-in-the-first-half-of-2025).

The core lesson is:

> A good narrative is not a valuation method, and improving from a weak base is not the same as earning an attractive return on the capital shareholders supplied."""
    ),
    md("## 14. Ten-year context: entry point changes the answer"),
    code(
        """metrics_10y = performance_metrics(history, '2016-09-22', analysis_end).merge(
    metadata[['ticker', 'longName', 'marketCap']], on='ticker', how='left'
)
metrics_10y['full_window'] = metrics_10y['first_date'].le(pd.Timestamp('2016-10-06'))
metrics_10y['comparison_subset'] = (
    metrics_10y['full_window']
    & metrics_10y['marketCap'].ge(5e12)
    & metrics_10y['median_daily_trading_value_idr'].ge(1e9)
    & metrics_10y['zero_return_day_fraction'].lt(0.30)
    & metrics_10y['ticker'].ne('^JKSE')
    & metrics_10y['ticker'].ne('PNLF')
)
ten_year_table = metrics_10y.loc[metrics_10y['comparison_subset']].sort_values('cagr', ascending=False)
ten_year_table[[
    'ticker', 'longName', 'total_return', 'cagr', 'annualized_volatility',
    'maximum_drawdown', 'positive_month_fraction'
]].style.format({
    'total_return': '{:.1%}',
    'cagr': '{:.1%}',
    'annualized_volatility': '{:.1%}',
    'maximum_drawdown': '{:.1%}',
    'positive_month_fraction': '{:.1%}',
})"""
    ),
    md(
        """ARTO can appear at the top of a ten-year CAGR table because its pre-transformation price base was tiny, even though it later lost more than 95% from its peak. It is therefore a high-return/high-path-risk transformation outcome, not a steady compounder.

Among established franchises, the ten-year table gives more weight to BBCA, BMRI, BBRI, BNGA, and BBNI. It also demonstrates why “which rose most?” is incomplete without:

- start and end dates,
- dividends and corporate actions,
- maximum drawdown,
- liquidity and stale prices,
- business-model continuity,
- survivorship and delisting history, and
- starting and ending valuation."""
    ),
    md("## 15. A disciplined bank-analysis worksheet"),
    md(
        """For each bank and each reporting period, record:

1. **Business model:** customer segment, geography, products, ecosystem, controlling shareholder.
2. **Five-year operating trend:** loans, deposits, CASA, NIM, fees, costs, provisions, profit.
3. **Credit vintages:** NPL/NPF, LaR/Stage 2, restructuring, write-offs, recoveries, coverage, cost of credit.
4. **Funding:** deposit concentration, cost, maturity, digital activity, wholesale dependence, LDR/FDR, LCR and NSFR.
5. **Capital:** Tier 1/CET1, total CAR, risk-weighted-asset growth, rights issues, and dividend capacity.
6. **Profit quality:** recurring versus treasury/recovery/one-off income; normalised ROA and ROE.
7. **Governance:** related-party exposure, controlling-owner actions, audit and regulatory events.
8. **Valuation:** P/B versus sustainable ROE; P/E versus normalised earnings; dividend yield; downside case.
9. **Market structure:** free float, median trading value, zero-return days, bid–ask spread, index ownership.
10. **Thesis and disconfirmation:** what must happen, what could falsify it, and what valuation already assumes.

### Minimum comparison rule

Never compare only one year's ROE or one day's P/B. Use at least a full credit cycle where possible, reconcile bank-only and consolidated figures, and use the same dates and definitions across banks.

### Red flags

- Loan growth far above peers without matching deposits, capital, or experienced staff
- CASA “growth” accompanied by unusually high promotional rates
- Falling NPL but rising LaR, Stage 2, restructuring, or write-offs
- High NIM with deteriorating cost of credit
- High ROE created by low capital or one-off gains
- Repeated rights issues without a credible path to adequate ROE
- Large related-party or single-sector concentration
- Thin trading that makes the chart look falsely stable
- Stock-price excitement unsupported by book-value and per-share earnings growth"""
    ),
    md(
        """## 16. Bottom line

Indonesia's banking system currently combines strong aggregate capital, profitability, liquidity, and credit growth with meaningful variation among individual banks. The durable economic advantages are cheap and sticky funding, disciplined underwriting, scalable transactions, sound governance, and returns on equity above the cost of capital. The recurring dangers are leverage, delayed credit losses, funding pressure, policy exposure, dilution, and paying too much for a good story.

For the specific five-year stock window studied here, BNGA and NISP produced the best combination of rise and steadiness; BDMN, BMRI, and BBNI also rose strongly with more volatility. Digital/turnaround names produced the deepest drawdowns. Over ten years, established large-bank compounders become more visible, while ARTO demonstrates how a spectacular transformation return can coexist with catastrophic peak-to-trough risk.

The correct conclusion is not “buy the recent winner.” It is:

> Identify a sound bank, understand the credit and funding cycle, estimate sustainable ROE, pay a valuation that leaves room for error, and size the position so a severe drawdown does not threaten the family plan.

### Data limitations

- Yahoo's current industry membership introduces survivorship bias.
- Adjusted prices are a provider series, not an official IDX total-return index.
- Historical prices do not include taxes, spreads, slippage, or investor-specific cash-flow timing.
- Thin trading can suppress measured volatility and distort apparent stability.
- Current market capitalisation is combined with historical returns only for filtering; it was not known at the historical start date.
- Explanations of stock performance are evidence-based interpretations, not causal decompositions.
- Official issuer ratios can differ between bank-only and consolidated scope.
- All current facts and valuations require refresh before an investment decision."""
    ),
    md(
        """## Sources and reproducible refresh

Principal sources are linked in the relevant sections. The market-data workflow is:

```bash
PYTHONNOUSERSITE=1 uv run --isolated --with 'numpy<2' --with pandas --with yfinance \
  python scripts/fetch_yahoo_bank_history.py --as-of YYYY-MM-DD --years 10

python3 scripts/build_banking_sector_overview_notebook.py
```

The bulk history and manifest remain under `private/market_data/yahoo/`. Rebuild and execute the notebook only after the dated metadata and bank-history snapshots have been refreshed."""
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
