Since Cz was the recording reference, every channel in the file is measured relative to Cz, and Cz itself is an implicit all-zeros signal. If you average-reference without Cz, you average over N-1 electrodes and the result is biased, particularly with few channels. The fix is to add Cz back as a flat channel, then re-reference. I'm assuming you're using MNE-Python.

```python
import mne

raw.load_data()  # data must be in memory to add a channel

# 1. Add Cz back as an all-zero EEG channel (modifies raw in place)
mne.add_reference_channels(raw, ref_channels="Cz", copy=False)

# 2. Give it (and everything else) a position
montage = mne.channels.make_standard_montage("standard_1020")  # or your own montage
raw.set_montage(montage, on_missing="warn")

# 3. Re-reference to the average of all EEG channels (including Cz)
raw.set_eeg_reference("average", projection=False)
```

Some details that matter:

- **Order of steps:** Add Cz before setting the montage. The new channel has no electrode position until you assign one, and the montage step is what gives it one (useful for topomaps and source work).
- **Include Cz in the average:** Because Cz is now a real channel in `raw`, it's included automatically. That is what makes this a true average reference.
- **Bad channels:** MNE excludes channels in `raw.info["bads"]` from the average by default. Mark bads *before* step 3 so they don't contaminate the reference. Cz is not marked bad, so it stays in the average.
- **Non-EEG channels:** EOG, ECG, and the like are left alone. Only EEG-type channels are used.
- **`projection=False`:** This applies the reference directly to the data. With `projection=True` it would be added as an SSP projector that you'd have to apply later (`raw.apply_proj()`).
- **Montage naming:** If your channel names don't match the standard 10-20 names (e.g. different case or a prefix), `set_montage` will warn about missing positions. You can fix that with `raw.rename_channels(...)` first.

Afterwards you can confirm with `raw.info["custom_ref_applied"]` and by checking that the mean across EEG channels is ~0 at each time point:

```python
import numpy as np
data = raw.get_data(picks="eeg")
print(np.abs(data.mean(axis=0)).max())  # should be ~1e-20 or so
```
