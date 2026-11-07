```python
epochs = mne.Epochs(raw, events, tmin=-0.2, tmax=0.5, preload=True)
epochs.resample(250)
```
