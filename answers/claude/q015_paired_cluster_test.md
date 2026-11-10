Here is a paired (within-subject) cluster-based permutation test using MNE-Python. A paired test is equivalent to a one-sample test on the difference, with permutations done by random sign flips.

```python
import numpy as np
from mne.stats import permutation_cluster_1samp_test

# X_a, X_b: (n_subjects, n_times)
X = X_a - X_b                      # within-subject difference, shape (20, n_times)

t_obs, clusters, cluster_pv, H0 = permutation_cluster_1samp_test(
    X,
    threshold=None,        # None -> cluster-forming threshold from t-dist at p < 0.05 (two-tailed)
    tail=0,                # two-sided: finds positive and negative clusters
    n_permutations=10000,  # 2**20 possible sign flips, so MNE uses random sign flips
    seed=42,               # reproducibility
    out_type="mask",       # clusters returned as boolean masks over time
    adjacency=None,        # 1D data: neighboring time points are treated as adjacent
)

# Inspect significant clusters
alpha = 0.05
for cl, p in zip(clusters, cluster_pv):
    if p < alpha:
        idx = np.where(cl)[0]
        print(f"Cluster from sample {idx[0]} to {idx[-1]}, p = {p:.4f}")
```

What you get back:

- `t_obs`: shape `(n_times,)`, the paired t-statistic at each time point.
- `clusters`: list of boolean masks, one per cluster found.
- `cluster_pv`: one corrected p-value per cluster, based on the max cluster-mass distribution under sign-flip permutations. This controls family-wise error across time.
- `H0`: the permutation distribution of the max cluster statistic.

Notes:

- With `tail=0`, the default threshold is two-tailed (`t.ppf(1 - 0.05/2, df=19)`). To use a different cluster-forming threshold, pass e.g. `threshold=2.5`. Note that the threshold affects which clusters are found, not the alpha for the cluster p-values.
- By default the cluster statistic is the sum of t-values within a cluster (cluster mass), which is the usual choice.
- If you also want to cluster with threshold-free cluster enhancement, set `threshold=dict(start=0, step=0.2)`. In that case the output is per-time-point p-values rather than per-cluster.

If you'd rather not depend on MNE, I can write an equivalent version using only NumPy/SciPy.
