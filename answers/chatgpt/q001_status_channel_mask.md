BioSemi systems store trigger information in the `Status` channel as a 16-bit digital signal. MNE-Python may interpret this as a signed integer, which can produce large negative or unexpected trigger values. Additionally, BioSemi's trigger channel can contain extra bits that cause spurious events.

The usual solution is to mask the lower 8 bits of the `Status` channel before extracting events.

Use this code:

```
import mneimport numpy as np# Get the Status channel datastatus = raw.get_data(picks=['Status'])[0]# Convert to unsigned 16-bit valuesstatus = status.astype(np.uint16)# Keep only the lower 8 bitsstatus = status & 0x00FF# Put the corrected trigger values back into the Raw objectraw._data[raw.ch_names.index('Status')] = status# Extract eventsevents = mne.find_events(    raw,    stim_channel='Status',    output='onset',    consecutive=True,    shortest_event=1)# Keep only your experimental trigger codes: 1, 2, and 3events = events[np.isin(events[:, 2], [1, 2, 3])]print(events)
```

Why this works:

1. `astype(np.uint16)` handles the signed/unsigned representation of the BioSemi trigger values.
2. `& 0x00FF` retains only the lower 8 bits, removing unwanted higher-bit information.
3. `mne.find_events()` detects the trigger onsets.
4. `np.isin()` retains only your experimental trigger codes (1, 2, and 3).

Important: This assumes your experimental trigger codes are encoded in the lower 8 bits. Also, modifying `raw._data` directly is an internal MNE operation; make a copy of `raw` first if you need to preserve the original data.

If you still see unexpected events, inspect the unique values in the corrected trigger channel:

```
print(np.unique(status))
```

You should see values including 0, 1, 2, and 3, rather than large unexpected values.
