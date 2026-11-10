## What's going on

An average reference subtracts the mean across all included channels from every channel. If one or more channels are bad (flat, disconnected, very noisy, or carrying large drift or line noise) and aren't marked as bad, their noise is in that mean. It is then subtracted from every channel, so every channel gets the same inverted copy of the bad channel's artifact. That is why the fluctuations look identical across channels and weren't there before.

Common culprits:
- an unmarked bad electrode
- a non-EEG channel (EOG, ECG, mastoid, trigger, etc.) still typed as `'eeg'`
- a very noisy channel that the average amplifies

The re-reference modifies the data in place, so you can't cleanly undo it. Reload the data and redo it in the right order.

## Fix

Mark bads, then re-reference. MNE excludes channels in `raw.info['bads']` from the average by default.

```python
import numpy as np
import mne
from scipy.stats import median_abs_deviation

# 1. Reload the raw data (the contaminated reference can't be undone)
raw = mne.io.read_raw_fif("your_file_raw.fif", preload=True)  # use the reader for your format

# 2. Make sure non-EEG channels aren't typed as EEG (edit names to match yours)
raw.set_channel_types({"EOG1": "eog", "EOG2": "eog"})

# 3. Make sure a montage is set (needed for interpolation)
raw.set_montage("standard_1020", on_missing="warn")

# 4. Flag bad channels (inspect visually too: raw.plot())
eeg_picks = mne.pick_types(raw.info, eeg=True, exclude=[])
data = raw.get_data(picks=eeg_picks)
ch_std = data.std(axis=1)
robust_z = (ch_std - np.median(ch_std)) / (1.4826 * median_abs_deviation(ch_std))
bads = [raw.ch_names[i] for i, z in zip(eeg_picks, robust_z) if abs(z) > 5]
raw.info["bads"] = sorted(set(raw.info["bads"]) | set(bads))
print("Bad channels:", raw.info["bads"])

# 5. Average reference excluding bads (default behavior), then interpolate,
#    then re-apply so the final reference includes the repaired channels
raw.set_eeg_reference("average", projection=False)   # bads excluded from the mean
raw.interpolate_bads(reset_bads=True)
raw.set_eeg_reference("average", projection=False)   # final, clean average reference
```

## Notes
- Mark bads before referencing, not after. Marking them afterward doesn't remove their contribution from the data.
- Re-applying the average after interpolation is cheap and keeps the data exactly zero-mean across channels.
- Filtering first (e.g. 0.1 or 1 Hz high-pass) helps both bad-channel detection and the reference, since slow drifts in one channel otherwise leak into all the others.
- If you use `projection=True`, MNE adds the reference as an SSP projector that isn't applied until `raw.apply_proj()`. Excluding bads works the same way, but the plot will look different until you apply it.
- A quick check that it worked: `raw.get_data(picks="eeg").mean(axis=0)` should be near zero at every timepoint, and the common-mode noise should be gone.
