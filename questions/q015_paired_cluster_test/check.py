import numpy as np

import mne

EXPECTED = None


def setup():
    global EXPECTED
    rng = np.random.default_rng(0)
    base = rng.standard_normal((20, 1)) * 3  # large between-subject offsets
    X_b = base + rng.standard_normal((20, 100))
    X_a = base + rng.standard_normal((20, 100))
    X_a[:, 50:70] += 0.8
    EXPECTED = mne.stats.ttest_1samp_no_p(X_a - X_b)
    return {"mne": mne, "np": np, "X_a": X_a, "X_b": X_b}


def check(ns):
    t_obs = ns.get("t_obs")
    if t_obs is None:
        return False, "no `t_obs` variable"
    t_obs = np.ravel(t_obs)
    if t_obs.shape != EXPECTED.shape or not np.allclose(np.abs(t_obs), np.abs(EXPECTED), rtol=1e-3):
        return False, "statistic is not the paired (1-sample on differences) t-test"
    if ns.get("cluster_pv") is None or np.min(ns["cluster_pv"]) >= 0.05:
        return False, "paired statistic but no significant cluster found"
    return True, "paired test with a significant cluster"
