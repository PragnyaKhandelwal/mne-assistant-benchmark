```python
import mne
print(mne.__version__)


```

```text
Traceback (most recent call last):
  File "<xbox-string>", line 1, in <module>
    import mne
ModuleNotFoundError: No module named 'mne'


```

```python
import mne

# Set average reference as a projection operator (recommended for source localization)
raw.set_eeg_reference("average", projection=True)

```

If your hardware used a specific scalp electrode as the recording reference (e.g., `'FCz'`) that was omitted from the channel array, add it back first before setting the average reference to avoid biasing the calculation:

```python
# 1. Add the original reference channel back (if missing from raw)
raw.add_reference_channels(ref_channels=["FCz"])

# 2. Set montage (so the added channel gets 3D location coordinates)
montage = mne.channels.make_standard_montage("standard_1020")
raw.set_montage(montage)

# 3. Add average reference projection
raw.set_eeg_reference("average", projection=True)

```

### Key Considerations for Source Localization

* **Use `projection=True`:** MNE's forward modeling (`make_forward_solution`) and inverse solvers (`make_inverse_operator` for dSPM/sLORETA) expect the average reference to be stored as a Signal Space Projection (SSP) operator in `raw.info['projs']`. This allows the inverse solver to incorporate the reference constraint directly into the gain/leadfield matrix.
* **Mark Bad Channels First:** Set noisy or flat channels in `raw.info['bads'] = ['EEG012', ...]` prior to calling `set_eeg_reference`. MNE automatically excludes any channel marked as bad from the average reference operator.
* **Applying the Projection:** The projector remains inactive until needed. If you want to force the projection directly onto the continuous signal data (e.g., for sensor-space plotting), run `raw.apply_proj()`.
