Use `epochs.events`. Its first column holds the sample index of each *kept* epoch's time-locking event (counted in the original `raw`, including `raw.first_samp`), and `epochs.tmin` gives the offset from that event to the epoch start. Dropped epochs are already removed from it.

```python
sfreq = raw.info["sfreq"]  # use raw's sfreq, since events are in raw samples
                           # (epochs.info["sfreq"] may differ if you decimated)

onsets = epochs.events[:, 0] / sfreq + epochs.tmin
durations = np.full(len(onsets), epochs.tmax - epochs.tmin)

raw.annotations.append(onset=onsets, duration=durations, description="kept")

raw.plot()
```

Notes:

- `events[:, 0]` already includes `raw.first_samp`, so dividing by `sfreq` puts the onset on the same time reference that `raw.annotations` uses. Don't subtract `first_samp` here.
- `raw.annotations.append(...)` modifies `raw` in place and keeps any existing annotations (e.g. `BAD_` segments). Don't use `raw.set_annotations(new)` unless you want to replace them.
- If you only want a marker at the epoch start rather than a span, use `duration=0`.
- If you want the annotation to cover the last sample too, use `epochs.tmax - epochs.tmin + 1 / sfreq`.
- If you cropped `raw` after making the epochs, the onsets may no longer line up, so build the annotations from the same `raw` that the epochs came from.
