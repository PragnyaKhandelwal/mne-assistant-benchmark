With `adjacency=None`, MNE treats the spatial dimension as **fully connected**: every channel is considered a neighbor of every other channel. Temporal adjacency is still handled as usual (adjacent time points connect).

**How clusters form**

- A cluster is a set of supra-threshold (time, channel) points connected through time and/or space.
- With full spatial connectivity, any two supra-threshold points that are at *adjacent time samples* are connected, regardless of which channels they're on. So a supra-threshold point at channel Fz at time t and one at Oz at time t+1 are part of the same cluster. Points at the same time on different channels are also connected, so all supra-threshold channels at a given time sample merge into one blob.
- In practice, clusters become essentially "time segments": runs of consecutive samples where *any* channel exceeds threshold get glued together, and clusters are extended across the whole scalp.

**Is that OK?**

Usually no, for sensor-level EEG/MEG data, for a few reasons:

1. **It violates the logic of the method.** Cluster-based inference assumes effects that are spatially contiguous. Ignoring the sensor layout throws away that assumption, so the cluster mass no longer reflects a spatially coherent effect.
2. **Sensitivity drops for focal effects.** Unrelated, scattered supra-threshold points get merged into one big cluster, which makes the cluster statistic dominated by noise-driven points and diffuses the distribution of the max cluster statistic under the null. Real, focal effects can be harder to detect.
3. **The spatial interpretation is meaningless.** A significant cluster tells you almost nothing about *where* the effect is, since you'd be claiming a "cluster" that spans non-neighboring sensors.
4. **It's an odd null/alternative combination.** You've effectively built a test closer to a temporal-only cluster test on the union of channels, but without declaring that intention.

It's defensible only if you deliberately want that (e.g., a pure time-course test where channel identity is irrelevant, or a single-channel / ROI-averaged analysis, in which case you'd just use a 1D temporal test).

**What to do instead**

Provide a sensor adjacency matrix:

```python
from mne.channels import find_ch_adjacency

adjacency, ch_names = find_ch_adjacency(epochs.info, ch_type="eeg")  # or "mag"/"grad"
# make sure the data's channel order matches ch_names

T_obs, clusters, p_values, H0 = mne.stats.spatio_temporal_cluster_1samp_test(
    X,  # (n_subjects, n_times, n_channels)
    adjacency=adjacency,
    n_permutations=1000,
    threshold=None,      # or an explicit t/F threshold
    tail=0,
)
```

Notes:

- `find_ch_adjacency` uses a Delaunay triangulation of the sensor positions, which is reasonable for most setups. You can also use a distance-based or custom matrix (e.g. `mne.channels.read_ch_adjacency` for built-in layouts such as `"neuromag306mag"`).
- For Neuromag data, handle magnetometers and gradiometers separately (different `ch_type`), since they have different units and scale.
- Make sure the channel dimension of `X` matches the adjacency matrix order, and that the data layout really is `(n_subjects, n_times, n_channels)` (the function expects times then space).
- Remember that the cluster-based test supports the claim that *there is an effect*, not that it's located precisely at the extent of the cluster.
