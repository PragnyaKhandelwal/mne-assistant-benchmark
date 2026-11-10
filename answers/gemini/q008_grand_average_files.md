To compute the grand average across participants in MNE-Python, you need to read the `Evoked` object from each file in your `fnames` list and pass them into `mne.grand_average()`.

Here is how you can do it:

```python
import mne

# Load the single-condition Evoked object from each participant's file
evokeds = [mne.read_evokeds(fname, verbose=False)[0] for fname in fnames]

# Compute the grand average
grand_avg = mne.grand_average(evokeds)

```

### Key Details:

* **`mne.read_evokeds(fname)`** always returns a list of `Evoked` objects (even if the file contains only one condition), which is why indexing with `[0]` is used.
* **`mne.grand_average(evokeds)`** computes the grand average across the list of loaded `Evoked` instances, automatically handling weighting if participant trial counts differ (unless specified otherwise).
