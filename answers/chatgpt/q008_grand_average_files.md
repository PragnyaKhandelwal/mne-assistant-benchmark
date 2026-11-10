Use MNE-Python's `mne.grand_average()` function:

```
evokeds = [mne.read_evokeds(fname, condition=0) for fname in fnames]grand_avg = mne.grand_average(evokeds)
```

Since each file contains a single condition, `condition=0` selects that condition from each file. `grand_avg` now contains the grand average across participants.
