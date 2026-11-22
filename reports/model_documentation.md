# Model Documentation — Credit Risk Scorecard and Profit Optimisation

**Model:** Behavioural Credit Risk Scorecard and C3 Monotonic LightGBM Challenger  
**Version:** v1.0 | **Date:** 22 November 2026 | **Author:** Vaidehi Kushwaha  
**Status:** Portfolio project — not approved for production use

## 1. Objective and scope

This project estimates the probability that an existing credit-card customer defaults in the following month. It is a behavioural credit-risk exercise, not an application scorecard for a new-to-bank applicant. The decision explored is whether to extend or maintain credit (approve) or restrict credit (decline) for a one-period horizon.

The intended use is academic and portfolio demonstration of feature engineering, scorecard development, challenger modelling, validation, fairness screening and illustrative profit optimisation. It is not approved for real lending, credit-limit assignment or customer rejection. Operational use would require current portfolio data, independent validation, legal and compliance review, governance approval and prospective testing.

Two models are compared: a WOE logistic-regression scorecard (champion candidate, selected for interpretability) and C3 Monotonic LightGBM (challenger, with stronger overall predictive metrics).

## 2. Data and definitions

### 2.1 Source and observation window

The source is the UCI Default of Credit Card Clients dataset: 30,000 Taiwan credit-card customers, with account and repayment information from April through September 2005. The customer identifier (ID) was removed, leaving 24 columns. The target DEFAULT indicates default payment in the following month (October under the project’s decision-date interpretation). The observation window is six months and the outcome horizon is one month.

### 2.2 Split and test protocol

A stratified 70:30 train/test split was used with random seed 42: 21,000 training and 9,000 test customers. The validation plan specifies 2,000 paired bootstrap resamples, seed 2026, and percentile 95% confidence intervals. Models were scored on the held-out test set and subsequent test analyses used saved predictions. Multiple analyses were nevertheless performed on the same holdout, so it is not a substitute for out-of-time validation.

### 2.3 Audit findings and treatment

The audit found no missing values and no customer rows were deleted. Seventy rows had identical feature values after excluding ID; these were retained because different IDs do not prove accidental duplication. A total of 795 dormant accounts (all six bills and payments equal to zero) were retained. The 468 undocumented EDUCATION codes (0, 5, 6) were merged into category 4 (“Others”); MARRIAGE code 0 was merged into category 3 (“Others”). There were 3,932 negative bill entries across six bill columns (1,930 customers), retained as potential credit balances; no negative payment amounts were found. Bills above credit limit and extreme monetary values were retained. A total of 8,063 month-to-month repayment-status jumps greater than one were retained. Another 1,238 records had positive current delay status with a non-positive previous-month bill; these were retained and flagged. PAY codes −2 and 0 are not fully documented. Only 32.73% of PAY_0 = −2 records had BILL_AMT1 ≤ 0, so “no consumption” is not confirmed.

ID was excluded from predictors and DEFAULT was used only as the target. Interpretation of repayment codes remains a limitation.

## 3. Methodology

### 3.1 Feature engineering

Approximately 48 engineered candidate features cover delinquency, utilisation, payment behaviour, bill dynamics and customer profile. Examples include delay recency and severity, monthly late counts, utilisation levels and trends, payment-to-bill ratios, bill trends and dormant-account indicators. Definitions, formulas, caps/floors and missing handling are documented in reports/feature_dictionary.md. Expected feature directions are hypotheses, not causal claims.

### 3.2 WOE scorecard

The scorecard uses nine selected behavioural predictors: avg_delay, delay_trend, n_revolving, log_limit, pay_amt_avg, bill_avg_to_limit, util_trend, util_latest and n_bill_increases. Backward elimination reduced 23 WOE-transformed predictors to nine. All retained coefficients were negative and significant at the 5% level. McFadden pseudo-R² changed from 0.1735 to 0.1727. L1 regularisation selected 17 predictors, including all nine retained variables. VIF values ranged from 1.438 to 2.969. The highest final-feature IV was 0.9125 for avg_delay. Score scaling uses base score 600, base odds 50:1 and 20 points to double the odds (PDO). Bin-level points are in reports/scorecard_points.csv.

### 3.3 LightGBM challenger

C1, C2 and C3 LightGBM models were evaluated. C3 applies monotonic constraints to selected features and uses 48 engineered inputs. Five-fold nested CV outer AUC mean was 0.7907 (SD 0.0096), and outer Gini mean was 0.5814 (SD 0.0193). SHAP mean absolute values were used for global interpretation, not causal inference. Leading features were months since most recent late payment, latest delay, maximum delay, average delay, average bill and average payment amount. Original uncalibrated probabilities were retained because Platt and isotonic alternatives did not provide a meaningful overall improvement.

### 3.4 Exclusions and fairness rationale

SEX and MARRIAGE were excluded as direct model inputs. Age was tested in scorecard selection; adding it changed mean CV Gini only from 0.5442 to 0.5443, so it was excluded from the final scorecard. The 48 model features predicted SEX with cross-validated AUC 0.615 and married/not-married status with AUC 0.646, indicating potential proxy information.

## 4. Validation results

Development results and locked-test results are reported separately.

| Model / stage | AUC | Gini | KS | Brier |
|---|---:|---:|---:|---:|
| WOE scorecard — 5-fold CV | 0.7720 | 0.5439 | 0.4248 | 0.1388 |
| WOE scorecard — test | 0.7588 | 0.5176 | 0.4034 | 0.1423 |
| C3 Monotonic LightGBM — 5-fold CV | 0.7896 | 0.5792 | 0.4382 | 0.1327 |
| C3 Monotonic LightGBM — test | 0.7807 | 0.5614 | 0.4319 | 0.1351 |

Test-minus-CV changes: scorecard Gini −0.0263, KS −0.0215, Brier +0.0035; C3 Gini −0.0178, KS −0.0063, Brier +0.0024.

Test 95% bootstrap intervals: scorecard Gini [0.4941, 0.5434], KS [0.3847, 0.4304], Brier [0.1378, 0.1471]; C3 Gini [0.5381, 0.5847], KS [0.4103, 0.4555], Brier [0.1305, 0.1399]. The paired test Gini improvement for C3 over the scorecard was 0.0438 (95% CI [0.0343, 0.0539]). Both models exceeded the validation-plan KS threshold of 0.35. CV top-decile default capture was 29.26% for the scorecard, 31.95% for C3 and 32.19% for C2. C3 led overall AUC, Gini, KS and Brier among the four Step 7 models. CV and test stages must not be conflated.

## 5. Calibration, stability and fairness

**Calibration:** scorecard mean predicted PD 0.22024 vs actual default rate 0.22122 (absolute gap 0.00098; slope 0.9305); C3 mean PD 0.22059 vs actual 0.22122 (gap 0.00064; slope 0.9655). Both satisfy planned gap <0.01 and slope 0.8–1.2 criteria. Original probabilities were retained.

**Stability:** train–test score PSI 0.000539; maximum scorecard variable CSI 0.000779. A hypothetical higher-utilisation weighting stress produced PSI 0.0262, mean PD 0.2385, actual rate 0.2410 and Gini 0.4723 vs base 0.5176. This is a simulation, not observed drift.

**Fairness:** at the economic break-even policy, scorecard approval-rate ratios were 0.957 for SEX, 0.969 for MARRIAGE and 0.880 for AGE_BAND. All exceed the 0.80 screen, but age was lowest and requires monitoring. An earlier fairness assessment at a different 75th-percentile OOF policy reported minimum age ratios 0.9206 scorecard and 0.9344 C3; these ratios are not interchangeable. Proxy AUCs were 0.615 for SEX and 0.646 for MARRIAGE. MARRIAGE category 3 had only 111 test customers in the model-card analysis. Passing a ratio screen is not fairness certification.

## 6. Economic analysis

All economics are illustrative, not observed issuer profitability: revenue R = NT$6,000; LGD = 70%; EAD = NT$51,221.26; loss L = NT$35,854.88. Break-even PD p* = R/(R+L) = 14.335%; scorecard cutoff = 538.71 (about 539), approve when PD ≤14.3%.

| Strategy | Approval | Bad rate approved | Profit / customer (NT$) |
|---|---:|---:|---:|
| Approve everyone | 100.0% | 22.1% | −3,259.23 |
| Decline everyone | 0.0% | — | 0.00 |
| Accuracy cutoff (PD ≤ 0.51) | 88.2% | 17.0% | −995.53 |
| Policy: decline if 2+ months late | 89.6% | 16.7% | −882.96 |
| Scorecard at break-even | 54.7% | 10.5% | 876.34 |
| LightGBM at break-even | 50.5% | 9.2% | 1,076.11 |

Scorecard gain over approve-all was NT$4,135.57/customer (paired bootstrap 95% CI approximately NT$3,856.50–4,437.10). Across 9,000 test customers, the decomposition was NT$52.85m losses avoided less NT$15.63m revenue foregone. At each model’s own break-even cutoff, LightGBM point uplift was NT$199.77/customer; paired-bootstrap mean was NT$201.10 (95% CI NT$87.40–313.40). At equal approval of approximately 54.7%, scorecard profit was NT$877.67 and LightGBM profit NT$1,049.74 (uplift NT$172.07). These comparisons are different and should not be conflated. LightGBM won all 25 revenue/LGD scenarios; mean uplift NT$175.30, range NT$30.30–301.70. Maximum fixed-cutoff regret was approximately NT$1,180.60/customer. PD multiplier stress profit was about NT$801 at 0.8×, NT$876 at base and NT$942 at 1.25×; larger stresses reduced profit more materially.

## 7. Limitations

The analysis uses one Taiwan portfolio and a 2005 period, a six-month behaviour window and a one-month outcome. There is no out-of-time validation or reject inference. PAY-code documentation is incomplete. Revenue, LGD and EAD are illustrative assumptions. The same saved test holdout was used for several post-scoring analyses, so the results should not be treated as an independent external validation. Proxy effects may remain despite excluding direct SEX and MARRIAGE inputs; age was the lowest economic-policy approval ratio. Customer behaviour, policy changes and population drift could alter outcomes. LightGBM also carries a greater governance and explainability burden than the scorecard.

## 8. Monitoring plan and governance

The following is a proposed framework for hypothetical deployment, not evidence of live monitoring.

| Metric | Frequency / trigger | Action |
|---|---|---|
| PSI / CSI | Monthly; 0.10 warning, 0.25 action | Investigate shift; recalibrate or rebuild |
| Calibration | Monthly on matured outcomes; gap >0.01 | Recalibrate; inspect segments |
| Gini / KS | Quarterly; Gini drop >0.05 | Diagnose; validate rebuild |
| Approval / approved bad rate | Monthly; outside agreed band | Review cutoff and policy |
| Profit / economics inputs | Quarterly; profit outside CI or R/LGD/EAD move >20% | Recheck assumptions; recompute cutoff |
| Fairness | Monthly; ratio <0.80 or calibration gap >0.02 | Escalate to Risk and Compliance |

Retain the WOE scorecard as champion; LightGBM remains a controlled challenger. Promotion requires the paired profit-uplift confidence interval to exclude zero, point uplift ≥NT$100/customer and all risk, performance and fairness guardrails to pass. A 3–6 month prospective pilot is proposed; formal power calculation and operational approval are required before launch.

## 9. Appendix: reproducibility and supporting artifacts

The train/test split is stratified 70:30 with seed 42. Bootstrap settings are 2,000 paired resamples, seed 2026, with percentile 95% intervals. Supporting artifacts include test_predictions.csv, test_results.csv, model_comparison_step7.csv, nested_cv_results.csv, scorecard_points.csv, final_feature_iv.csv, shap_feature_importance.csv, strategy_comparison_test.csv, sensitivity_grid.csv, feature_dictionary.md, data_audit_log.md, model_card.md, validation_plan.md and economics_plan.md.

The data/ folder is excluded from Git. The project dependency list is provided in requirements.txt. Exact package versions are not pinned in that file; therefore, results are documented against the project environment rather than a fully version-locked software image. The final Git revision is preserved in the repository’s commit history. This document is complete as a portfolio technical record; no further edits or manual placeholders are required for upload.

**This is a portfolio demonstration, not a production model.**
