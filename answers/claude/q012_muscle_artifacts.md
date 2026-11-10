In MNE-Python, the standard approach is to detect muscle artifacts from high-frequency power, annotate them as `BAD_` segments, and let `Epochs` drop any epoch that overlaps them.

```python
import numpy as np
import matplotlib.pyplot as plt
import mne
from mne.preprocessing import annotate_muscle_zscore

# 1. Detect muscle bursts (z-scored 110-140 Hz power, averaged across channels)
threshold_muscle = 5  # z-score; tune this by inspecting the scores (see below)
annot_muscle, scores_muscle = annotate_muscle_zscore(
    raw,
    ch_type="eeg",
    threshold=threshold_muscle,
    min_length_good=0.1,   # merge bad segments separated by <0.1 s of "good" data
    filter_freq=(110, 140),
)

# 2. Check that the threshold is sensible
fig, ax = plt.subplots()
ax.plot(raw.times, scores_muscle)
ax.axhline(threshold_muscle, color="r")
ax.set(xlabel="Time (s)", ylabel="Muscle z-score")

# 3. Add the annotations to the data (keeps existing annotations)
raw.set_annotations(raw.annotations + annot_muscle)

# 4. Epoch all events; epochs overlapping BAD_ annotations are dropped
epochs = mne.Epochs(
    raw,
    events,
    event_id=None,            # use all events in the array
    tmin=-0.2,
    tmax=0.5,
    baseline=(None, 0),
    reject_by_annotation=True,  # default, shown explicitly for clarity
    preload=True,
)

# 5. Verify what was dropped and why
print(epochs.drop_log_stats())
epochs.plot_drop_log()
```

Some practical points:

- **Sampling rate:** the default 110-140 Hz band requires a sampling rate above 280 Hz. If your data are lower, change `filter_freq` to a band below Nyquist, such as 40-Nyquist-ish, and expect a less specific muscle signature.
- **Don't low-pass first:** do this detection on data that haven't been low-pass filtered below ~140 Hz. A typical 1-40 Hz filter would remove exactly the band you need. If `raw` is already filtered, run the detection on a copy of the unfiltered data and transfer the annotations (they're time-based), or run it before filtering.
- **Threshold:** 4-5 is a reasonable starting point. Inspect the scores plot, and use `raw.plot()` with the annotations visible to confirm the flagged segments really are muscle. Lower it if bursts are being missed, raise it if clean data are being flagged.
- **Partial overlap counts:** any epoch overlapping a `BAD_muscle` segment, even by one sample, is dropped. This is what you want here, but check `drop_log_stats()` so you know you aren't losing an excessive fraction of trials.
- **Annotation names:** `annotate_muscle_zscore` labels segments `BAD_muscle`, and the `BAD_` prefix is what makes `reject_by_annotation` act on them.
- **Bad channels:** mark bad channels (`raw.info["bads"]`) before running detection so a single noisy channel doesn't skew the average z-score.

I haven't run this on your data, so check the dropped-epoch count and the annotations visually before moving on.
