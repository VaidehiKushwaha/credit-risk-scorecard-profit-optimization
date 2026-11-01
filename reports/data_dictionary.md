
# Data Dictionary

This document describes the variables in the UCI Default of Credit Card Clients dataset used in the Credit Risk Scorecard & Profit-Optimal Approval Strategy project.

| Column | Description | Type | Available at decision time? |
|---|---|---|---|
| `LIMIT_BAL` | Credit limit | Numeric | Yes | |
| `SEX` | Gender (1 = male, 2 = female) | Categorical | Yes |
| `EDUCATION` | 1 = graduate school, 2 = university, 3 = high school, 4 = other | Categorical | Yes |
| `MARRIAGE` | 1 = married, 2 = single, 3 = other | Categorical | Yes |
| `AGE` | Age in years | Numeric | Yes |
| `PAY_0` | September repayment status | Ordinal | Yes |
| `PAY_2` to `PAY_6` | August to April repayment status | Ordinal | Yes |
| `BILL_AMT1` to `BILL_AMT6` | September to April bill amounts | Numeric | Yes |
| `PAY_AMT1` to `PAY_AMT6` | September to April payment amounts | Numeric | Yes |
| `DEFAULT` | Default in October | Binary | **No — target variable** |

## Fairness Note

Demographic variables such as `SEX`, `AGE`, and `MARRIAGE` require careful consideration in credit-risk modelling. Their availability in the dataset does not automatically mean they should be used in a deployed decision system. Excluding them also does not guarantee fairness, because other variables may act as proxies.

## Data Quality Note

The documented category values and month mappings should be verified against the original dataset documentation and the actual data file. Undocumented values should be investigated before deciding how to handle them.

### Data Leakage Audit

The prediction decision point is assumed to be the end of September 2005. Each variable was assessed to determine whether the information would have been available to the lender at that point.

| Column | Source month | Known at decision? | Leakage risk | Verdict |
|---|---|---|---|---|
| `LIMIT_BAL` | Set by lender | Yes | None | Allowed |
| `SEX`, `MARRIAGE`, `AGE`, `EDUCATION` | Customer profile | Yes | None (but fairness issue) | Allowed to test; SEX and MARRIAGE excluded from final model |
| `PAY_0` | September | Yes, subject to timing assumption | Low | Allowed |
| `PAY_2` to `PAY_6` | August to April | Yes | None | Allowed |
| `BILL_AMT1` to `BILL_AMT6` | September to April | Yes, assuming statements are issued | None | Allowed |
| `PAY_AMT1` to `PAY_AMT6` | September to April | Yes | None | Allowed |
| `ID` | Index | Not applicable | No predictive meaning | Drop |
| `DEFAULT` | October | No | It is the target | Never a feature |

**Timing assumption:** All six months of repayment, bill and payment information are assumed to be fully observed and available at the decision point. In particular, `PAY_0` reflects September's repayment cycle. If September's status were finalized only after the decision date, it would create a timing risk.

**Conclusion:** No obvious leakage columns were identified under the stated timing assumption. `DEFAULT` is retained as the target variable and excluded from model inputs. `ID` is excluded because it is an identifier rather than a meaningful predictive feature.

SEX and MARRIAGE will be excluded from the final model as a modelling and fairness-related decision, although they may be examined during exploratory analysis.