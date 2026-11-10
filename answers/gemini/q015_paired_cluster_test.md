To perform a cluster-based permutation test for a within-subject design over time, the standard and most robust approach in Python is using **MNE-Python**.

Since it is a within-subject comparison between two conditions (`X_a` and `X_b`), you compute the difference array (`diff = X_a - X_b`) and run a **one-sample cluster-based permutation t-test** against zero using `mne.stats.permutation_cluster_1samp_test`.

### Python Implementation

```python
import numpy as np
import mne

# 1. Compute the within-subject difference (shape: n_subjects, n_times)
diff = X_a - X_b

# 2. Run the cluster-based permutation test
# threshold can be a float (e.g., t-value corresponding to p < 0.05) or None for automatic thresholding
t_obs, clusters, cluster_pv, H0 = mne.stats.permutation_cluster_1samp_test(
    diff,
    n_permutations=1024,
    tail=0,          # 0 for a two-tailed test, 1 or -1 for one-tailed
    threshold=None,  # If None, uses a t-threshold equivalent to p=0.05 (two-tailed)
    out_type='mask'
)

```

### Key Variables

* **`t_obs`**: Array of shape `(n_times,)` containing the observed t-statistic for each time point across participants.
* **`cluster_pv`**: Array containing the corrected permutation p-value for each identified cluster.
* **`clusters`**: A tuple of boolean arrays indicating the time indices belonging to each significant or tested cluster.
