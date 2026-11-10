To mark the span of each remaining epoch as an annotation in `raw`, compute the onset times using `epochs.events` (which automatically excludes dropped epochs) and update `raw.annotations` in place.

```python
import mne

# 1. Compute onset times (in seconds) and durations for the kept epoch windows
onsets = (epochs.events[:, 0] - raw.first_samp) / raw.info["sfreq"] + epochs.tmin
durations = epochs.tmax - epochs.tmin

# 2. Create an Annotations object for remaining epochs
kept_annot = mne.Annotations(
    onset=onsets,
    duration=durations,
    description="kept",
    orig_time=raw.info["meas_date"]
)

# 3. Add to existing raw annotations and update raw in place
raw.set_annotations(raw.annotations + kept_annot)

```

### Key Details

* **`epochs.events` filters dropped epochs automatically:** When epochs are dropped during cleaning, MNE removes their corresponding rows from `epochs.events`. Only surviving epochs remain.
* **Accounting for `raw.first_samp` & `tmin`:** `epochs.events[:, 0]` contains sample indices relative to the start of file acquisition. Subtracting `raw.first_samp` converts this to continuous time within `raw`, and adding `epochs.tmin` aligns the annotation with the exact start of the epoch window.
* **Shading epoch windows in `raw.plot()`:** Passing `duration = epochs.tmax - epochs.tmin` draws a colored box across the entire epoch duration in `raw.plot()` rather than displaying a single point marker.
