import mne
import numpy as np
# Get the Status channel data
status = raw.get_data(picks=['Status'])[0]
# Convert to unsigned 16-bit values
status = status.astype(np.uint16)
# Keep only the lower 8 bits
status = status & 0x00FF
# Put the corrected trigger values back into the Raw object
raw._data[raw.ch_names.index('Status')] = status
# Extract events
events = mne.find_events(    raw,    stim_channel='Status',    output='onset',    consecutive=True,    shortest_event=1)
# Keep only your experimental trigger codes: 1, 2, and 3
events = events[np.isin(events[:, 2], [1, 2, 3])]
print(events)
