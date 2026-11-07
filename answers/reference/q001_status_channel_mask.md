Mask the system bits:
```python
events = mne.find_events(raw, stim_channel="Status", mask=0xFFFF, mask_type="and")
```
