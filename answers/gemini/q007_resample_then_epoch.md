You can achieve this in MNE-Python by using the `resample` method on your `raw` object followed by `mne.Epochs`:

```python
import mne

# 1. Downsample the raw data to 250 Hz
raw.resample(250)

# 2. Create epochs from -0.2 to 0.5 seconds around the events
epochs = mne.Epochs(raw, events, tmin=-0.2, tmax=0.5)

```

> **Note:** If you haven't already applied a low-pass filter to your raw data, it is strongly recommended to filter your data (e.g., below the new Nyquist frequency of 125 Hz) *before* resampling to prevent aliasing artifacts.
