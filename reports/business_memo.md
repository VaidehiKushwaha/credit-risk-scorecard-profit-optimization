# Business Decision Memo: Credit Card Approval Strategy

**To:** Head of Credit Risk  
**From:** Vaidehi Kushwaha  
**Date:** 21 November 2026  
**Decision:** Retain the WOE scorecard as champion; run LightGBM as a controlled challenger.

## Recommendation

Use the WOE logistic scorecard as the production champion, with an illustrative approval rule of **PD ≤ 14.3%** (credit score **≥ 539**). The break-even threshold is based on assumed revenue of NT$6,000, LGD of 70%, and estimated EAD of NT$51,221. These are project assumptions, not validated issuer economics.

On the held-out test set, the scorecard approves **54.7%** of applicants, with a **10.5%** default rate among approved applicants and realized profit of **NT$876 per applicant**. Approving everyone produces a loss of **NT$3,259 per applicant**. The scorecard's paired gain over approve-all is **NT$4,136 per applicant** (95% bootstrap CI: **NT$3,857–4,437**). Across the 9,000 test observations, losses avoided are NT$52.85m, offset by NT$15.63m in revenue foregone.

The accuracy-based cutoff produces a loss of about NT$996 per applicant, so accuracy is not an appropriate decision objective here.

## Challenger evidence

At each model's own break-even cutoff, LightGBM earns **NT$1,076** per applicant versus **NT$876** for the scorecard: a point-estimate uplift of **NT$199.77**. The paired-bootstrap mean uplift is **NT$201.10** (95% CI: **NT$87–313**). At the same 54.7% approval rate, LightGBM's uplift is **NT$172.07** per applicant. It outperformed the scorecard in all 25 tested revenue/LGD scenarios. This supports a challenger pilot, not immediate replacement.

For scale only, applying test-set estimates to one million comparable applicants implies about **NT$876m** scorecard profit and **NT$200m** additional LightGBM uplift (bootstrap interval approximately **NT$87m–313m**). These are extrapolations, not forecasts.

## Economics, sensitivity and limitations

The assumed break-even revenue for approving everyone is approximately **NT$10,183** per customer. The largest fixed-cutoff regret in the tested revenue/LGD grid is about **NT$1,181 per applicant**. Revenue is the most influential one-at-a-time assumption: a 50% increase changes profit by about +NT$1,612 per applicant, while a 50% decrease changes it by about −NT$812.

The calibration stress test shows profit of NT$801 at a 0.8 PD multiplier and NT$942 at 1.25, compared with NT$876 at the base multiplier. Thus, moderate ±20–25% PD stress changes profit by roughly NT$66–75 per applicant; larger stress (0.6 or 1.5–2.0) reduces profit more materially. The small peak at 1.25 is not a reason to change the cutoff.

Expected scorecard profit (NT$1,109) exceeds realized test profit (NT$876); the realized-profit bootstrap 95% interval is NT$674–1,065. The expected value is slightly above that interval, so the difference should be investigated rather than described as fully consistent. The data cover one issuer and a short 2005 observation window; there is no out-of-time validation. Economic inputs are illustrative. Reject inference, applicant behaviour changes, population drift and model complexity also limit deployment conclusions.

## Key risks and controls

| Risk | Control |
|---|---|
| Revenue, LGD or EAD assumptions are wrong | Finance/Risk validate inputs; recompute break-even PD and cutoff quarterly and when inputs move >20%. |
| Calibration or population drift | Monthly calibration and PSI/CSI monitoring; recalibrate or rebuild when thresholds are breached. |
| Performance decay | Quarterly Gini/KS review; investigate a Gini fall greater than 0.05. |
| Fairness disparity | Monthly approval and calibration comparisons; escalate approval ratios below 0.80 or calibration gaps above 0.02. |
| Reject inference and behavioural response | Treat results as historical-policy estimates; monitor outcomes and attrition in a controlled pilot. |
| Short historical window / no OOT test | Require prospective pilot evidence before production expansion. |
| Challenger complexity | Keep scorecard as champion; require explainability, governance and independent validation for LightGBM. |

Fairness checks at the selected cutoff show approval-rate ratios of **0.957 (SEX), 0.969 (MARRIAGE), and 0.880 (AGE_BAND)** for the scorecard; all exceed the 0.80 screening threshold, but age is the lowest and warrants monitoring. These are screening diagnostics, not proof of fairness or legal compliance.

## Pilot and monitoring recommendation

Run a **3–6 month randomized champion–challenger pilot** among eligible applicants, stratified by risk and credit-limit bands. Pre-register the analysis; compare realized profit per applicant using paired/stratified bootstrap intervals; monitor approved-customer bad rate, approval rate, attrition, complaints and fairness. Examine applicants for whom the models disagree. Do not promote LightGBM unless the paired uplift confidence interval excludes zero, point uplift is at least **NT$100 per applicant**, and all guardrails pass.

The observed paired-difference standard deviation is about **NT$9,524**. Approximate sample sizes are **142,410 per arm** for NT$100 detectable uplift, **35,603 per arm** for NT$200, and **15,823 per arm** for NT$300 (planning approximation; confirm with a formal power calculation).

| Metric | Frequency | Trigger | Action |
|---|---|---|---|
| PSI / CSI | Monthly | 0.10 warning; 0.25 action | Investigate shift; recalibrate or rebuild |
| Mean predicted vs. observed default | Monthly, on matured outcomes | Gap > 0.01 | Recalibrate and investigate segments |
| Gini / KS | Quarterly | Gini drop > 0.05 | Diagnose and validate rebuild |
| Approval rate / approved bad rate | Monthly | Outside agreed operating band | Review cutoff and policy |
| Realized vs. expected profit | Quarterly | Outside expected confidence range | Recheck revenue, LGD and EAD |
| Fairness approval ratio / calibration gap | Monthly | Ratio < 0.80 or gap > 0.02 | Escalate to compliance and risk governance |
| Revenue, LGD, EAD | Quarterly | Any input moves > 20% | Recompute break-even PD and cutoff |

**Decision requested:** Approve the scorecard as the analytical champion and authorize a governed LightGBM challenger pilot, subject to Finance validation of the economic assumptions and Risk/Compliance approval of guardrails.

**Supporting project outputs:** `reports/strategy_comparison_test.csv`, `reports/sensitivity_grid.csv`, `reports/model_value_vs_revenue.csv`, `reports/scenario_B_customer_specific.csv`, and `reports/test_results.csv`.
