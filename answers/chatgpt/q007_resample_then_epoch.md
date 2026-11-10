```
# Downsample from 1000 Hz to 250 Hzraw.resample(250)# Create epochs around all events (-0.2 to 0.5 seconds)epochs = mne.Epochs(    raw,    events,    event_id=None,    tmin=-0.2,    tmax=0.5,    baseline=None,    preload=True)
```

Notes:

- `raw.resample(250)` modifies `raw` in place.
- `event_id=None` includes all event codes.
- `preload=True` loads the epochs into memory for processing.
- MNE automatically adjusts event sample indices during resampling when `events` are passed to `raw.resample`? Since you already extracted `events`, use this safer version instead:

```
raw.resample(250, events=events)
```

Use the returned events when creating epochs:

```
raw, events = raw.resample(250, events=events)
```
