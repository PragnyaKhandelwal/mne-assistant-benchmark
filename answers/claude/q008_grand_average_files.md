Use `mne.read_evokeds` to load each file, then `mne.grand_average` to combine them:

```python
import mne

# Each file holds a single condition, so condition=0 (or the default first entry) returns one Evoked
evokeds = [mne.read_evokeds(fname, condition=0) for fname in fnames]

grand_avg = mne.grand_average(evokeds)
```

**Notes**

- `read_evokeds` normally returns a list, even for a single condition. Passing `condition=0` (an index) or the condition's name returns the `Evoked` object itself, which is what `grand_average` expects.
- If you'd rather not use `condition=`, you can unpack the list instead: `[mne.read_evokeds(f)[0] for f in fnames]`.
- `grand_average` requires the same channels, time points, and sampling rate in every file. By default it also **interpolates bad channels** (`interpolate_bads=True`) and drops channels that aren't shared across all participants (`drop_bads=True` handles the rest). If participants have different bad channels, this is usually what you want, but check `grand_avg.info['bads']` afterward.
- The result is an `Evoked` object whose `nave` is the sum of the individual `nave` values, and `grand_avg.comment` is set to `'Grand average (n = N)'`.
- If your files have different head positions or sensor layouts (e.g., MEG with different head origins), the grand average is only meaningful after you've aligned them, for example with `mne.channels.equalize_channels` or by transforming to a common head position before saving.

A quick sanity check and plot:

```python
print(grand_avg)
grand_avg.plot_joint()
```
