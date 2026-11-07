```python
filt_raw = raw.copy().filter(l_freq=1.0, h_freq=None)
ica = mne.preprocessing.ICA(n_components=10, random_state=97, max_iter="auto")
ica.fit(filt_raw)
```
