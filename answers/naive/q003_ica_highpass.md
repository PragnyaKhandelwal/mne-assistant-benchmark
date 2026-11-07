```python
ica = mne.preprocessing.ICA(n_components=10, random_state=97, max_iter="auto")
ica.fit(raw)
```
