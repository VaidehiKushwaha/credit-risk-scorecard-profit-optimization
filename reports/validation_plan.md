# Step 8: Final Validation Plan

**Written before scoring the locked test set**

## 1. Models evaluated

1. **Champion:** WOE logistic scorecard, using the nine variables selected in Step 6.
2. **Challenger:** C3 Monotonic LightGBM, using all 48 candidate features.

**Calibration:** None. Original uncalibrated predictions will be retained because Platt and isotonic calibration did not meaningfully improve the Step 7 results.

## 2. Acceptance criteria

| Area | Criterion |
|---|---|
| Discrimination | Test Gini within 0.03 of CV Gini, or CV Gini inside the test 95% CI |
| Separation | KS above 0.35 |
| Calibration | Absolute difference between mean predicted PD and observed default rate below 0.01 |
| Calibration slope | Between 0.8 and 1.2 |
| Stability | Score PSI below 0.10; scorecard variable CSI below 0.10 |
| Fairness screening | Approval-rate ratio at least 0.80, with groupwise Gini and calibration gaps reported |
| Model comparison | Challenger considered superior only if the paired Gini-difference 95% CI excludes zero |

Approval thresholds will be determined using training out-of-fold predictions only. Test results will not be used to select or modify thresholds.

## 3. Bootstrap procedure

- Number of resamples: 2,000
- Random seed: 2026
- Confidence intervals: Percentile 95% intervals
- Paired model comparison: Both models evaluated on the same bootstrap resamples.

## 4. Test-set protocol

1. Verify the Step 5 data fingerprints before scoring.
2. Load the saved scorecard and C3 LightGBM models.
3. Score the locked test set once.
4. Save actual outcomes, predicted probabilities and scorecard scores in `reports/test_predictions.csv`.
5. Restart the notebook kernel.
6. Conduct all subsequent test analysis using the saved prediction file.

## 5. Restrictions

- Do not change features, binning, model parameters or calibration after viewing test performance.
- Do not select approval thresholds using test outcomes.
- Do not retrain models using the test set.
- Do not overwrite the original test predictions file.
- Document all validation results, limitations and fairness findings.

The test set is reserved for independent final validation.

