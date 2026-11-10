To add standard 10-20 electrode positions to your `raw` object in MNE-Python 1.13, use `mne.channels.make_standard_montage()` combined with the `.set_montage()` method.

By default, `.set_montage()` operates **in place** on MNE data objects.

### Code Example

```python
import mne

# 1. Create the standard 10-20 montage object
montage = mne.channels.make_standard_montage('standard_1020')

# 2. Apply it to your raw object in place
raw.set_montage(montage)

```

### Tips & Common Pitfalls

* **Channel Name Matching:** MNE matches channel names case-insensitively, but names must match standard conventions (e.g., `Fp1`, `Fz`, `Cz`). If your channel names have extra prefixes/suffixes (like `EEG Fp1` or lowercase letters), you may need to rename them first using `raw.rename_channels()` before setting the montage.
* **Handling Missing/Extra Channels:** If your `raw` object contains non-EEG channels (like EOG, ECG, or STIM) or custom channels not present in the standard 10-20 template, MNE-Python will normally raise an error. You can bypass this by telling MNE how to handle missing electrodes:
```python
raw.set_montage(montage, on_missing='ignore')

```
