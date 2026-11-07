```python
info = mne.create_info(ch_names, sfreq, "eeg")
epochs = mne.EpochsArray(data, info)
```
