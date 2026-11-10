To re-reference your MNE-Python `raw` object to the **average reference** (which is standard practice before computing a forward model and running source localization like dSPM), you can use the `set_eeg_reference()` method.

### Python Code

```python
import mne

# 1. (Optional but recommended) Ensure bad channels are marked,
# as the average reference automatically excludes channels in raw.info['bads']
# raw.info['bads'] = ['EEG024']  # example bad channel

# 2. Ensure data is loaded into memory (required if projection=False)
raw.load_data()

# 3. Apply the average reference directly in-place
raw.set_eeg_reference(ref_channels='average', projection=False)

```

---

### Important Best Practices for Source Localization:

1. **Mark Bad Channels First:** The average reference calculates the mean across all good EEG channels. If you have noisy, dead, or bridging channels, **make sure to mark them in `raw.info['bads']**` *before* re-referencing, otherwise they will heavily skew your average reference.
2. **Alternative (Using Projectors):** Instead of modifying the raw data array immediately, you can add the average reference as a Signal Space Projection (SSP):
```python
raw.set_eeg_reference(ref_channels='average', projection=True)

```


*Why use this?* MNE's covariance estimation and inverse operator functions will automatically apply active SSP projectors, leaving your raw time-series data un-subtracted until needed (which is useful if you want to keep the option to inspect un-referenced or alternative references later).
