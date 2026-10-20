# Lab 14 — Portfolio Baselines
Ethan Heeres

## D — Question
What does each simple portfolio earn and risk, and does any meet Meridian's mandate?

The benchmark meets the 6.5% estimated return target, but fails the 3% reserve requirement. Equal weight and inverse volatility meet the reserve requirement, but miss the return target. None of the three meets both.

## R — Inputs
Course-authored training values, **not market estimates**. CPI is estimated at 2.5%, making the CPI + 4% objective **6.5%**.

| Asset | Expected return | Volatility |
|---|---:|---:|
| Treasury bills | 3.5% | 0.5% |
| Treasury 10-year note | 4.3% | 7.0% |
| Investment-grade bond fund | 5.0% | 6.0% |
| Global equity index fund | 8.0% | 16.0% |

The complete correlation table is at the top of `portfolio.py`; bills and the 10-year note count toward Meridian's reserve.

## I — Implementation
`portfolio.py` computes covariance as correlation × each asset's volatility. Separate, reusable functions calculate portfolio weights, expected return, variance, volatility, reserve percentage, and whether expected return meets the objective. Uses Python's standard library only.

**Run:** `python portfolio.py`. Run `python mandate.py` for candidates A–E.

## V — Verification

| Portfolio | Bills / 10yr / IG / Equity weights (%) | Return | Volatility | Reserve | Meets 6.5%? |
|---|---|---:|---:|---:|---|
| Benchmark | 0.0 / 0.0 / 40.0 / 60.0 | 6.80% | 10.46% | 0.0% | Yes |
| Equal weight | 25.0 / 25.0 / 25.0 / 25.0 | 5.20% | 5.21% | 50.0% | No |
| Inverse volatility | 84.3 / 6.0 / 7.0 / 2.6 | 3.77% | 1.05% | 90.3% | No |

**Tests run:** Setting both IG/equity correlations to 0.50 raises benchmark volatility to 11.00%. Setting both to 1.3 refuses execution with a clear correlation error. Asymmetric inputs also refuse execution. The original 0.25 correlations are restored. `mandate.py` candidate E is 40% IG and 60% equity; it fails the reserve test with 0.0% versus 3.0% required, but passes the other checkable holdings rules.

## Diversification — Learn on my own
**What is it?** Spreading investments across assets rather than relying on just one.

**How does it work?** Assets are not perfectly correlated, so one asset's losses can partly offset another's gains. This reduces diversifiable risk, but not all market risk. Correlations can also change.

**Hand calculation:**
- Expected return = 0.40 × 5% + 0.60 × 8% = **6.80%**.
- Bond/equity covariance = 0.25 × 0.06 × 0.16 = **0.0024**.
- Variance = (0.40² × 0.06²) + (0.60² × 0.16²) + (2 × 0.40 × 0.60 × 0.0024) = **0.010944**.
- Volatility = √0.010944 = **10.46%**. Ignoring covariance incorrectly produces 9.90%.

## Reflect — Discussion prompts to review with my partner
**Why does inverse volatility pile into bills?** Bills have only 0.5% volatility. Dividing 1 by that small number gives bills the biggest relative weight, greatly lowering risk but also expected return.

**Which baseline to show the CIO first?** I would show the client's 60/40 benchmark first as a clear comparison: it meets the return target in the exercise but violates the reserve rule, so it is not investable unchanged.

## Before Thursday — Provisional fund universe
These **funds** support the app's fund-only universe; the Project 2 mandate in Lab 13 continues to focus on Oracle as an individual-stock allocation decision.

| Ticker | Fund name | Role |
|---|---|---|
| BIL | SPDR Bloomberg 1-3 Month T-Bill ETF | Cash / Treasury-bill reserve proxy |
| IEF | iShares 7-10 Year Treasury Bond ETF | Government bonds |
| BND | Vanguard Total Bond Market ETF | Broad investment-grade fixed income |
| VT | Vanguard Total World Stock ETF | Diversified global equity |

Fund descriptions: [BIL](https://www.ssga.com/us/en/intermediary/etfs/state-street-spdr-bloomberg-1-3-month-t-bill-etf-bil), [IEF](https://www.ishares.com/us/products/239456/ishares-710-year-treasury-bond-etf), [BND](https://investor.vanguard.com/investment-products/etfs/profile/bnd), [VT](https://investor.vanguard.com/investment-products/etfs/profile/vt).

**Prices pending, not fabricated:** Source to use: Yahoo Finance → Historical Data → Monthly → **Adj Close**. Obtain five years of actual monthly adjusted close, date first, oldest to newest, and record the **actual retrieval date** when collected. `prices.csv` has not yet been created. Existing Project 2 benchmark remains 50% VT / 40% BND / 10% BIL pending an explicit mandate revision.
