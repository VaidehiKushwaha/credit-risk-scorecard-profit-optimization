# credit-risk-scorecard-profit-optimization
PD scorecard, ML challenger and profit-optimal approval strategy for credit cards.

# Problem Definition

## 1. Business Problem

Credit card lenders face a trade-off between losses caused by customer defaults and the revenue lost when credit is unnecessarily restricted. This project investigates how historical customer repayment behavior can be used to estimate next-month default risk and develop a risk-based credit decision strategy.

The primary business question is: **Which decision threshold maximizes expected profit under explicitly defined assumptions about revenue, default losses and operating costs?**

## 2. Project Objectives

The project aims to:

1. Estimate the probability of next-month default for existing credit card customers.
2. Develop an interpretable points-based credit risk scorecard.
3. Compare the scorecard with machine learning challenger models.
4. Evaluate ranking performance, calibration and stability.
5. Identify a profit-optimal decision threshold under illustrative economic assumptions.

## 3. Dataset and Population

The project uses the UCI Default of Credit Card Clients dataset, containing 30,000 customer records from Taiwan. Each observation represents an existing credit card customer with historical billing, payment and repayment-status information.

The data covers April through September 2005, with the target outcome recorded for October 2005.

## 4. Target Definition

The binary target is `DEFAULT`.

- **DEFAULT = 1**: default recorded in the target month.
- **DEFAULT = 0**: no default recorded in the target month.

The default rate will be calculated from the dataset and reported as part of the exploratory data analysis. The target represents a one-month outcome and should not be interpreted as a 12-month probability of default.

## 5. Observation and Performance Windows

The observation window is April–September 2005. Model features will be derived from information available within this period.

The conceptual decision point is the end of September 2005. The performance window is October 2005, during which the target outcome is observed.

No information from the performance window or subsequent events will be used as predictive input features.

## 6. Modeling and Evaluation

The project will develop a logistic regression-based scorecard and compare its performance with machine learning challenger models.

Evaluation will consider Gini, KS, probability calibration and distribution stability. Business evaluation will compare expected profit across decision thresholds and against clearly defined baseline strategies.

All evaluation criteria will be documented before final model selection. Proposed metric ranges are guidelines rather than guaranteed outcomes.

## 7. Fairness and Responsible Lending

SEX, AGE and MARRIAGE are sensitive attributes. In many jurisdictions, lenders may not use gender or marital status in credit decisions, and age is restricted in some. This project will exclude SEX and MARRIAGE from the final model, and will test whether including AGE materially changes performance. EDA may still examine these variables to check for disparities

## 8. Assumptions and Limitations

Assumptions

Revenue and loss figures in the economic analysis are illustrative, because the dataset contains no real profit data.
PAY = -2 is treated as “no consumption / no bill.”
Currency amounts are in NT dollars and are used as given.

Limitations

Data is from one issuer in Taiwan in 2005, so patterns may not transfer to other markets or periods.
There are no timestamps beyond the six-month window, so a true out-of-time validation is not possible. Validation uses a stratified random split. (If you extend to Lending Club later, you can add a true out-of-time test.)
One-month default window, which is shorter than industry practice.
Reject inference is not addressed: a real lender only observes outcomes for customers it approved, so a model trained on approved customers can be biased when applied to the full applicant pool.
Scorecard is behavioral, not an application scorecard. 

This project develops a behavioral scorecard for existing customers. The simplified approve/decline framework used in the economic analysis is a proxy for credit exposure decisions, not a validated application approval policy.

## 9. Project Status

Problem definition and data documentation in progress.
