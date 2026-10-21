
# Credit Risk Scorecard & Profit-Optimal Approval Strategy

PD scorecard, machine learning challenger models, and profit-optimal credit decision strategy.

## 1. Business Problem

Credit card lenders face a trade-off between losses caused by customer defaults and revenue lost when credit is unnecessarily restricted.

This project investigates how historical repayment behaviour can be used to estimate next-month default risk and develop a risk-based credit decision strategy.

**Primary business question:** Which decision threshold maximizes expected profit under explicitly defined assumptions about revenue, default losses, and operating costs?

## 2. Project Objectives

The project aims to:

1. Estimate the probability of next-month default for existing credit card customers.
2. Develop an interpretable, points-based credit risk scorecard.
3. Compare the scorecard with machine learning challenger models.
4. Evaluate ranking performance, calibration, and stability.
5. Identify a profit-optimal decision threshold under illustrative economic assumptions.

## 3. Dataset and Population

The project uses the UCI Default of Credit Card Clients dataset, containing approximately 30,000 customer records from Taiwan in 2005.

Each observation represents an existing credit card customer with historical billing, payment, repayment-status, and demographic information.

The observation period covers April–September 2005, with the target outcome recorded for October 2005. Exact variable-to-month mappings will be verified against the original dataset documentation.

**Dataset source:** UCI Default of Credit Card Clients. Add the official dataset URL when finalising the repository.

Expected project file location: `data/credit_card_default.csv`.

## 4. Target Definition

The binary target is `DEFAULT` in the cleaned dataset. The original UCI column is commonly named `default.payment.next.month`.

- `DEFAULT = 1`: Default recorded in the target month.
- `DEFAULT = 0`: No default recorded in the target month.

The actual default rate will be calculated and reported during exploratory data analysis.

The target represents a one-month outcome and must not be interpreted as a 12-month probability of default.

## 5. Observation and Performance Windows

- **Observation window:** April–September 2005.
- **Conceptual decision point:** End of September 2005.
- **Performance window:** October 2005.

Predictive features must use only information available at the conceptual decision point. Information from the performance window or subsequent events must not be used as input features.

## 6. Modelling and Evaluation

The planned modelling workflow is:

1. Problem definition and data audit.
2. Exploratory data analysis (EDA) and feature engineering.
3. Weight of Evidence (WoE) / Information Value (IV) logistic regression scorecard.
4. XGBoost or LightGBM challenger model with SHAP-based interpretation.
5. Model validation using Gini, KS, calibration, and Population Stability Index (PSI).
6. Profit-optimal threshold selection and sensitivity analysis.

The project will evaluate predictive performance separately from business value. Threshold selection will use clearly defined economic assumptions and will be evaluated on data not used to tune the threshold.

Proposed metric ranges are evaluation guidelines, not guaranteed results.

## 7. Fairness and Responsible Lending

Variables such as `SEX`, `AGE`, and `MARRIAGE` require careful consideration in credit-risk modelling.

The planned approach is to exclude `SEX` and `MARRIAGE` from the final model and investigate whether including `AGE` materially changes performance. Their use in a real lending system would require jurisdiction-specific legal and policy review.

Exploratory analysis may examine these variables to investigate potential disparities. Removing demographic variables does not automatically eliminate bias because other variables may act as proxies.

## 8. Assumptions and Limitations

### Assumptions

1. Revenue and loss figures used in the economic analysis are illustrative because the dataset does not contain actual profit data.
2. The treatment of repayment-status value `-2` will be verified against the dataset documentation before assigning a business interpretation.
3. Currency amounts will be used as recorded in the source dataset, with units documented and verified.

### Limitations

1. The data represents a particular credit-card population in Taiwan in 2005 and may not generalise to current customers or other markets.
2. The dataset has a single target period, limiting genuine out-of-time validation. A stratified random split can assess performance within the historical sample but does not establish future temporal stability.
3. The target covers one month rather than a longer default horizon.
4. Reject inference is not addressed. Outcomes for rejected applicants are unavailable, so results for existing cardholders may not generalise to the entire applicant population.
5. This is a behavioural scorecard for existing customers, not an application scorecard for new applicants.
6. The simplified approve/decline framework in the economic analysis is a proxy for credit-exposure decisions, not a validated real-world lending policy.
7. Predictive relationships do not establish causation, and model performance alone does not establish fairness or regulatory compliance.

## 9. How to Run

Create the project environment using Conda:

```bash
conda create -n credit-risk python=3.11
conda activate credit-risk
pip install -r requirements.txt
```

Open JupyterLab or Jupyter Notebook and run the notebooks in the documented project workflow.

Ensure that the dataset is stored in the expected location before running the analysis.

## 10. Headline Results

To be completed after model development and validation.

This section will report the selected model, validation results, calibration findings, and profit-optimal decision threshold under the stated economic assumptions.

## 11. Project Status

**Current stage:** Problem definition, data documentation, and exploratory data analysis.

Progress and results will be updated as the project develops.
