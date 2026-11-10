import numpy as np
from mne.stats import permutation_cluster_1samp_test
# Within-subject differences: (n_subjects, n_times)
X_diff = X_a - X_b
# Cluster-based permutation test
t_obs, clusters, cluster_pv, H0 = permutation_cluster_1samp_test(    X_diff,    n_permutations=5000,    tail=0,              # Two-sided test
    threshold=None,      # Automatic t-statistic threshold
    adjacency=None,      # Adjacent time points define clusters
    out_type='mask',    seed=42,    n_jobs=-1)
