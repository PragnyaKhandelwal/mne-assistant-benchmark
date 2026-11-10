The key point: if you downsample `raw` *after* extracting events, the event sample indices no longer match the new sampling rate. There are two safe ways to handle it.

**Option 1 (recommended): resample raw and events together**

```python
raw_resampled, events_resampled = raw.copy().resample(250, events=events)

epochs = mne.Epochs(
    raw_resampled,
    events_resampled,
    tmin=-0.2,
    tmax=0.5,
    baseline=(None, 0),   # default; set to None to disable
    preload=True,
)
```

Passing `events=events` makes MNE rescale the event sample indices to the new rate and return them alongside the data.

**Option 2: epoch first, then decimate/resample the epochs**

```python
epochs = mne.Epochs(
    raw, events,
    tmin=-0.2, tmax=0.5,
    baseline=(None, 0),
    preload=True,
)
epochs.resample(250)
```

This avoids event-timing issues entirely, but it needs more memory up front because the 1000 Hz epochs are loaded before being reduced.

**Notes**

- Use `raw.copy().resample(...)` if you want to keep the original `raw`; drop `.copy()` to resample in place and save memory (then `raw, events = raw.resample(250, events=events)`).
- Resample applies an anti-aliasing low-pass filter. If you plan to filter anyway, high-pass/low-pass filter the raw data *before* resampling, and keep the low-pass cutoff well below the new Nyquist (125 Hz).
- Raw data must be preloaded for `resample`. If it isn't, call `raw.load_data()` first (or load with `preload=True`).
- Don't just do `raw.resample(250)` and reuse the old `events`. The timing would be off by a factor of 4. Event times can also be rounded to the nearest new sample, so small jitter (up to ~2 ms) is possible. If you need exact timing, Option 2 or `raw.resample(250, events=events)` with trigger-sample alignment checks is worth considering.
- If you pass `event_id`, keep it consistent with the events array in both cases.

Option 1 gives you the memory savings you wanted, since you only ever hold the 250 Hz data (the original `raw` can be freed afterward with `del raw`).
