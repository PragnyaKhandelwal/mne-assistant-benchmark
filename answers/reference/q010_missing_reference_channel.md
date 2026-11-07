```python
raw = mne.add_reference_channels(raw, "Cz")
raw.set_eeg_reference("average")
```
