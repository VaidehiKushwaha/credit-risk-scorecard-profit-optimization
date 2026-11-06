# Feature Dictionary

This document describes the engineered features used in the credit risk scorecard project.

| Feature | Family | Formula / Description | Business Rationale | Missing Handling | Expected Direction |
|---|---|---|---|---|---|
| `delay_latest` | Delinquency | September PAY status, floored at zero and capped at 3 | Measures current repayment delay | None | Higher = riskier |
| `n_late_months` | Delinquency | Count of months with PAY status above zero | Measures persistent late payment behaviour | None | Higher = riskier |
| `n_late_last3` | Delinquency | Count of delayed months in July–September | Captures recent repayment problems | None | Higher = riskier |
| `max_delay` | Delinquency | Maximum delay across six months, capped at 3 | Measures worst repayment delay | None | Higher = riskier |
| `avg_delay` | Delinquency | Average monthly delay score | Summarises delay severity | None | Higher = riskier |
| `delay_trend` | Delinquency | Slope of monthly delay scores | Identifies worsening or improving repayment behaviour | None | Higher = riskier |
| `months_since_late` | Delinquency | Months since the most recent positive delay code; 6 if never late | Captures recency of repayment problems | None | Lower = riskier |
| `ever_late` | Delinquency | 1 if any positive delay code occurred | Identifies customers with a history of delay | None | 1 = potentially riskier |
| `n_revolving` | Delinquency | Count of months with PAY status 0 | Captures revolving-credit behaviour | None | To be tested |
| `n_paid_full` | Delinquency | Count of months with PAY status -1 | Captures months marked as paid duly | None | Higher = potentially safer |
| `n_no_use` | Delinquency | Count of months with PAY status -2 | Captures months with no consumption under the working interpretation | None | To be tested |
| `util_latest` | Utilization | September bill divided by credit limit, floored at zero and capped at 1.5 | Measures latest credit usage | None | Higher = riskier |
| `util_avg` | Utilization | Average utilization across six months | Measures typical credit usage | None | Higher = potentially riskier |
| `util_max` | Utilization | Maximum monthly utilization | Captures peak credit usage | None | Higher = potentially riskier |
| `util_trend` | Utilization | Slope of monthly utilization | Captures increasing or decreasing credit usage | None | Higher = potentially riskier |
| `util_avg_last3` | Utilization | Average utilization over July–September | Captures recent credit usage | None | Higher = potentially riskier |
| `n_over_limit` | Utilization | Number of months when raw bill exceeded credit limit | Identifies repeated over-limit bills | None | Higher = riskier |
| `n_zero_bill` | Utilization | Number of months with bill at or below zero | Captures months without a positive outstanding bill | None | To be tested |
| `has_credit_bal` | Utilization | 1 if any monthly bill was negative | Identifies credit-balance months | None | To be tested |
| `limit_bal` | Utilization | Original credit limit | Captures credit exposure and prior underwriting | None | To be tested |
| `log_limit` | Utilization | Natural logarithm of credit limit | Reduces right-skewness in credit limit | None | To be tested |
| `pay_ratio_latest` | Payment | September payment divided by August bill, capped at 1.5 | Measures latest repayment coverage | NaN if August bill is not positive | Higher = potentially safer |
| `pay_ratio_avg` | Payment | Average of valid monthly payment ratios | Captures typical repayment coverage | NaN when no valid ratios exist | Higher = potentially safer |
| `pay_ratio_min` | Payment | Minimum valid monthly payment ratio | Captures weakest repayment coverage | NaN when no valid ratios exist | Higher = potentially riskier |
| `pay_ratio_last3` | Payment | Average of the last three valid monthly payment ratios | Captures recent repayment coverage | NaN when no valid ratios exist | Higher = potentially safer |
| `n_valid_ratios` | Payment | Number of positive previous bills available for ratio calculation | Measures how much payment history supports the ratios | None | To be tested |
| `no_prior_bill_latest` | Payment | 1 if August bill was not positive | Identifies an undefined latest payment ratio | None | To be tested |
| `n_paid_zero` | Payment | Number of months with zero payment | Captures zero-payment behaviour | None | Higher = potentially riskier |
| `n_paid_zero_with_bill` | Payment | Number of months with zero payment despite a positive previous bill | Identifies failure to pay despite an outstanding bill | None | Higher = riskier |
| `n_paid_full_cov` | Payment | Number of months where payment covered the entire positive previous bill | Captures full bill coverage | None | Higher = potentially safer |
| `n_min_payer` | Payment | Number of months with payment above zero but below 20% of the previous bill | Captures low payment coverage; 20% is a project assumption | None | Higher = potentially riskier |
| `total_paid_over_billed` | Payment | Sum of five payments divided by sum of five positive previous bills | Measures overall payment coverage | NaN if denominator is zero | Higher = potentially safer |
| `pay_amt_avg` | Payment | Average monthly payment amount across six months | Captures typical payment size | None | To be tested |
| `pay_amt_trend` | Payment | Slope of monthly payment amounts | Captures changes in payment activity | None | Higher = potentially safer |
| `pay_amt_latest_vs_avg` | Payment | September payment divided by six-month average payment | Identifies changes in latest payment activity | NaN if average payment is zero | To be tested |
| `pay_ratio_to_limit` | Payment | September payment divided by credit limit | Scales payment by credit exposure | None | Higher = potentially safer |
| `bill_avg` | Bill dynamics | Average monthly bill | Measures typical outstanding bill amount | None | To be tested |
| `bill_avg_to_limit` | Bill dynamics | Average bill divided by credit limit | Scales average bill by credit exposure | None | To be tested |
| `bill_change_6m` | Bill dynamics | September bill minus April bill, divided by credit limit | Measures scaled six-month bill change | None | Higher = potentially riskier |
| `bill_trend` | Bill dynamics | Slope of monthly bills divided by credit limit | Measures scaled bill movement over time | None | Higher = potentially riskier |
| `bill_cv` | Bill dynamics | Standard deviation of bills divided by absolute average bill | Measures relative bill volatility | NaN when average bill is too close to zero | To be tested |
| `bill_latest_vs_avg` | Bill dynamics | September bill divided by six-month average bill | Compares latest bill with historical average | NaN when average bill is too close to zero | To be tested |
| `n_bill_increases` | Bill dynamics | Number of month-to-month bill increases | Captures frequency of bill growth | None | Higher = potentially riskier |
| `age` | Profile | Customer age | Candidate demographic predictor | None | To be tested |
| `education` | Profile | Customer education category | Candidate profile predictor | None | To be tested |
| `dormant` | Profile | 1 if all six bills and all six payments equal zero | Identifies inactive accounts | None | To be tested |
| `late_and_high_util` | Combined | 1 if September delay is positive and utilization is at least 80% | Captures combined repayment and credit-usage risk | None | Higher = potentially riskier |

Expected directions are hypotheses, not guaranteed relationships. They will be examined during model development.
