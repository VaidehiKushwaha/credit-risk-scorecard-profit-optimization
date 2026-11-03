# Data Audit Report

## 1. Data Audit Summary

The credit card dataset contains 30,000 customer records and 24 columns after dropping the customer identifier (`ID`).

The dataset contains no missing values. Undocumented `EDUCATION` and `MARRIAGE` categories were consolidated into the respective "Others" categories.

No customer rows were deleted during the audit. Negative bill amounts were retained because they may represent credit balances. Extreme monetary observations were retained rather than automatically removed.

The audit also identified undocumented repayment-status codes, month-to-month repayment-status jumps, and potential logical inconsistencies. These findings were documented for consideration during feature engineering and modelling.

## 2. Key Data Quality Findings

- 70 rows shared identical feature values after excluding the customer ID; these were retained.
- 795 potentially dormant accounts were retained.
- 3,932 negative bill entries were found across six monthly bill columns.
- No negative payment amounts were found.
- Bills exceeded assigned credit limits in 2.66%–7.05% of monthly records.
- The IQR method flagged 0.6% of `LIMIT_BAL`, 8.0% of `BILL_AMT1`, and 9.2% of `PAY_AMT1`.
- 1,238 records showed a positive repayment-delay status alongside a non-positive previous-month bill.

## 3. Cleaning Decisions

Undocumented education and marriage categories were consolidated into the "Others" categories. No missing-value imputation was required.

No customer records were deleted solely because they had unusual monetary values, negative bill amounts, or potential logical inconsistencies.

The final dataset passed the checks for missing values, target categories, education categories, and marriage categories.

## 4. Modelling Considerations

- Repayment-status codes require cautious interpretation because their documentation is incomplete.
- September repayment status is subject to the stated decision-date assumption.
- Extreme monetary values will be retained for modelling evaluation.
- Any capping of engineered ratios will use training-set percentiles only.
- `ID` will be excluded from model features.
- `DEFAULT` will be used only as the target variable.

## Data Audit Table

| Issue                                       | Finding                                                                                                         | Action                                                                                                                                                                                               |
|:--------------------------------------------|:----------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Duplicates                                  | 70 rows share identical feature values, excluding ID                                                            | Inspected matching profiles. Kept rows because different IDs and identical feature values do not establish that records are accidental duplicates; removing them could exclude legitimate customers. |
| Missing values                              | None found (or: describe what you found)                                                                        | No imputation needed                                                                                                                                                                                 |
| Dormant accounts                            | 795 accounts with zero bills and payments                                                                       | Kept; they are valid inactive customers                                                                                                                                                              |
| EDUCATION codes 0,5,6                       | Undocumented values (468)                                                                                       | Merged into 4 (Others)                                                                                                                                                                               |
| MARRIAGE code 0                             | Undocumented value                                                                                              | Merged into 3 (Others)                                                                                                                                                                               |
| PAY_ codes -2 and 0                         | Not fully documented in source                                                                                  | Assumed -2 = no consumption and 0 = revolving credit; interpretation to be checked against bill amounts.                                                                                             |
| PAY_ codes -2 and 0                         | Not fully documented in source                                                                                  | Tested PAY_0 = -2 against BILL_AMT1: only 32.73% of bills were <= 0. The no-consumption interpretation received limited support; meanings of -2 and 0 remain assumptions.                            |
| PAY_ sequence                               | 8063 month-to-month jumps greater than 1                                                                        | Retained all records. Large increases may reflect genuine changes in repayment status and are not confirmed data errors.                                                                             |
| Negative BILL_AMT                           | 3932 negative entries across six bill columns; 1930 customers affected                                          | Kept because negative bills may represent legitimate credit balances; utilization will be floored at zero in the ratio only.                                                                         |
| Negative PAY_AMT                            | 0 negative entries across all six payment columns                                                               | No correction required; zero and positive payment amounts were retained.                                                                                                                             |
| Negative PAY_AMT                            | 0 negative entries across all six payment columns                                                               | No correction required; zero and positive payment amounts were retained.                                                                                                                             |
| Bills above credit limit                    | 2.66% to 7.05% of records across six monthly bill columns                                                       | Retained; exceeding the assigned limit alone does not establish a data error.                                                                                                                        |
| Bills above credit limit                    | 2.66% to 7.05% of records across six monthly bill columns                                                       | Retained; exceeding the assigned limit alone does not establish a data error.                                                                                                                        |
| Negative BILL_AMT                           | Credit balances (customer overpaid)                                                                             | Kept; handled in utilization feature in Step 4                                                                                                                                                       |
| Bills above credit limit                    | Present in some rows                                                                                            | Kept; legitimate over-limit usage                                                                                                                                                                    |
| Outliers                                    | Heavy right tails in monetary variables; IQR flagged 0.6% of LIMIT_BAL, 8.0% of BILL_AMT1, and 9.2% of PAY_AMT1 | No deletion; extreme values retained pending further validation. WOE binning and tree-based models will be evaluated. Any engineered-ratio capping will use training-set percentiles only.           |
| Late status with non-positive previous bill | 1238 records where PAY_0 >= 1 and BILL_AMT2 <= 0                                                                | Retained and flagged for investigation; the condition alone does not establish a data error.                                                                                                         |

## Data Audit Table

| Issue                                       | Finding                                                                                                         | Action                                                                                                                                                                                               |
|:--------------------------------------------|:----------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Duplicates                                  | 70 rows share identical feature values, excluding ID                                                            | Inspected matching profiles. Kept rows because different IDs and identical feature values do not establish that records are accidental duplicates; removing them could exclude legitimate customers. |
| Missing values                              | None found (or: describe what you found)                                                                        | No imputation needed                                                                                                                                                                                 |
| Dormant accounts                            | 795 accounts with zero bills and payments                                                                       | Kept; they are valid inactive customers                                                                                                                                                              |
| EDUCATION codes 0,5,6                       | Undocumented values (468)                                                                                       | Merged into 4 (Others)                                                                                                                                                                               |
| MARRIAGE code 0                             | Undocumented value                                                                                              | Merged into 3 (Others)                                                                                                                                                                               |
| PAY_ codes -2 and 0                         | Not fully documented in source                                                                                  | Assumed -2 = no consumption and 0 = revolving credit; interpretation to be checked against bill amounts.                                                                                             |
| PAY_ codes -2 and 0                         | Not fully documented in source                                                                                  | Tested PAY_0 = -2 against BILL_AMT1: only 32.73% of bills were <= 0. The no-consumption interpretation received limited support; meanings of -2 and 0 remain assumptions.                            |
| PAY_ sequence                               | 8063 month-to-month jumps greater than 1                                                                        | Retained all records. Large increases may reflect genuine changes in repayment status and are not confirmed data errors.                                                                             |
| Negative BILL_AMT                           | 3932 negative entries across six bill columns; 1930 customers affected                                          | Kept because negative bills may represent legitimate credit balances; utilization will be floored at zero in the ratio only.                                                                         |
| Negative PAY_AMT                            | 0 negative entries across all six payment columns                                                               | No correction required; zero and positive payment amounts were retained.                                                                                                                             |
| Bills above credit limit                    | 2.66% to 7.05% of records across six monthly bill columns                                                       | Retained; exceeding the assigned limit alone does not establish a data error.                                                                                                                        |
| Negative BILL_AMT                           | Credit balances (customer overpaid)                                                                             | Kept; handled in utilization feature in Step 4                                                                                                                                                       |
| Bills above credit limit                    | Present in some rows                                                                                            | Kept; legitimate over-limit usage                                                                                                                                                                    |
| Outliers                                    | Heavy right tails in monetary variables; IQR flagged 0.6% of LIMIT_BAL, 8.0% of BILL_AMT1, and 9.2% of PAY_AMT1 | No deletion; extreme values retained pending further validation. WOE binning and tree-based models will be evaluated. Any engineered-ratio capping will use training-set percentiles only.           |
| Late status with non-positive previous bill | 1238 records where PAY_0 >= 1 and BILL_AMT2 <= 0                                                                | Retained and flagged for investigation; the condition alone does not establish a data error.                                                                                                         |
