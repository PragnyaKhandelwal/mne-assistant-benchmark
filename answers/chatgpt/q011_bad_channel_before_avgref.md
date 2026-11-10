This is most likely a bad-channel contamination problem caused by the common average reference (CAR).

When you apply an average reference, EEG data from every included channel contribute to a common reference signal. That signal is then subtracted from every EEG channel.

Mathematically,

\\[ V_i^{\mathrm{referenced}}(t) = V_i(t)-\frac{1}{N}\sum\_{j=1}^{N}V_j(t) \\]

If one or more channels contain large noise, electrode artifacts, or unusually large fluctuations, they can dominate the average. Because that noisy average is subtracted from every channel, the same fluctuations suddenly appear across all channels.

The important point: Average referencing does not necessarily create new noise. It can spread the influence of existing noisy channels across the entire EEG recording.

## 1. How to fix it in MNE-Python

The solution is to identify bad EEG channels, mark them as bad, and then recompute the average reference.

MNE automatically excludes channels listed in `raw.info['bads']` from the average-reference calculation.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://mne.tools\&sz=32)

MNE 1.13.2 documentation+1



For example:

```
# Identify channels that are noisy or malfunctioningbad_channels = ['Fp1', 'T8']  # Replace with your actual bad channels# Mark them as badraw.info['bads'] = bad_channels# Recompute the average reference, in-placeraw.set_eeg_reference(ref_channels='average', projection=False)# Check the resultraw.plot()
```

The channel names above are examples. Only mark channels that you have actually identified as bad.

Important: If you have already applied average referencing, you can still recompute it after marking the bad channels. For the remaining good channels, subtracting their new average removes the old common reference offset.

## 2. A more careful preprocessing workflow

Ideally, identify bad channels before applying the reference. I recommend keeping an untouched copy of the original data:

```
# Preserve original, unreferenced dataraw_original = raw.copy()# Identify bad channels after inspecting the EEGbad_channels = ['Fp1', 'T8']  # Example only# Mark bad channelsraw.info['bads'] = bad_channels# Apply average referenceraw.set_eeg_reference(    ref_channels='average',    projection=False)# Plot the average-referenced dataraw.plot()
```

This modifies `raw` in-place, so your `raw` object remains the average-referenced recording.

## 3. How to identify the problematic channels

Before deciding which channels to exclude, inspect the original recording:

```
# Plot original data before average referencingraw_original.plot(    duration=10,    n_channels=32,    scalings='auto')
```

Look for channels with:

- Much larger amplitudes than neighboring channels.
- Persistent high-frequency noise.
- Sudden jumps or large irregular fluctuations.
- Flat signals or intermittent electrode contact.

You can also inspect the channel types:

```
print(raw.get_channel_types())print("Bad channels:", raw.info['bads'])
```

## 4. Verify that average referencing worked

For the good EEG channels, the instantaneous average should be approximately zero after average referencing.

```
import numpy as npimport mne# Get good EEG channel indicespicks = mne.pick_types(    raw.info,    eeg=True,    exclude='bads')# Extract EEG datadata = raw.get_data(picks=picks)# Calculate the average across good EEG channelsaverage_signal = np.mean(data, axis=0)print("Maximum residual average:",      np.max(np.abs(average_signal)))
```

The residual should be close to zero (allowing for floating-point precision).

## 5. One additional important consideration

If your original acquisition reference electrode was not included in the recorded channels, simply averaging the available electrodes can introduce a reference bias. MNE documents this situation and provides `mne.add_reference_channels()` to handle it.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://mne.tools\&sz=32)

MNE 1.13.2 documentation



Also, if all channels show the same fluctuations even after excluding bad channels, investigate common-mode artifacts, ground/reference electrode problems, and acquisition-related noise. Average referencing cannot remove genuine noise shared by all electrodes.

My recommendation: Don't discard the recording or apply aggressive filtering immediately. First identify the noisy channels, mark them as bad, recompute the average reference, and inspect the result.

Documentation: [MNE-Python: Setting the EEG reference](https://mne.tools/stable/auto_tutorials/preprocessing/55_setting_eeg_reference.html?utm_source=chatgpt.com).
