# Model Card: Credit Risk Scorecard and Profit Optimisation

## 1. Project Overview

**Purpose:** Estimate the probability that an existing credit card customer defaults on their payment in the following month. The models are designed to support credit-risk assessment and customer approval decisions.

**Project type:** Behavioural credit-risk modelling.

**Dataset:** UCI Default of Credit Card Clients.

**Geography and period:** Taiwan, April–September 2005.

**Sample size:** 30,000 customers.

**Target variable:** DEFAULT — whether the customer defaulted in the following month.

**Data split:** Stratified 70:30 training and test split.
- Training: 21,000 customers.
- Locked test: 9,000 customers.

The test set was scored once. Subsequent validation and fairness analyses used the saved test predictions.

## 2. Models Developed

### Model 1: WOE Logistic Regression Scorecard

- Nine selected behavioural features.
- Weight of Evidence (WOE) transformations and logistic regression.
- Designed for interpretability and transparent risk scoring.
- Base score: 600.
- Base odds: 50:1.
- Points to Double the Odds (PDO): 20.

### Model 2: C3 Monotonic LightGBM

- 48 engineered features.
- Gradient-boosted decision trees.
- Monotonic constraints applied to selected features.
- Designed to improve predictive discrimination while retaining selected directional relationships.
- Original uncalibrated probabilities retained because calibration methods did not provide a meaningful overall improvement.

## 3. Input Variables and Exclusions

The scorecard uses nine features:

1. avg_delay
2. delay_trend
3. n_revolving
4. log_limit
5. pay_amt_avg
6. bill_avg_to_limit
7. util_trend
8. util_latest
9. n_bill_increases

The LightGBM challenger uses 48 engineered features covering repayment behaviour, utilisation, payment behaviour, bill dynamics and customer profile.

**Excluded sensitive attributes:** SEX and MARRIAGE were excluded as direct model inputs.

**Age:** Tested during feature selection but excluded because it did not provide a meaningful cross-validation improvement.

## 4. Test Performance

The following results were obtained on the locked test set.

| Metric | WOE Scorecard | C3 Monotonic LightGBM |
|---|---:|---:|
| AUC | 0.7588 | 0.7807 |
| Gini | 0.5176 | 0.5614 |
| Gini 95% CI | [0.4941, 0.5434] | [0.5381, 0.5847] |
| KS | 0.4034 | 0.4319 |
| KS 95% CI | [0.3847, 0.4304] | [0.4103, 0.4555] |
| Brier score | 0.1423 | 0.1351 |
| Brier 95% CI | [0.1378, 0.1471] | [0.1305, 0.1399] |
| Calibration slope | 0.9305 | 0.9655 |

The paired bootstrap Gini improvement of C3 over the scorecard was 0.0438, with a 95% confidence interval of [0.0343, 0.0539].

Both models met the registered generalisation, KS and calibration criteria. C3 demonstrated stronger ranking performance and a lower Brier score.

## 5. Calibration

| Measure | Scorecard | C3 LightGBM |
|---|---:|---:|
| Mean predicted PD | 0.22024 | 0.22059 |
| Actual default rate | 0.22122 | 0.22122 |
| Absolute mean gap | 0.00098 | 0.00064 |
| Calibration slope | 0.9305 | 0.9655 |

Both models meet the registered mean-PD gap and calibration-slope criteria.

The original probabilities were retained without additional calibration.

## 6. Stability and Drift Assessment

| Measure | Result |
|---|---:|
| Train–test score PSI | 0.000539 |
| Maximum scorecard variable CSI | 0.000779 |
| Simulated higher-utilisation score PSI | 0.0262 |

The ordinary train–test distribution comparison showed very little shift.

A simulated higher-utilisation population was created by assigning four times the sampling weight to customers with latest utilisation above 80%.

Under this scenario:
- Mean predicted PD increased to 0.2385.
- Actual default rate increased to 0.2410.
- Gini declined from 0.5176 to 0.4723.

This simulation indicates that ranking performance can weaken under a change in population composition, even when aggregate predicted risk remains close to the actual default rate. It is a hypothetical stress scenario, not evidence of actual future drift.

## 7. Fairness Assessment

The approval policy was based on the 75th percentile of training out-of-fold predicted probabilities.

| Measure | Scorecard | C3 LightGBM |
|---|---:|---:|
| Test approval rate | 75.04% | 74.89% |
| Approval of goods | 83.89% | 84.31% |
| Decline of bads | 56.10% | 58.26% |

All approval-rate ratios across SEX, MARRIAGE and age groups exceeded the 0.80 screening criterion.

The minimum ratios were:
- SEX: 0.9629 for the scorecard and 0.9583 for C3.
- MARRIAGE: 0.9688 for the scorecard and 0.9572 for C3.
- Age bands: 0.9206 for the scorecard and 0.9344 for C3.

### Proxy checks

The 48 model features were used to predict the excluded sensitive attributes through five-fold stratified cross-validation on the training set.

| Attribute | Proxy AUC |
|---|---:|
| SEX | 0.615 |
| MARRIAGE (married vs. not married) | 0.646 |

These results indicate that the model features retain information associated with the excluded attributes. Excluding sensitive variables directly therefore does not eliminate all potential proxy effects.

Groupwise calibration and discrimination differences were also observed. MARRIAGE category 3 had only 111 test customers, making its estimates less reliable.

**Fairness conclusion:** Both models pass the specified approval-rate screening rule, but the proxy signals and groupwise differences mean that fairness cannot be assumed or certified.

## 8. Limitations

1. The dataset represents one credit-card portfolio in Taiwan from 2005.
2. The target covers only a one-month default horizon.
3. No out-of-time validation was possible because the available dataset does not provide the required longitudinal decision-period structure.
4. Reject inference was not addressed.
5. Some repayment-status codes required working assumptions during data cleaning.
6. The random train–test split does not establish performance under real future population drift.
7. The profit analysis will use explicit modelling assumptions and should not be interpreted as observed bank profitability.
8. Proxy information associated with excluded sensitive attributes remains present.

## 9. Monitoring Recommendations

If these models were used in a real portfolio, the following monitoring framework would be appropriate:

- Monitor score PSI and characteristic stability monthly.
- Investigate PSI above 0.10 and treat values above 0.25 as a major drift warning.
- Monitor Gini, KS and calibration against matured outcomes quarterly.
- Monitor calibration gaps and groupwise performance.
- Review approval-rate ratios and proxy risks across relevant customer groups.
- Investigate material Gini deterioration and recalibration requirements before changing the model.
- Validate any revised model on a fresh independent holdout.

These are proposed monitoring recommendations, not monitoring results from this historical dataset.

## 10. Intended Use

**Intended use:** Academic and portfolio demonstration of behavioural credit-risk modelling, scorecard development, model comparison, validation, fairness screening and profit optimisation.

**Not intended for:** Direct use in real lending, credit approval, credit-limit assignment or customer rejection decisions.

The results demonstrate a modelling and validation workflow. They do not establish suitability for a real financial institution without current data, independent validation, governance review and regulatory assessment.

