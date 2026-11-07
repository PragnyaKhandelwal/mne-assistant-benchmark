```python
annot, scores = mne.preprocessing.annotate_muscle_zscore(raw, ch_type="eeg", threshold=4)
raw.set_annotations(raw.annotations + annot)
epochs = mne.Epochs(raw, events, tmin=-0.2, tmax=0.5, preload=True)
```
