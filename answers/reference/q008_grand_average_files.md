```python
evokeds = [mne.read_evokeds(f, condition=0) for f in fnames]
grand_avg = mne.grand_average(evokeds)
```
