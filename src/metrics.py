import numpy as np
import pandas as pd

from scipy.stats import ks_2samp
from sklearn.metrics import roc_auc_score, brier_score_loss


# 1. AUC: measures how well the model ranks customers by risk
def auc(y, s):
    return roc_auc_score(y, s)


# 2. Gini: calculated from AUC
def gini(y, s):
    return 2 * roc_auc_score(y, s) - 1


# 3. KS: measures the maximum separation between good and bad customers
def ks_stat(y, s):
    y, s = np.asarray(y), np.asarray(s)
    return ks_2samp(s[y == 1], s[y == 0]).statistic


# 4. Brier score: measures the accuracy of predicted probabilities
def brier(y, p):
    return brier_score_loss(y, p)


# 5. PSI: measures how much a population's feature distribution has shifted
def psi(expected, actual, bins=10):
    """
    Population Stability Index.
    Bins are created using the expected (reference) sample.
    Missing values are ignored here; check missing rates separately.
    """
    expected = pd.Series(expected).dropna()
    actual = pd.Series(actual).dropna()

    cuts = np.unique(
        np.quantile(expected, np.linspace(0, 1, bins + 1))
    )

    if len(cuts) < 3:
        return 0.0

    cuts[0], cuts[-1] = -np.inf, np.inf

    e = (
        pd.cut(expected, cuts)
        .value_counts(normalize=True, sort=False)
        .clip(lower=1e-4)
    )

    a = (
        pd.cut(actual, cuts)
        .value_counts(normalize=True, sort=False)
        .clip(lower=1e-4)
    )

    return float(((a - e) * np.log(a / e)).sum())


# 6. Decile table: groups customers into ten risk groups
def decile_table(y, p, n=10):
    d = pd.DataFrame({
        "y": np.asarray(y),
        "p": np.asarray(p)
    })

    d["decile"] = (
        pd.qcut(
            d["p"].rank(method="first"),
            n,
            labels=False
        ) + 1
    )

    g = d.groupby("decile").agg(
        customers=("y", "size"),
        bads=("y", "sum"),
        avg_pd=("p", "mean"),
        bad_rate=("y", "mean")
    )

    g = g.sort_index(ascending=False)

    g["cum_bads_captured_%"] = (
        100 * g["bads"].cumsum() / g["bads"].sum()
    )

    return g


# 7. Summary: calculates the main performance metrics together
def summarize(y, p, name=""):
    return {
        "model": name,
        "AUC": auc(y, p),
        "Gini": gini(y, p),
        "KS": ks_stat(y, p),
        "Brier": brier(y, np.clip(p, 0, 1))
    }