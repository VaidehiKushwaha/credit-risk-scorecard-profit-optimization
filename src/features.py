import numpy as np
import pandas as pd


# Arrange the six months from oldest to newest:
# April, May, June, July, August, September
pay_chron = ["PAY_6", "PAY_5", "PAY_4", "PAY_3", "PAY_2", "PAY_0"]
bill_chron = [f"BILL_AMT{i}" for i in range(6, 0, -1)]
amt_chron = [f"PAY_AMT{i}" for i in range(6, 0, -1)]


# Calculate the trend (slope) across six monthly values for each customer
def row_slope(values: np.ndarray) -> np.ndarray:
    x = np.arange(values.shape[1], dtype=float)
    xc = x - x.mean()
    return (values - values.mean(axis=1, keepdims=True)) @ xc / (xc @ xc)


# 1. Delinquency features: repayment delay behaviour
def delinquency_features(d):
    f = pd.DataFrame(index=d.index)

    late = d[pay_chron].clip(lower=0)

    f["pay0_raw"] = d["PAY_0"]
    f["delay_latest"] = late["PAY_0"].clip(upper=3)
    f["n_late_months"] = (late > 0).sum(axis=1)
    f["n_late_last3"] = (late[pay_chron[-3:]] > 0).sum(axis=1)
    f["max_delay"] = late.max(axis=1).clip(upper=3)
    f["avg_delay"] = late.mean(axis=1)
    f["delay_trend"] = row_slope(late.values)

    f["delay_recent_vs_old"] = (
        late[pay_chron[-3:]].mean(axis=1)
        - late[pay_chron[:3]].mean(axis=1)
    )

    is_late = late.values > 0
    last_idx = np.where(
        is_late.any(axis=1),
        5 - np.argmax(is_late[:, ::-1], axis=1),
        -1
    )

    f["months_since_late"] = np.where(
        last_idx >= 0, 5 - last_idx, 6
    )

    f["ever_late"] = (f["n_late_months"] > 0).astype(int)
    f["n_revolving"] = (d[pay_chron] == 0).sum(axis=1)
    f["n_paid_full"] = (d[pay_chron] == -1).sum(axis=1)
    f["n_no_use"] = (d[pay_chron] == -2).sum(axis=1)

    return f


# 2. Utilization features: how much of the credit limit is being used
def utilization_features(d):
    f = pd.DataFrame(index=d.index)

    lim = d["LIMIT_BAL"]

    util = (
        d[bill_chron]
        .clip(lower=0)
        .div(lim, axis=0)
        .clip(upper=1.5)
    )

    f["util_latest"] = util["BILL_AMT1"]
    f["util_avg"] = util.mean(axis=1)
    f["util_max"] = util.max(axis=1)
    f["util_trend"] = row_slope(util.values)
    f["util_avg_last3"] = util[bill_chron[-3:]].mean(axis=1)

    f["n_over_limit"] = d[bill_chron].gt(lim, axis=0).sum(axis=1)
    f["n_zero_bill"] = (d[bill_chron] <= 0).sum(axis=1)
    f["has_credit_bal"] = (d[bill_chron] < 0).any(axis=1).astype(int)

    f["limit_bal"] = lim
    f["log_limit"] = np.log(lim)

    return f


# 3. Payment features: how much customers pay relative to previous bills
def payment_features(d):
    f = pd.DataFrame(index=d.index)

    pay_cols_p = [f"PAY_AMT{i}" for i in range(5, 0, -1)]
    bill_cols_p = [f"BILL_AMT{i}" for i in range(6, 1, -1)]

    P = d[pay_cols_p].values.astype(float)
    B = d[bill_cols_p].values.astype(float)

    # Calculate payment-to-previous-bill ratios only when the bill is positive
    valid = B > 0
    ratio = np.full(P.shape, np.nan)
    ratio[valid] = P[valid] / B[valid]
    ratio = np.clip(ratio, 0, 1.5)

    R = pd.DataFrame(
        ratio,
        index=d.index,
        columns=[f"r{i}" for i in range(5, 0, -1)]
    )

    f["pay_ratio_latest"] = R["r1"]
    f["pay_ratio_avg"] = R.mean(axis=1)
    f["pay_ratio_min"] = R.min(axis=1)
    f["pay_ratio_last3"] = R[["r3", "r2", "r1"]].mean(axis=1)

    f["n_valid_ratios"] = valid.sum(axis=1)
    f["no_prior_bill_latest"] = (~valid[:, -1]).astype(int)

    f["n_paid_zero"] = (d[pay_cols_p] == 0).sum(axis=1)
    f["n_paid_zero_with_bill"] = ((P == 0) & valid).sum(axis=1)
    f["n_paid_full_cov"] = ((P >= B) & valid).sum(axis=1)
    f["n_min_payer"] = ((ratio > 0) & (ratio < 0.2)).sum(axis=1)

    total_billed = (
        d[bill_cols_p]
        .clip(lower=0)
        .sum(axis=1)
        .replace(0, np.nan)
    )

    f["total_paid_over_billed"] = d[pay_cols_p].sum(axis=1) / total_billed

    f["pay_amt_avg"] = d[amt_chron].mean(axis=1)
    f["pay_amt_trend"] = row_slope(d[amt_chron].values.astype(float))

    avg_payment = d[amt_chron].mean(axis=1).replace(0, np.nan)

    f["pay_amt_latest_vs_avg"] = d["PAY_AMT1"] / avg_payment
    f["pay_ratio_to_limit"] = d["PAY_AMT1"] / d["LIMIT_BAL"]

    return f


# 4. Bill features: changes and patterns in monthly outstanding bills
def bill_features(d):
    f = pd.DataFrame(index=d.index)

    B = d[bill_chron].values.astype(float)
    lim = d["LIMIT_BAL"].values

    avg_bill = B.mean(axis=1)

    f["bill_avg"] = avg_bill
    f["bill_avg_to_limit"] = avg_bill / lim
    f["bill_change_6m"] = (
        (d["BILL_AMT1"] - d["BILL_AMT6"]) / d["LIMIT_BAL"]
    )
    f["bill_trend"] = row_slope(B) / lim

    f["bill_cv"] = (
        B.std(axis=1)
        / np.where(np.abs(avg_bill) > 1, np.abs(avg_bill), np.nan)
    )

    f["bill_latest_vs_avg"] = (
        d["BILL_AMT1"]
        / np.where(np.abs(avg_bill) > 1, avg_bill, np.nan)
    )

    f["n_bill_increases"] = (np.diff(B, axis=1) > 0).sum(axis=1)

    return f


# 5. Profile features: basic customer profile and combined risk indicators
def profile_features(d):
    f = pd.DataFrame(index=d.index)

    f["age"] = d["AGE"]
    f["education"] = d["EDUCATION"]

    f["dormant"] = (
        (d[bill_chron] == 0).all(axis=1)
        & (d[amt_chron] == 0).all(axis=1)
    ).astype(int)

    late_latest = d["PAY_0"].clip(lower=0)

    util_latest = (
        d["BILL_AMT1"].clip(lower=0) / d["LIMIT_BAL"]
    ).clip(upper=1.5)

    f["late_and_high_util"] = (
        (late_latest >= 1) & (util_latest >= 0.8)
    ).astype(int)

    return f


# Combine all five feature groups into one feature table
def build_features(d):
    parts = [
        delinquency_features(d),
        utilization_features(d),
        payment_features(d),
        bill_features(d),
        profile_features(d)
    ]

    X = pd.concat(parts, axis=1)
    X = X.replace([np.inf, -np.inf], np.nan)

    return X

    