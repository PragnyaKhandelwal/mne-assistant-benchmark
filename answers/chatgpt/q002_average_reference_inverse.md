For EEG source localization with MNE-Python (e.g., dSPM), the recommended approach is to use an average reference projector rather than immediately modifying the data.

Use:

```
raw.set_eeg_reference('average', projection=True)
```

This adds an average-reference projector to `raw` without immediately changing the EEG samples. It also allows MNE to account for the reference when constructing the inverse operator.

### Recommended complete code

```
# Mark bad EEG channels before adding the average reference# (if you haven't already done so)raw.info['bads'] = ['EEG 001']  # Replace with your actual bad channels# Add average EEG reference as a projectorraw.set_eeg_reference(ref_channels='average', projection=True)# Check that the projector was addedprint(raw.info['projs'])
```

If you have already marked bad channels, don't overwrite `raw.info['bads']`.

### Should you call `raw.apply_proj()`?

Not necessarily. You can leave the projector unapplied:

```
# Optional: explicitly apply all pending projectorsraw.apply_proj()
```

For source localization, I recommend keeping the average reference as a projector and allowing MNE to handle it consistently during source estimation.

### Important considerations

1. Bad channels: Mark bad EEG channels before creating the reference. They will be excluded from the average.
2. Electrode positions: Make sure your EEG montage and electrode positions are correctly specified before computing the forward solution.
3. Covariance: Use a consistent projector configuration when computing the noise covariance and inverse operator.

Bottom line: For EEG dSPM source localization, use:

```
raw.set_eeg_reference('average', projection=True)
```

This is the approach explicitly recommended in the [official MNE-Python documentation on EEG referencing](https://mne.tools/stable/auto_tutorials/preprocessing/55_setting_eeg_reference.html?utm_source=chatgpt.com).&#x20;

[image](https://www.google.com/s2/favicons?domain=https://mne.tools\&sz=32)

MNE 1.13.2 documentation+1
