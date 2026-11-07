```python
raw.resample(250)
epochs = mne.Epochs(raw, events, tmin=-0.2, tmax=0.5, preload=True)
```
