For EEG source localization with MNE-Python (e.g., minimum-norm estimation or dSPM), you should generally use an average reference.

MNE provides a direct method for this: `raw.set_eeg_reference('average')`.

### Python code

```
import mne# Apply average reference directly to the Raw objectraw.set_eeg_reference(ref_channels='average', projection=False)
```

This modifies `raw` in place.

However, for your specific goal of dSPM/source localization, I recommend using an average-reference projector instead:

```
import mne# Add an average EEG reference projectorraw.set_eeg_reference(ref_channels='average', projection=True)
```

Recommended for dSPM

### Why use `projection=True`?

MNE specifically recommends this approach for EEG source imaging because:

- The average reference is applied as a projector rather than immediately modifying the signal.
- It adapts if you subsequently mark channels as bad or drop channels.
- It ensures compatibility with MNE's EEG inverse modeling workflow.&#x20;

  [image](https://www.google.com/s2/favicons?domain=https://mne.tools\&sz=32)

  MNE 1.13.2 documentation+1



### Important considerations

1. Mark bad EEG channels before creating the projector:
   ```
   raw.info['bads'] = ['EEG 001']  # Replace with your bad channel namesraw.set_eeg_reference('average', projection=True)
   ```
2. You can inspect the projector:
   ```
   print(raw.info['projs'])
   ```
3. MNE will handle applying the projector during subsequent processing where appropriate. You can also explicitly apply it:
   ```
   raw.apply_proj()
   ```

My recommendation: Use `projection=True` rather than `projection=False` if you intend to perform EEG source localization with dSPM. Also ensure that your original acquisition reference electrode is represented appropriately in the data, as this can affect average referencing.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://github.com\&sz=32)

GitHub+1



Documentation: [MNE-Python: Setting the EEG reference](https://mne.tools/stable/auto_tutorials/preprocessing/55_setting_eeg_reference.html?utm_source=chatgpt.com).
