Since your original sampling rate is 1000 Hz and your target is 250 Hz, the downsampling factor is 4.

For accurate event timing, I recommend creating epochs first and then downsampling the epochs. This avoids resampling the continuous `raw` data before epoching, which can introduce small timing shifts in event onsets.

### Recommended code

```
import mne# 1. Create epochs at the original sampling rate (1000 Hz)epochs = mne.Epochs(    raw,    events,    event_id=None,       # Include all event codes    tmin=-0.2,    tmax=0.5,    baseline=None,    preload=True)# 2. Downsample epochs from 1000 Hz to 250 Hzepochs.resample(250)# 3. Verify sampling rate and dimensionsprint("Sampling frequency:", epochs.info['sfreq'])print("Epoch shape:", epochs.get_data().shape)
```

### Even better: avoid epoch-edge resampling artifacts

MNE's recommended workflow is to low-pass filter the continuous data before downsampling, then decimate the epochs.

```
# 1. Low-pass filter continuous data to prevent aliasingraw_filt = raw.copy()raw_filt.filter(    l_freq=None,    h_freq=80.0,    picks='eeg')# 2. Create epochs and decimate by a factor of 4epochs = mne.Epochs(    raw_filt,    events,    event_id=None,    tmin=-0.2,    tmax=0.5,    baseline=None,    preload=True,    decim=4)# Check resultsprint("Sampling frequency:", epochs.info['sfreq'])print("Epoch dimensions:", epochs.get_data().shape)
```

The 80 Hz low-pass filter provides a margin below the new Nyquist frequency (125 Hz), helping prevent aliasing.

### Expected output

- Original sampling rate: 1000 Hz
- New sampling rate: 250 Hz
- Epoch duration: −0.2 to 0.5 seconds
- Samples per epoch: approximately 176 (including both endpoints)
- Memory usage: approximately 75% lower for the epoch data.

My recommendation: Use the second approach for your EEG ERP and source-localization pipeline, provided 80 Hz is an appropriate upper frequency limit for your analysis.

Reference: [MNE-Python: Filtering and resampling data](https://mne.tools/stable/auto_tutorials/preprocessing/30_filtering_resampling.html?utm_source=chatgpt.com).
