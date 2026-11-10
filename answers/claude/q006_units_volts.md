MNE stores EEG data in **volts**, so you need to convert your microvolt values before building the object. If you skip that, plots will be off by a factor of 10⁶ (a 10 µV ERP would be labeled as 10 µV only if the data is 1e-5 V).

```python
import mne

# Convert µV -> V (MNE's internal unit for EEG)
data_volts = data * 1e-6

info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types="eeg")

epochs = mne.EpochsArray(data_volts, info, tmin=-0.2)  # set tmin to your epoch start time (s)
```

**Things to get right**

- **`tmin`**: This is the time (in seconds) of the first sample relative to the event. If your epochs start 200 ms before stimulus onset, use `tmin=-0.2`. If you leave it at the default of 0, your time axis and any baseline will be wrong, and ERP plots won't line up with stimulus onset.
- **Events**: By default `EpochsArray` creates dummy events (all with ID 1). If you have real trial labels, pass them so you can do `epochs["condition"]`:

  ```python
  # events: (n_epochs, 3) array -> [sample_index, 0, event_id]
  epochs = mne.EpochsArray(data_volts, info, events=events, event_id=event_id, tmin=-0.2)
  ```

- **Baseline**: `EpochsArray` does not baseline-correct by default. If your exported data wasn't already baseline-corrected, apply it with `epochs.apply_baseline((None, 0))`, or pass `baseline=(None, 0)` to the constructor.
- **Montage (optional)**: For topomaps you need sensor positions:

  ```python
  epochs.set_montage("standard_1020")  # or your own montage
  ```

**Check it worked**

```python
evoked = epochs.average()
evoked.plot()   # y-axis should show sensible µV values (typically a few to tens of µV)
```

MNE automatically displays EEG in µV in plots even though it stores volts, so if the plotted amplitudes look like what you'd expect from the original program, the scaling is correct. As a quick numeric sanity check, `epochs.get_data().std()` should be on the order of 1e-5 to 1e-4 for typical EEG.
