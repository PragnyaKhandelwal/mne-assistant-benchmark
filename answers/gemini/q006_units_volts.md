To create an MNE-Python `Epochs` object from a NumPy array where values are in **microvolts ($\mu V$)**, you need to take into account that MNE-Python expects internal data units to be in **Volts ($V$)**.

If you pass microvolts directly without conversion, MNE will treat them as Volts and scale them incorrectly during plotting. Therefore, you must multiply your data by $10^{-6}$ before passing it to `mne.EpochsArray`.

Here is the complete code to accomplish this:

```python
import mne
import numpy as np

# Given variables: data, ch_names, sfreq, and tmin (start time of each epoch in seconds)
# data shape: (n_epochs, n_channels, n_times)
tmin = 0.0  # Adjust this to your epoch's start time relative to the event (e.g., -0.2 for a 200ms baseline)

# 1. Create the Info object
info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types='eeg')

# 2. Convert data from microvolts (uV) to Volts (V)
# MNE expects Volts internally and automatically converts them to uV for display/plotting.
data_volts = data * 1e-6

# 3. Create the EpochsArray
# If you have a custom events array, pass it via `events=events`.
# If `events=None`, MNE will automatically generate sequential dummy events.
epochs = mne.EpochsArray(data_volts, info, tmin=tmin)

```

### Key Details to Keep in Mind:

* **Unit Scaling:** MNE-Python plotting functions (like `epochs.plot()` or `epochs.average().plot()`) automatically scale Volts to microvolts ($\mu V$) for EEG channels. By converting your input array to Volts (`data * 1e-6`), MNE's internal math and plotting scales will align perfectly.
* **Event Timing (`tmin`):** Be sure to set `tmin` correctly if your epochs start before the time-locking event (e.g., `-0.2` seconds for a pre-stimulus baseline).
