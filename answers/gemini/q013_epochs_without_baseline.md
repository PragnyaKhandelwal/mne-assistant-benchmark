By default, `mne.Epochs` applies baseline correction using `baseline=(None, 0)`, which subtracts the mean of the pre-stimulus interval and removes the DC offset.

To keep the data exactly as recorded without baseline correction, pass `baseline=None` when initializing the epochs object:

```python
epochs = mne.Epochs(raw, events, tmin=-0.2, tmax=0.5, baseline=None)
data = epochs.get_data()

```
