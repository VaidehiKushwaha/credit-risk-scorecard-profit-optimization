### Step 6.6 — Logistic Regression Variable Selection

Backward elimination reduced the initial 23 WOE-transformed predictors to nine variables: `avg_delay`, `delay_trend`, `n_revolving`, `log_limit`, `pay_amt_avg`, `bill_avg_to_limit`, `util_trend`, `util_latest`, and `n_bill_increases`.

All nine retained variables had negative coefficients and p-values below 0.05. McFadden pseudo-R² decreased only slightly from 0.1735 to 0.1727 after variable elimination.

L1 regularisation selected 17 variables, including all nine variables retained by backward elimination. This provides additional support for the nine-variable core specification.

The final model's VIF values ranged from 1.438 to 2.969, indicating no serious multicollinearity concerns under the chosen threshold of 5.

**Decision:** Carry the nine-variable backward-elimination model forward for cross-validation and scorecard development. Variable selection was performed using the training sample only.

### Step 6.7 — Five-fold Cross-validation

The nine-variable WOE logistic scorecard was evaluated using stratified five-fold cross-validation. Binning rules and logistic regression coefficients were refitted within each fold.

- Average Gini: 0.544
- Standard deviation of Gini: 0.016
- AUC: 0.772
- KS: 0.425
- Brier score: 0.139

The decile analysis showed a clear risk gradient. The actual default rate was 64.71% in the highest-risk decile and 5.29% in the lowest-risk decile. The highest-risk 20% of customers accounted for approximately 49.88% of all defaults.

**Interpretation:** The scorecard demonstrates useful and relatively consistent risk-ranking ability. Probability calibration and independent test performance will require further evaluation.

### Step 6.8 — Age Inclusion Assessment

The nine-variable scorecard was compared with an alternative specification that included age.

| Metric | Without age | With age |
|---|---:|---:|
| Average Gini | 0.5442 | 0.5443 |
| Gini standard deviation | 0.0160 | 0.0165 |

Adding age improved average Gini by only 0.0001, which is negligible.

**Decision:** Age was excluded from the final scorecard because it provided no meaningful improvement in predictive performance and its inclusion would introduce an additional demographic variable into the credit decision model.