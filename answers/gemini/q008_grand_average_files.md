```python
import mne

# 1. Read the Evoked object from each participant's file
evokeds = [mne.read_evokeds(fname)[0] for fname in fnames]

# 2. Compute the grand average across all participants
grand_avg = mne.grand_average(evokeds)

```

### Key Notes

* **List indexing (`[0]`):** `mne.read_evokeds()` returns a list of `Evoked` objects (even when a file contains only one condition). Indexing `[0]` extracts the single `Evoked` instance per subject into a clean list.
* **Equalizing channels:** `mne.grand_average()` automatically handles channel alignment across participants, dropping any channels that are not present in all datasets.
