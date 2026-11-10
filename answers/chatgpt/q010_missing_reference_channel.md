If you're using MNE-Python, you can re-reference `raw` to the average of all available EEG electrodes using:

```
raw.set_eeg_reference(ref_channels='average', projection=False)
```

This performs the re-referencing in place, so the result remains in `raw`.

Important points:

- Since Cz was the original reference but is not present in the file, you do not need to add or reconstruct Cz.
- MNE computes the average reference using the available EEG channels.
- `projection=False` applies the reference immediately rather than adding it as a projection.
- Make sure non-EEG channels (EOG, ECG, EMG, etc.) are correctly typed so they are excluded from the average.

You can verify the result with:

```
print(raw.get_eeg_reference())
```

Note: This is an average reference of the available electrodes, not necessarily the ideal average reference of the original full electrode montage, since Cz is missing.
