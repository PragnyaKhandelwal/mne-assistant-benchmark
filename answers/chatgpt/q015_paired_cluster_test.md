You can use `scipy` and `mne.stats.permutation_cluster_1samp_test` for a within-subject cluster-based permutation test.

First, calculate the paired difference (`X_a - X_b`), then perform a one-sample cluster permutation test against zero.

```
import numpy as npfrom mne.stats import permutation_cluster_1samp_test# Within-subject differences: (n_subjects, n_times)X_diff = X_a - X_b# Cluster-based permutation testt_obs, clusters, cluster_pv, H0 = permutation_cluster_1samp_test(    X_diff,    n_permutations=5000,    tail=0,              # Two-sided test    threshold=None,      # Automatic t-statistic threshold    adjacency=None,      # Adjacent time points define clusters    out_type='mask',    seed=42,    n_jobs=-1)# Observed statistic array# t_obs.shape == (n_times,)# Cluster p-values# cluster_pv contains one p-value per detected cluster# Significant clusters at alpha = 0.05significant_clusters = [    clusters[i] for i in range(len(cluster_pv))    if cluster_pv[i] < 0.05]
```

Interpretation:

- `t_obs`: Observed t-statistic at each time point.
- `clusters`: Boolean masks identifying the time points belonging to each cluster.
- `cluster_pv`: Permutation-based p-value for each cluster.
- `H0`: Null distribution of the maximum cluster-level statistics.

Important: This is a paired test because the permutation test operates on the within-subject differences. It preserves the repeated-measures structure by sign-flipping each participant's entire difference time course rather than shuffling individual time points.

With 20 participants, there are \\(2^{20}=1,048,576\\) possible sign-flip combinations, so 5,000 permutations provide a reasonable approximation.
