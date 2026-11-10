When you set `adjacency=None` in `mne.stats.spatio_temporal_cluster_1samp_test`, MNE assumes that all channels are spatially connected to one another. It does not use the physical sensor layout to determine neighboring channels.

For your data shape:

```
(n_subjects, n_times, n_channels)
```

the clustering is performed over the time × channel dimensions, with the subject dimension used for the one-sample statistical test.

This is an important distinction: `adjacency=None` does not mean that channels are ignored or that clustering happens independently at each channel.

## 1. Exactly how are clusters formed?

With `adjacency=None`, MNE uses a regular lattice (grid) adjacency.

For your 2D data dimensions (time, channels), the neighborhood relationships are:

- Temporal adjacency: immediately neighboring time samples are connected.
- Spatial adjacency: immediately neighboring channel indices are connected.

Consequently, two supra-threshold samples can belong to the same cluster if they are connected through neighboring time samples, neighboring channel indices, or a combination of both.

For example, suppose you have four channels ordered as:

```
channels = ['Fz', 'Cz', 'Pz', 'Oz']
```

MNE effectively treats their spatial arrangement as:

```
Fz — Cz — Pz — Oz
```

This is a one-dimensional chain, not the actual geometry of the EEG/MEG sensor array.

Importantly, MNE does not know that Fz and Cz are physically close, or that Cz and Pz are physically close. It simply uses the channel ordering.

This behavior is documented in the [`adjacency` parameter documentation](https://mne.tools/stable/generated/mne.stats.spatio_temporal_cluster_1samp_test.html?utm_source=chatgpt.com).&#x20;

[image](https://www.google.com/s2/favicons?domain=https://mne.tools\&sz=32)

MNE 1.13.2 documentation+1



## 2. Is this OK?

Generally, I would not recommend it for sensor-level EEG or MEG data.

The problem is that your cluster definition depends on the ordering of channels in your input array.

For example, if your channels are ordered alphabetically, two physically distant sensors might become neighbors, while two physically adjacent sensors might not be connected.

This has implications for:

- Which significant samples are grouped into clusters.
- The spatial extent of detected clusters.
- The cluster-level permutation statistics and resulting p-values.

The permutation procedure does not automatically correct an inappropriate adjacency structure. The adjacency structure is part of the statistical hypothesis being tested.

## 3. What should you use instead?

For sensor-level data, I recommend constructing adjacency from the actual sensor positions using `mne.channels.find_ch_adjacency()`.

For EEG:

```
import mneadjacency, ch_names = mne.channels.find_ch_adjacency(    info,    ch_type="eeg")
```

Then run:

```
T_obs, clusters, cluster_p_values, H0 = (    mne.stats.spatio_temporal_cluster_1samp_test(        X,        adjacency=adjacency,        n_permutations=1000,        threshold=None,        tail=0,        n_jobs=-1,        seed=42    ))
```

Here:

- `adjacency` specifies which EEG sensors are spatial neighbors.
- `max_step=1` (the default) specifies that immediately neighboring time samples can be connected.
- Clusters are formed using both spatial and temporal connectivity.

You should ensure that the channel ordering in `X` matches the ordering in `info` and the returned `ch_names`. Also ensure that your `info` contains an appropriate sensor montage.

For MEG, use the appropriate channel type (`"mag"` or `"grad"`).

See MNE's [sensor adjacency documentation](https://mne.tools/stable/generated/mne.channels.find_ch_adjacency.html?utm_source=chatgpt.com) and [spatiotemporal clustering tutorial](https://mne.tools/stable/auto_tutorials/stats-source-space/20_cluster_1samp_spatiotemporal.html?utm_source=chatgpt.com).&#x20;

[image](https://www.google.com/s2/favicons?domain=https://mne.tools\&sz=32)

MNE 1.13.2 documentation+1



## 4. One important distinction

There are three different adjacency choices worth distinguishing:

| Setting                      | Spatial connectivity        | Temporal connectivity         |
| ---------------------------- | --------------------------- | ----------------------------- |
| `adjacency=None`             | Consecutive channel indices | Yes                           |
| `adjacency=False`            | No spatial connectivity     | No spatial clustering         |
| `adjacency=adjacency_matrix` | Actual sensor neighbors     | Yes, controlled by `max_step` |

For your application, the third option is generally the most appropriate.

My recommendation: Use `find_ch_adjacency()` for EEG/MEG sensor-level cluster permutation tests rather than relying on `adjacency=None`. This makes your spatial cluster definition reflect the actual sensor geometry rather than an arbitrary ordering of channels.
