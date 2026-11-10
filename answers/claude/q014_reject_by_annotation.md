Assuming `raw` is an `mne.io.Raw` object, MNE can drop the annotated spans for you:

```python
import numpy as np

# Drops every sample covered by an annotation whose description starts with "bad" (case-insensitive, so BAD_* matches)
data = raw.get_data(reject_by_annotation="omit")   # shape (n_channels, n_clean_samples)

variances = np.var(data, axis=1)                    # shape (n_channels,)
```

- **Mean and variance use only clean samples.** `"omit"` removes the bad spans entirely, so neither the mean nor the variance is affected by them. Don't use `reject_by_annotation="NaN"` here unless you switch to `np.nanvar`.
- **Sample vs. population variance.** `np.var` defaults to `ddof=0`. Use `np.var(data, axis=1, ddof=1)` if you want the unbiased estimate.
- **Channel selection.** `get_data()` includes every channel in `raw`, which may include stim/EOG/ECG channels. If you only want data channels, pick them first, but then the array length won't equal `len(raw.ch_names)`:
  ```python
  data = raw.get_data(picks="data", reject_by_annotation="omit")
  ```
- **Sanity check.** Confirm that the annotations are what you expect and that some data remains:
  ```python
  print(set(raw.annotations.description))
  print(data.shape, variances.shape)
  ```
- **Units.** The values are in the channels' native units (e.g., V² for EEG/MEG), so they will look tiny. Multiply by `1e12` for µV² if you want readable numbers.

If `raw` isn't an MNE object, tell me what it is (plain NumPy array plus a list of annotation onsets/durations, for example) and I'll adapt the code.
