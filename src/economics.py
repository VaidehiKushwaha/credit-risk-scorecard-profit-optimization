
import numpy as np
import pandas as pd


def realized_profit(y, R, L):
    """Profit per customer IF approved: +R if good (y=0), -L if bad (y=1)."""
    return np.where(y == 0, R, -L)


def evaluate(y, approve, R, L):
    """Realized outcome of a decision rule (approve = boolean array)."""
    y = np.asarray(y)
    approve = np.asarray(approve, bool)

    R = np.broadcast_to(R, y.shape)
    L = np.broadcast_to(L, y.shape)

    pr = np.where(approve, realized_profit(y, R, L), 0.0)

    return {
        "approval_rate": approve.mean(),
        "bad_rate_approved": y[approve].mean() if approve.any() else np.nan,
        "profit_total": pr.sum(),
        "profit_per_customer": pr.mean()
    }


def profit_grid(y, p, R, L, cuts):
    """Profit per customer if approving everyone with PD <= cut, for each cut."""
    y = np.asarray(y)
    p = np.asarray(p)

    R = np.broadcast_to(R, y.shape)
    L = np.broadcast_to(L, y.shape)

    pr = realized_profit(y, R, L)

    return pd.DataFrame({
        "cut": cuts,
        "approve_rate": [(p <= c).mean() for c in cuts],
        "profit_pc": [pr[p <= c].sum() / len(y) for c in cuts]
    })


def decompose(y, approve, R, L):
    """Where does the gain vs approve-all come from?"""
    y = np.asarray(y)
    dec = ~np.asarray(approve, bool)

    R = np.broadcast_to(R, y.shape)
    L = np.broadcast_to(L, y.shape)

    avoided = (L * (dec & (y == 1))).sum()
    foregone = (R * (dec & (y == 0))).sum()

    return {
        "losses_avoided": avoided,
        "revenue_foregone": foregone,
        "net_gain_vs_approve_all": avoided - foregone
    }

