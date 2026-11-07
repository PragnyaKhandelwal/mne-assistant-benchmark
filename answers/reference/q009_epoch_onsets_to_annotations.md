```python
annot = mne.annotations_from_events(epochs.events, raw.info["sfreq"],
    event_desc={e: "kept" for e in set(epochs.events[:, 2])}, first_samp=raw.first_samp)
raw.set_annotations(raw.annotations + annot)
```
