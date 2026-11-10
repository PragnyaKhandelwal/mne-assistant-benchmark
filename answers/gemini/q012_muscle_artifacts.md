To find short bursts of muscle activity and exclude them from your epochs in MNE-Python, you can use **`annotate_muscle_zscore`** to automatically tag the muscle artifacts, and then pass the annotated `raw` object into **`mne.Epochs`** with `reject_by_annotation=True` (which is enabled by default).

Here is how you can do it:

```python
import mne
from mne.preprocessing import annotate_muscle_zscore

# 1. Automatically detect muscle artifact bursts in the raw data
# Adjust the threshold (e.g., 4.0) depending on your data's noise level
muscle_annotations, scores_muscle = annotate_muscle_zscore(
    raw,
    threshold=4.0,
    ch_type='eeg',
    filter_freq=(110, 140)
)

# 2. Add the detected muscle annotations to your raw object
raw.set_annotations(raw.annotations + muscle_annotations)

# 3. Create the epochs (-0.2 to 0.5 s around events)
# reject_by_annotation=True (default) automatically drops epochs overlapping with 'BAD_' annotations
epochs = mne.Epochs(
    raw,
    events,
    tmin=-0.2,
    tmax=0.5,
    reject_by_annotation=True,
    preload=True
)

```

### How it works:

1. **`annotate_muscle_zscore`**: Bandpass filters the data in a high-frequency range (typically 110–140 Hz where muscle artifact power dominates), computes z-scores, and creates `mne.Annotations` labeled as `BAD_muscle` for segments exceeding your threshold.
2. **`raw.set_annotations`**: Appends these bad segments to your existing `raw` annotations.
3. **`mne.Epochs`**: When `reject_by_annotation=True`, any epoch that overlaps with an annotation starting with `bad` (like `BAD_muscle`) is automatically discarded and logged in `epochs.drop_log`.
