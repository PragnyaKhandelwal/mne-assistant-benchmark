```python
t_obs, clusters, cluster_pv, h0 = mne.stats.permutation_cluster_1samp_test(
    X_a - X_b, n_permutations=1000, seed=0)
```
