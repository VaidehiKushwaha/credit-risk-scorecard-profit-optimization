
# Data Dictionary

This document describes the variables in the UCI Default of Credit Card Clients dataset used in the Credit Risk Scorecard & Profit-Optimal Approval Strategy project.

| Column | Description | Type | Available at decision time? | Notes |
|---|---|---|---|---|
| `LIMIT_BAL` | Credit limit | Numeric | Yes | |
| `SEX` | Gender (1 = male, 2 = female) | Categorical | Yes | Sensitive; see fairness note |
| `EDUCATION` | 1 = graduate school, 2 = university, 3 = high school, 4 = other | Categorical | Yes | Values 0, 5, and 6 are undocumented; review in Step 2 |
| `MARRIAGE` | 1 = married, 2 = single, 3 = other | Categorical | Yes | Value 0 is undocumented; sensitive |
| `AGE` | Age in years | Numeric | Yes | Sensitive; see fairness note |
| `PAY_0` | September repayment status | Ordinal | Yes | Values range from -2 to 8; verify against source documentation |
| `PAY_2` to `PAY_6` | August to April repayment status | Ordinal | Yes | Verify month mapping against source documentation |
| `BILL_AMT1` to `BILL_AMT6` | September to April bill amounts | Numeric | Yes | Some values may be negative, e.g. overpayments |
| `PAY_AMT1` to `PAY_AMT6` | September to April payment amounts | Numeric | Yes | |
| `DEFAULT` | Default in October | Binary | **No — target variable** | This is the outcome to predict, not a model input |

## Fairness Note

Demographic variables such as `SEX`, `AGE`, and `MARRIAGE` require careful consideration in credit-risk modelling. Their availability in the dataset does not automatically mean they should be used in a deployed decision system. Excluding them also does not guarantee fairness, because other variables may act as proxies.

## Data Quality Note

The documented category values and month mappings should be verified against the original dataset documentation and the actual data file. Undocumented values should be investigated before deciding how to handle them.
