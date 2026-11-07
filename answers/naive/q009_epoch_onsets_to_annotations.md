```python
onsets = epochs.events[:, 0] / raw.info["sfreq"] + raw.first_time
raw.set_annotations(mne.Annotations(onsets, 4.99, "kept"))
```
