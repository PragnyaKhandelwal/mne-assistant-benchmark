Use MNE-Python's `mne.grand_average()` function. It computes the grand average across participants from their individual `Evoked` objects.

```
import mne# Load each participant's Evoked fileevokeds = [mne.read_evokeds(fname, condition=0) for fname in fnames]# Compute grand averagegrand_avg = mne.grand_average(evokeds)# Inspect the resultprint(grand_avg)
```

### Plot the grand average

```
# Plot ERP waveformsgrand_avg.plot()# Plot topographic mapsgrand_avg.plot_topomap(times=[0.1, 0.2, 0.3, 0.4])
```

### Save the grand average (optional)

```
grand_avg.save('grand_average-ave.fif', overwrite=True)
```

### Important notes

- All participants should have compatible channel names, channel types, sampling frequencies, and time points.
- `mne.grand_average()` interpolates bad channels by default (`interpolate_bads=True`).
- It excludes channels marked as bad in individual participants from the corresponding grand-average calculation.
- The result is an equally weighted average across participants, not a trial-count-weighted average.

For your EEG group-level ERP analysis, this is the standard approach.
