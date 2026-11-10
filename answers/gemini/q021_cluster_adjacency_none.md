Leaving `adjacency=None` when running `mne.stats.spatio_temporal_cluster_1samp_test` on sensor-level data is **not OK** and will lead to invalid spatial clustering.

---

### How Clusters Are Formed When `adjacency=None`

According to MNE-Python's documentation, if `adjacency=None`, the function assumes a **regular lattice adjacency** along the dimensions of your data array.

* **Time dimension:** Time points are correctly linked to their immediate temporal neighbors ($t - 1$ and $t + 1$).
* **Channel dimension:** Each channel at index $i$ is treated as a neighbor only to channels at index $i - 1$ and $i + 1$ based strictly on **their sequence in your NumPy array**, rather than their physical layout on the scalp.

### Why This Is Problematic for Sensor Data

In standard MNE datasets, channels are ordered alphabetically, numerically, or arbitrarily by the acquisition system (e.g., `'A1'`, `'A2'`, etc., or sorted channel names).

* An alphabetical or arbitrary index order **does not map to physical space**.
* Channel index `5` might be adjacent to channel index `6` in your array, but physically located on opposite sides of the head.
* Consequently, MNE will group physically unrelated electrodes into the same spatial clusters, completely breaking the assumption of spatial contiguity required for cluster-based permutation tests.

---

### How to Fix It

You must explicitly compute a spatial adjacency matrix using `mne.channels.find_ch_adjacency()` based on your channel layout and pass it to the `adjacency` parameter.

Here is how you properly set it up:

```python
from mne.channels import find_ch_adjacency
from mne.stats import spatio_temporal_cluster_1samp_test

# 1. Compute spatial adjacency for your sensor type (e.g., 'eeg' or 'mag'/'grad')
spatial_adjacency, ch_names = find_ch_adjacency(info, ch_type='eeg')

# 2. Run the test with the proper adjacency matrix
# Note: When passing a 2D spatial adjacency matrix (n_channels, n_channels),
# MNE automatically handles time connectivity using the max_step parameter (default max_step=1).
T_obs, clusters, cluster_pv, H0 = spatio_temporal_cluster_1samp_test(
    X,
    threshold=threshold,
    n_permutations=1024,
    adjacency=spatial_adjacency,
    tail=0
)

```
