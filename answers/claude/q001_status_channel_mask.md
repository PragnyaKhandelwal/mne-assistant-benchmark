BioSemi's Status channel is a 24-bit channel, and the upper bits carry hardware flags (CMS in/out of range, battery low, speed mode, etc.). Your trigger codes only occupy the lowest 8 bits. Also, the 16 bits from the parallel port can leave a residual offset, so raw values look like 65281 or 16711681 instead of 1, 2, 3. The fix is to mask the lower 8 bits.

```python
import mne
import numpy as np

# Mask to keep only the lower 8 bits (the actual trigger codes)
events = mne.find_events(
    raw,
    stim_channel='Status',
    shortest_event=1,        # BioSemi triggers can be very short (1 sample)
    mask=255,                # 0xFF: keep bits 0-7 only
    mask_type='and',
    initial_event=False,
    verbose=True,
)

# Keep only the codes you actually sent
events = events[np.isin(events[:, 2], [1, 2, 3])]

print(np.unique(events[:, 2], return_counts=True))
```

Notes:

- **`mask=255, mask_type='and'`** is the key step. It strips the high-bit status flags so only values 1, 2, 3 remain. In older MNE versions, the default mask behavior differed, so being explicit is safest.
- **`shortest_event=1`** prevents short pulses from being dropped (MNE's default is 2 samples).
- **Extra events**: if you still see spurious events after masking, it's usually either (a) a trigger code that returns to 0 via an intermediate value (e.g., the parallel port lines not all switching at the same sample), or (b) the "pulse off" being picked up as an event. Filtering to `[1, 2, 3]` as above removes (b). For (a), you can use `consecutive=True` (the default) and check `events[:, 1]` (the previous value) to inspect transitions.
- **Reading the file**: if you haven't loaded with the right options, `mne.io.read_raw_bdf(..., stim_channel='Status')` is the standard approach. Some MNE versions also support `mne.io.read_raw_bdf(..., exclude=...)` and treat Status specially, so `find_events` on it works directly.

If the result still looks off, print `np.unique(raw.get_data(picks='Status')[0].astype(int))` to see which raw values exist and adjust the mask accordingly.
