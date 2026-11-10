To correctly re-reference your EEG data to the average reference when the original reference electrode (`Cz`) is missing from the file, you must first **add `Cz` back as a zero-filled channel**.

If you apply an average reference without adding `Cz` back first, the average will be calculated incorrectly (divided by $N$ channels instead of $N + 1$), biasing your data.

Here is how to do this correctly in MNE-Python, leaving the result directly in `raw`:

```python
import mne

# 1. Add Cz back as a zero-filled reference channel
raw = mne.add_reference_channels(raw, ref_channels=['Cz'], copy=False)

# 2. Re-reference to the average of all channels (including Cz)
raw.set_eeg_reference(ref_channels='average', copy=False)

```

### Verification

* **Check channel count:** Run `print(len(raw.ch_names))` before and after adding `Cz` to confirm that `Cz` has been successfully appended to the channel list.
* **Check signal values:** Inspect `raw.get_data()` or plot a short segment (`raw.plot()`) to verify that `Cz` shows a valid signal after the average reference has been subtracted.
