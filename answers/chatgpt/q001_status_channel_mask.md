BioSemi systems store trigger information in the `Status` channel as a 16-bit digital word. MNE may interpret this as a combination of trigger bits, producing large values and extra events.

For BioSemi data, the usual solution is to mask the Status channel to retain only the lower 8 bits before extracting events.

Use this code:

python

```python
import mne

# Extract events from the BioSemi Status channel
events = mne.find_events(
    raw,
    stim_channel='Status',
    output='onset',
    consecutive=True,
    shortest_event=1
)

# Keep only the lower 8 bits of the trigger values
events[:, 2] &= 0xFF

# Retain only your experimental trigger codes (1, 2, 3)
events = events[events[:, 2] != 0]
events = events[events[:, 2] <= 3]

print(events)
```

An important detail: For BioSemi, it is generally better to mask the trigger channel before event extraction, rather than after it. This avoids detecting spurious transitions caused by other bits in the Status channel.

Here is the recommended approach:

python

```python
import mne
import numpy as np

# Get the Status channel data
status = raw.get_data(picks=['Status'])[0]

# Mask to retain only the lower 8 bits
status = np.bitwise_and(status.astype(np.int64), 0xFF)

# Create a temporary stim channel
raw_events = raw.copy()

raw_events._data[raw_events.ch_names.index('Status')] = status

# Extract events
events = mne.find_events(
    raw_events,
    stim_channel='Status',
    output='onset',
    consecutive=True,
    shortest_event=1
)

# Keep only trigger codes 1, 2 and 3
events = events[np.isin(events[:, 2], [1, 2, 3])]

print(events)
```

Why this works:

- `0xFF` is a bitmask that retains the lower 8 bits.
- `np.isin()` retains only your intended experimental trigger codes.
- `events` remains a standard MNE events array with columns `[sample, previous_value, event_id]`.

One caveat: This assumes your experimental triggers are encoded in the lower 8 bits. If you still see unexpected values, inspect the raw Status values and confirm the trigger encoding before applying the mask.
