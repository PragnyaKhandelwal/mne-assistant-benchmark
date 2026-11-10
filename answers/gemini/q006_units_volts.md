MNE-Python stores EEG data in **Volts (V)**. Because your data is in microvolts ($\mu V$), you must multiply `data` by $10^{-6}$ before passing it to `mne.EpochsArray`. If you skip this step, MNE's plotting functions (which automatically scale inputs to $\mu V$ for display) will display your amplitudes scaled up by a factor of one million.

```python
import mne

# 1. Convert data from microvolts (uV) to Volts (V)
data_volts = data * 1e-6

# 2. Create MNE info structure (sets channel types to 'eeg')
info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types="eeg")

# 3. Instantiate the Epochs object (set tmin if your epoch starts before 0 s)
epochs = mne.EpochsArray(data_volts, info, tmin=-0.2)

```

### Key Parameters to Adjust

* **`tmin`**: Sets the start time of each epoch relative to timepoint 0 (defaults to `0.0` seconds if omitted). Adjust `tmin=-0.2` to match your pre-stimulus window.
* **`events` & `event_id**`: If omitted, MNE automatically creates dummy event codes (`1`) occurring at `tmin` for every epoch. You can pass a custom $(N, 3)$ integer array to `events` if you have event markers.
