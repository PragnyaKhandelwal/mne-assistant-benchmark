The cause is that `mne.Epochs` applies baseline correction by default. When you don't pass `baseline`, it uses `baseline=(None, 0)`, which subtracts the mean of the pre-stimulus interval (from `tmin` to 0) from every channel. That's what removes the DC offset.

To keep the data as recorded, pass `baseline=None`:

```python
epochs = mne.Epochs(raw, events, tmin=-0.2, tmax=0.5, baseline=None, preload=True)
data = epochs.get_data()
```

`data` is then a NumPy array of shape `(n_epochs, n_channels, n_times)` with the original offsets intact.

A few things to be aware of:

- **Units:** MNE stores data in SI units, so EEG/EOG/EMG is in volts and MEG in tesla (or tesla/meter for gradiometers). If you need microvolts, multiply by `1e6`. Newer MNE versions also let you call `epochs.get_data(units="uV")`.
- **Preloading:** `preload=True` loads the epochs into memory immediately. If you leave it off, `get_data()` will load them on demand, so it isn't strictly required.
- **Raw data processing still applies:** `baseline=None` only disables the baseline step. If you filtered `raw` beforehand, e.g. with a high-pass filter, the DC offset may already have been removed there, and no epoching option will bring it back. If the offset is missing even with `baseline=None`, check your preprocessing for `raw.filter(l_freq=...)`.
- **Applying a baseline later:** if you change your mind, you can call `epochs.apply_baseline((None, 0))` on the same object without re-epoching.

You can confirm that no baseline was applied by checking `epochs.baseline`, which should return `None`.
