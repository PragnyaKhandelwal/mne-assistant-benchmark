When using a BioSemi system with MNE-Python, the `'Status'` channel packs both your trigger codes (in the lower 16 bits) and hardware/system status flags like CMS range and battery levels (in the upper bits 16–24). This causes `mne.find_events()` to read massive numbers and pick up hundreds of spurious extra events from normal hardware fluctuations.

To fix this, you need to use the `mask` parameter set to `2**16 - 1` (which filters out everything above the 16th bit).

Here is the Python code to extract the correct events into the `events` variable:

```python
import mne

# Extract events from the 'Status' channel, masking out the upper system-status bits
events = mne.find_events(raw, stim_channel='Status', mask=2**16 - 1)

```
