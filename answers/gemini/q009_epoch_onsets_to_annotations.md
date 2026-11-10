To mark the start of each remaining (kept) epoch as an annotations layer in your original `raw` object, you can extract the sample indices from `epochs.events`, convert them to seconds, create an `mne.Annotations` object, and add them to `raw` in place.

Here is how you can do it:

```python
import mne
import numpy as np

# 1. Get the sample indices of the kept epochs
event_samples = epochs.events[:, 0]

# 2. Convert sample indices to time in seconds (accounting for raw.first_samp)
onsets = (event_samples - raw.first_samp) / raw.info["sfreq"]

# 3. Define durations (0 for a point marker, or span the full epoch window)
# Option A: Zero duration point markers at the epoch onset
durations = np.zeros_like(onsets)

# Option B (Alternative): Span the entire epoch duration from tmin to tmax
# durations = np.full_like(onsets, epochs.tmax - epochs.tmin)
# onsets = onsets + epochs.tmin  # Shift onset to the true start of the epoch window

# 4. Create the Annotations object
kept_annotations = mne.Annotations(
    onset=onsets,
    duration=durations,
    description=["kept"] * len(onsets)
)

# 5. Add them to raw in place (combining with any existing annotations)
if raw.annotations is not None and len(raw.annotations) > 0:
    raw.set_annotations(raw.annotations + kept_annotations)
else:
    raw.set_annotations(kept_annotations)

# Now you can view them in the plot window
raw.plot()

```

### Explanation:

* **`epochs.events[:, 0]`**: When you drop bad epochs, `epochs.events` is automatically filtered to contain **only** the events corresponding to the remaining, accepted epochs.
* **`raw.first_samp`**: Subtracting `raw.first_samp` ensures the time alignment is correct if your raw data file starts at a non-zero sample index.
* **`raw.set_annotations(...)`**: Modifies the `raw` object in place. By adding `raw.annotations + kept_annotations`, you preserve any pre-existing annotations already present in your `raw` instance.
