MNE-Python applies baseline correction by default in `mne.Epochs()`. The default is `baseline=(None, 0)`, which subtracts the mean voltage during the pre-stimulus interval from each epoch.

To preserve the original DC offset, explicitly set `baseline=None`:

```
epochs = mne.Epochs(    raw,    events,    tmin=-0.2,    tmax=0.5,    baseline=None)data = epochs.get_data()
```

Now `data` contains the epoched signal without baseline correction, preserving the DC offset (assuming no other preprocessing has removed it).

Important: If `epochs` has already been baseline-corrected, setting `epochs.baseline = None` afterward will not restore the original DC offset. MNE documents that baseline correction cannot be reverted once applied.

You need to recreate the epochs from `raw` with `baseline=None`.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://mne.tools\&sz=32)

MNE 1.13.2 documentation+1
