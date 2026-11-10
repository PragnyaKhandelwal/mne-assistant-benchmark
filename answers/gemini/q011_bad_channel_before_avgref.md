### What is Going On?

When you compute an **average reference**, the software calculates the mean signal across *all* included EEG channels at every time point and subtracts that mean from each individual channel.

If your recording contains a **bad or malfunctioning channel** with massive noise, a movement artifact, or a rail artifact (disconnection), and that channel was **not** marked as bad beforehand, its extreme fluctuations get factored into the global average. When this contaminated average is subtracted from every single channel, that local noise is injected globally into your entire montage. Consequently, every channel suddenly appears to share those exact same large, noisy fluctuations.

---

### How to Fix It

To fix this, you need to explicitly tell MNE-Python which channel is causing the issue by adding it to `raw.info['bads']` *before* applying the average reference. MNE automatically excludes any channels listed in `raw.info['bads']` when calculating the average reference.

Here is the correct workflow in Python:

```python
import mne

# 1. If 'raw' was already corrupted in-place, reload or copy a clean version
# (e.g., raw = mne.io.read_raw_fif('your_data_raw.fif', preload=True))
raw.load_data()  # Ensure data is loaded into memory

# 2. Identify the noisy channel(s) and mark them as bad
# Replace 'EEG 0XX' with the actual name of the rogue channel(s)
raw.info['bads'] = ['EEG 0XX']

# 3. Apply the average reference.
# MNE will automatically exclude any channels listed in raw.info['bads']
raw.set_eeg_reference(ref_channels='average', projection=False)

# 4. (Optional but recommended) Interpolate the bad channel
# so you don't lose spatial data coverage
raw.interpolate_bads(reset_bads=True)

```

### Pro-Tip for Finding the Culprit

If you aren't sure which channel is causing the issue:

1. Re-load your raw data *without* the average reference.
2. Plot the data using `raw.plot(block=True)`.
3. Visually scan for any flat lines, clipping, or wildly erratic channels, and **click on their channel names** in the interactive MNE plot window to flag them red as `bads`.
4. Close the plot window and then run the snippet above.
