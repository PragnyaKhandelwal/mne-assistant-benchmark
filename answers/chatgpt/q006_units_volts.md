MNE expects EEG data in volts (V), whereas your NumPy array contains microvolts (µV). You must therefore multiply `data` by \\(10^{-6}\\) before creating the `Epochs` object.

The simplest approach is to use `mne.EpochsArray`:

```
import mneimport numpy as np# Convert microvolts to voltsdata_volts = data * 1e-6# Create channel informationinfo = mne.create_info(    ch_names=ch_names,    sfreq=sfreq,    ch_types='eeg')# Create MNE Epochs objectepochs = mne.EpochsArray(    data_volts,    info,    tmin=0,    baseline=None)
```

For ERP plotting, you can then use:

```
evoked = epochs.average()evoked.plot()
```

Or plot selected channels:

```
evoked.plot(picks=['Cz', 'Pz', 'Fz'])
```

Important notes:

- Set `tmin` to the actual epoch start time (e.g. `-0.2` if epochs start 200 ms before stimulus onset).
- Use `baseline=(None, 0)` instead of `baseline=None` if you want baseline correction using the pre-stimulus interval.
- MNE automatically displays EEG amplitudes in µV when plotting, even though the internal data are stored in volts.

The key is multiply by `1e-6` exactly once. Do not multiply again when plotting.

References: [MNE EpochsArray documentation](https://mne.tools/1.8/generated/mne.EpochsArray.html?utm_source=chatgpt.com) and [MNE creating data structures tutorial](https://mne.tools/dev/auto_tutorials/simulation/10_array_objs.html?utm_source=chatgpt.com).
