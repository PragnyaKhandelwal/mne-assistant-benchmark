When downsampling `raw` after extracting `events`, you must resample both the continuous data and the event sample indices together. If you resample `raw` alone, the event timestamps (originally indexed at 1000 Hz) will become 4 times too large for the 250 Hz timebase.

Passing `events` directly to `raw.resample()` updates both the data and event indices in sync.

```python
import mne

# 1. Resample raw data and events together to 250 Hz
raw, events = raw.resample(sfreq=250.0, events=events)

# 2. Extract epochs (-0.2 to 0.5 s)
epochs = mne.Epochs(
    raw,
    events=events,
    tmin=-0.2,
    tmax=0.5,
    baseline=(-0.2, 0),
    preload=True
)

```

### Key Notes

* **In-Place Modification:** `raw.resample()` modifies the `raw` object in-place. If you want to keep your original 1000 Hz continuous recording in memory, use `raw_250, events_250 = raw.copy().resample(sfreq=250.0, events=events)`.
* **Anti-Aliasing Filter:** `raw.resample()` automatically applies a low-pass anti-aliasing filter prior to downsampling, preventing high-frequency noise from folding into your resampled data.
* **`preload=True`:** Loading epoch data into memory allows immediate manipulation, plotting, or saving without relying on the continuous `raw` data source.
