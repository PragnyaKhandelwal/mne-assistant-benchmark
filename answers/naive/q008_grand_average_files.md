```python
evokeds = [mne.read_evokeds(f) for f in fnames]
grand_avg = mne.grand_average(evokeds)
```
