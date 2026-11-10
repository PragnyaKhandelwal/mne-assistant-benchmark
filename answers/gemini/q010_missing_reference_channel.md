To re-reference to the average correctly when the recording reference electrode (`Cz`) was omitted from the channel list, you must first add `Cz` back as a zero-signal channel before computing the average reference.

If you omit `Cz`, the average reference calculation will exclude a real channel location whose potential was $0\text{ V}$ during recording, introducing a spatial bias into your average voltage calculation.

```python
import mne

# 1. Add the missing reference channel back (initialized with 0 V)
raw.add_reference_channels(ref_channels=["Cz"])

# 2. Set the montage so Cz gets standard 3D location coordinates
montage = mne.channels.make_standard_montage("standard_1020")
raw.set_montage(montage)

# 3. Re-reference to the average reference in-place
raw.set_eeg_reference("average")

```

### Key Considerations

* **Montage Matching:** If your dataset uses a different electrode layout (e.g., `'standard_1005'`, `'biosemi32'`, etc.), specify that montage name in `make_standard_montage()`.
* **Bad Channels:** Mark noisy channels (`raw.info['bads'] = ['EEG012', ...]`) before running `set_eeg_reference`. MNE automatically excludes bad channels from the average calculation.
* **Source Localization:** If you plan to perform source estimation (e.g., dSPM) later, use `raw.set_eeg_reference("average", projection=True)` instead to store the average reference as a Signal Space Projection (SSP) operator.
