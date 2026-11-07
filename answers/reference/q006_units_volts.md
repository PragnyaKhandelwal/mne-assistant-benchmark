```python
info = mne.create_info(ch_names, sfreq, "eeg")
epochs = mne.EpochsArray(data * 1e-6, info)
```
