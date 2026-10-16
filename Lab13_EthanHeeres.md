# Lab 13 — Portfolio Mandate Defense
Ethan Heeres

## D — The question

Which of these portfolios does the Meridian Foundation's mandate permit — and what must the CIO answer before anyone optimizes?

A passes every rule the checker tests. B fails the reserve, liquidity, and issuer concentration rules. C fails the reserve rule. Passing these checks does not establish that A is fully suitable for the client. The CIO still needs to clarify the calendar-year loss statement and identify what the pilot should optimize.

## R — Statement types

| Statement | Type | Reason |
|---|---|---|
| S1 | Hard constraint | The seven-year horizon and annual rebalancing requirement set the planning period and required rebalancing schedule. |
| S2 | Objective | CPI + 4% annually, net of costs over rolling five-year periods, describes the return the client wants. |
| S3 | Hard constraint | The reserve must cover four quarterly payouts of $0.75 million using eligible holdings. |
| S4 | Preference | The 60/40 benchmark provides a comparison standard; it does not require the portfolio to hold exactly those weights. |
| S5 | Hard constraint | Borrowing, short sales, and derivatives are prohibited. |
| S6 | Hard constraint | Securities from the same company must total no more than 8%, with the stated exemptions. |
| S7 | Hard constraint | Annual turnover cannot exceed 25% unless the committee approves it. |
| S8 | Hard constraint | At least 90% of the portfolio must be redeemable within five business days. |
| S9 | Unverifiable promise | The loss statement lacks an operational risk measure and breach rule, and the holdings alone cannot guarantee future losses stay below 10%. |
| S10 | Missing | No additional preferences are specified, and the pilot's optimization objective has not been chosen. |

S2 provides a performance target, but S10 leaves open how to choose among portfolios. A target does not tell the computer whether to minimize risk, maximize expected return, or optimize something else.

## I — The checker

The checker uses the holdings, candidate weights, and policy inputs in `mandate.py`. It calculates the reserve minimum and checks total weights, long-only weights, reserve eligibility, liquidity, and issuer concentration.

Cash, U.S. Treasury securities, and diversified funds are exempt from the issuer limit. Acme's bonds and stock count together.

The calendar-year loss statement always prints “requires CIO clarification” and is not tested.

Run command: `python mandate.py`

## V — Verification

The required reserve is:

4 × $0.75 million = $3 million

$3 million ÷ $100 million × 100 = 3.0%

| Rule | A | B | C |
|---|---|---|---|
| Weights sum to 100 | 100.0 pass | 100.0 pass | 100.0 pass |
| Long-only: lowest weight | 0.0 pass | 0.0 pass | 0.0 pass |
| Reserve ≥ 3.0% | 14.0 pass | 1.0 FAIL | 2.0 FAIL |
| Redeemable in five days ≥ 90% | 100.0 pass | 85.0 FAIL | 100.0 pass |
| Largest single company ≤ 8% | 0.0 pass | 9.0 FAIL | 8.0 pass |
| Calendar-year loss | Requires CIO clarification | Requires CIO clarification | Requires CIO clarification |
| Verdict | Passes every checkable rule | Fails 3 rules | Fails 1 rule |

A's reserve includes cash, Treasury bills, and the Treasury 10-year note because all three are reserve-eligible in the supplied table. Reserve eligibility does not mean the 10-year note has a stable market value.

B's Acme exposure is 5% in bonds plus 4% in stock, totaling 9%. C's 8% Acme position passes because the rule allows exactly 8%.

### Negative-weight probe

Changing A's cash to −2% and global equity fund to 64% produces:

| Rule | Result |
|---|---|
| Weights sum to 100 | 100.0 pass |
| Long-only: lowest weight | −2.0 FAIL |
| Reserve ≥ 3.0% | 10.0 pass |
| Redeemable in five days ≥ 90% | 100.0 pass |
| Largest single company ≤ 8% | 0.0 pass |
| Verdict | Fails 1 rule |

Only long-only fails. The final code restores A's cash to 2% and global equity fund to 60%.

## E — Attack the checker

Candidate D holds 3% cash and 97% in the global equity index fund, with zero in every other holding.

| Rule | D |
|---|---|
| Weights sum to 100 | 100.0 pass |
| Long-only: lowest weight | 0.0 pass |
| Reserve ≥ 3.0% | 3.0 pass |
| Redeemable in five days ≥ 90% | 100.0 pass |
| Largest single company ≤ 8% | 0.0 pass |
| Calendar-year loss | Requires CIO clarification |
| Verdict | Passes every checkable rule |

### Two-sentence judgment

The objection holds because a portfolio with 97% in global equities could lose more than 10% in a calendar year despite passing every check. S9 gives the CIO a reason to reject it pending clarification, but it does not provide a defined loss test that the checker can apply.

### Sceptical colleague role

I would cite S9 against this portfolio. The diversified-fund exemption removes the issuer concentration problem, but it does not remove equity market risk or establish that the portfolio meets the client's loss concern.

## Your question for the CIO

**Question:** What single objective should the pilot optimize among portfolios that satisfy the clarified mandate?

**Answer that would change the portfolio:** If the CIO says “minimize volatility while targeting CPI + 4% net,” I would evaluate lower equity exposure and more short-term government securities than I would under a maximum-expected-return objective. I would still need to check whether the return target is feasible under the agreed constraints.

S10 makes this question necessary. S9 also needs a defined risk measure and breach response before the loss concern can become an operational rule.

## Investment policy statement — Learn on your own

### 1. What is it?

An investment policy statement is a written policy for managing a specific investor's assets. The CFA Institute reading organizes it around scope and purpose, governance, investment/return/risk objectives, and risk management. It should fit the investor's circumstances rather than copy a generic set of limits (CFA Institute, 2010, pp. 1–3).

### 2. How does it work?

Objectives describe what the portfolio is trying to achieve. Constraints define what it is allowed to do. Governance identifies who approves the policy, implements it, monitors results, and authorizes changes. Risk management defines consistent measures, reporting responsibilities, and how rebalancing or breaches are handled (CFA Institute, 2010, pp. 4–7, 16–17).

### 3. Mapping S1–S10

| IPS component | Meridian statements |
|---|---|
| Time horizon and rebalancing | S1 |
| Return objective | S2 |
| Payout needs and reserve requirement | S3 |
| Performance benchmark | S4 |
| Permitted investment methods | S5 |
| Issuer concentration | S6 |
| Turnover and approval process | S7 |
| Liquidity requirement | S8 |
| Unresolved loss concern | S9 |
| Unspecified preferences and missing optimization objective | S10 |

### 4. What the reading adds to this case

S1–S10 are the beginning of an IPS, not a complete one. S7 names committee approval for turnover exceptions, but the case does not fully assign responsibility for approving the IPS, monitoring compliance, choosing assumptions, reporting results, or reviewing the policy. Those responsibilities need to be specified rather than assumed.

The reading also separates a performance benchmark from a policy portfolio with required allocation ranges. S4 names a benchmark but supplies no mandatory asset-class ranges. That is why I use the assignment's preference category for S4 without treating 60/40 as a required allocation (CFA Institute, 2010, pp. 8–10).

S9 needs both a defined risk measure and an action when its threshold is breached. Liquidity, return volatility, and the ability to meet payouts are different concerns. A complete IPS needs reporting and rebalancing procedures, not just a statement that losses must stay below a number (CFA Institute, 2010, pp. 10–12, 16–17).

## Reflect

### 1. Why can a portfolio pass every checkable rule and still be wrong for this client?

The checker evaluates only the rules that can be calculated from the supplied holdings and weights. It does not establish that the portfolio can achieve CPI + 4%, meet the CIO's loss expectations, or follow the annual rebalancing and turnover rules over time. D shows that a liquid portfolio can pass every holdings check while still exposing the client to substantial market risk.

### 2. Which statement type was I least sure of?

I was least sure about S4 because a precise 60/40 benchmark looks like an allocation requirement. I classified it as a preference because the CIO named it as a benchmark, without requiring the actual portfolio to use those weights.

## After this lab — Proposed Project 2 mandate: Oracle

### Intended user and decision

The intended user is a fictional individual investor with a diversified portfolio who wants to evaluate an Oracle (ORCL) allocation. The committee decision will be whether to pilot, allocate to, rebalance, or reject the proposed process after comparing it with transparent baselines, costs, and risk.

The settings below are proposed course-project assumptions, not instructions from an actual client or numbers required by the professor. They must be reviewed before the rule is frozen. ORCL is the research focus; it is not the entire portfolio.

### Investment universe

| Holding | Role |
|---|---|
| Oracle common stock (ORCL) | Individual-company allocation being evaluated |
| Vanguard Total World Stock ETF (VT) | Diversified global equity exposure |
| Vanguard Total Bond Market ETF (BND) | Broad U.S. investment-grade bond-market exposure |
| State Street SPDR Bloomberg 1-3 Month T-Bill ETF (BIL) | Short-term Treasury-bill exposure and the project's reserve proxy |
| Uninvested cash | Settlement and reserve balance; include it in total weights |

The fund descriptions are supported by the providers' [VT page](https://investor.vanguard.com/investment-products/etfs/profile/vt), [BND page](https://investor.vanguard.com/investment-products/etfs/profile/bnd), and [BIL page](https://www.ssga.com/us/en/intermediary/etfs/state-street-spdr-bloomberg-1-3-month-t-bill-etf-bil). Treating BIL as reserve-eligible is an explicit choice for this proposed mandate, not a claim that an ETF is cash or has a guaranteed value.

### Objective, constraints, and suitability

| Item | Proposed rule |
|---|---|
| Objective | Maximize estimated annual total return, net of trading costs, within the risk and portfolio limits. Use 6% expected annual nominal net return as the initial feasibility target. This is a target, not a promised realized return. |
| Horizon | Five years, with no planned withdrawals from this investment pool during that period. |
| Rebalancing | Review holdings monthly and rebalance annually. Set the exact observation and execution dates in the frozen rule card before testing. A policy breach may require an approved correction outside the annual schedule. |
| Benchmark | A simple portfolio of 50% VT, 40% BND, and 10% BIL, rebalanced annually. Compare it over identical dates and show its gross and net returns under the same cost convention. |
| Risk measure | Estimated annualized portfolio volatility: square root of 12 times the monthly covariance quadratic form, sqrt(12 × w'Σw), with weights entered as decimals. Start with a 60-month estimation window. |
| Risk limit | Estimated annualized volatility at most 15% at a proposed allocation. This is a model-based screen, not a guarantee about future losses. |
| Loss tolerance and response | Monitor drawdown using net portfolio wealth. Drawdown is 1 minus current wealth divided by its previous running peak. A drawdown of 15% or more triggers a pause in new risk-taking and a review. The threshold is a response rule; prices can move beyond it before action is possible. |
| Weights | Every weight must be nonnegative, and all positions, including cash, must sum to 100%. |
| Reserve | At least 5% of portfolio value must be in BIL or uninvested cash. |
| Liquidity | At least 90% must be convertible to available cash within five business days under documented normal-market assumptions. Include sale and settlement timing; a quoted market price alone does not prove this condition. |
| Leverage and shorting | No borrowing, short sales, direct derivatives, leveraged funds, or inverse funds. |
| Concentration | Direct exposure to any individual company, including ORCL, cannot exceed 10%. Diversified funds are exempt from this direct-issuer cap; disclose indirect company exposure through funds separately. |
| Turnover | Rolling 12-month one-way turnover cannot exceed 25% without recorded approval. At each trade date, measure turnover as half the sum of absolute changes from the actual pre-trade weights, including cash, and sum those values over 12 months. Document initial funding separately. |
| Costs | Start with 10 basis points per dollar bought or sold in securities. Charge each traded side, state how cash is treated, and report gross and net results. Stress the cost input before recommending the process. |
| Suitability | This scenario assumes the investor has emergency savings outside the portfolio, can leave these funds invested for five years, accepts market losses, and does not require principal protection or near-term income. Taxes are outside the initial model and must be disclosed as a limitation. |

The initial ORCL action range is 0%–10%, including the option to hold none. This is a permitted range, not a calculated recommendation. No portfolio has yet been shown to meet the proposed return and volatility settings. If no feasible allocation exists, report that result and return to the mandate instead of silently relaxing a limit.

Check the weight, reserve, concentration, liquidity, and estimated-risk rules at each monthly review and before proposed trades. Show a failure and pause new risk-taking when a rule is breached, required data are missing, or the proposed allocation is infeasible. Record any approved exception and its effect on costs and turnover.

### Governance and review

For this fictional project, the investor approves the mandate, its numerical limits, and exceptions. I act as the analyst responsible for the data, assumptions, calculations, monthly compliance report, and recommendation. The committee evaluates the evidence and the proposed action; the model cannot grant itself an exception.

Review the IPS annually and whenever cash needs or risk capacity materially change. Record each change and the reason in the repository. After the rule is frozen, a material change creates a new hypothesis and requires new or prospective evidence; it must not overwrite the original holdout. No client approval or final committee decision is claimed at this stage.

### One question for the client

Will you need any of this investment money for a major expense within the next five years?

If yes, I would separate the amount needed for that expense before deciding how much of the remaining portfolio to allocate to ORCL. The horizon, reserve requirement, and risk limits would need to reflect that withdrawal.

### Carrying the mandate into Project 2

The next labs will build the engine and a locally runnable Python web app, such as Streamlit. The current `mandate.py` checks the assigned Meridian case only; it is not yet the Project 2 application.

- Compare equal-weight and inverse-volatility baselines before the constrained process. Show any mandate violations rather than calling an invalid baseline investable. For example, equal weight across ORCL, VT, BND, and BIL gives ORCL 25%, which fails the proposed 10% limit. Document any constraint adjustment and apply consistent timing and cost assumptions.
- Use total returns including distributions. Document the sample and as-of dates, units, missing observations, revisions, and transformations. Establish signal availability and trading time before using a signal.
- Record every signal, lag, threshold, universe, and rule tried. Freeze the selected rule before running a genuinely untouched holdout, then report gross and net results and a placebo or falsification test. No signal or holdout result has been produced in this lab.
- Keep the data, point-in-time rule, official rule card, and holdout locked. Bound the live controls for objective return, reserve minimum, estimation window, signal lag, and trading costs. Label control-driven scenarios separately so they do not overwrite the locked holdout result.
- Test estimates, windows, costs, and constraints. Pause or reject the process if its net holdout evidence fails the precommitted decision rule or if it cannot satisfy the mandate. Define that decision rule before seeing the holdout.
- Complete the required human-authored, AI-off changed-input prediction before its run, and preserve the timestamp or commit. Add the cold-run check, visible-output check, highest-risk counterexample, and an independently checked AI output as the system is built.
- The final Project 2 submission will also need the runnable repository, README, decision memo, validation/AI-use file, three videos with corrected transcripts, and manifest. The README, memo, and each video must open with the required AI-use and education-not-investment-advice statements. Video 3 must begin its substantive content with the live app demonstration.

## Code quiz

Question: What would go wrong if `company_weights[issuer] = company_weights.get(issuer, 0) + weight` were replaced with `company_weights[issuer] = weight` when checking candidate B?

Answer after discussion: Using `= weight` would replace the saved 5% in Acme bonds with the 4% in Acme stock instead of adding them together. The checker would report 4% and incorrectly pass the 8% issuer limit, even though the total is 9%. The original line adds both holdings together, so B correctly fails this rule.

## Reading used

CFA Institute. (2010). *Elements of an investment policy statement for institutional investors*. May 2010. ISBN 978-0-938367-32-1. Supplied course reading: `investment-policy-statement-institutional-investors.pdf`.
