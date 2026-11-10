BioSemi records trigger codes alongside system status flags (such as CMS/DRL range status, battery level, and optical link sync) in a single status channel. The trigger inputs use the lower 16 bits (or lower 8 bits), while system flags use bits 16–23.

When `mne.find_events` reads the `'Status'` channel without masking, these upper system bits add large values (e.g., $2^{16} = 65536$) to your trigger codes and trigger false event detections whenever a system state changes.

Applying a bitwise mask directly inside `mne.find_events()` strips out the system bits before event transitions are detected.

```python
import mne

# Extract correct events by masking out BioSemi system status bits (bits 16-23)
events = mne.find_events(
    raw, 
    stim_channel='Status', 
    mask=2**16 - 1,  # 65535 (or 255 / 0xFF if using an 8-bit trigger port)
    mask_type='and'
)

```

### Why this works

* **Fixes large values:** The `mask` parameter performs a bitwise `AND` operation (`raw_value & 65535`), stripping off upper bits (16–23) so that values like `65537` revert to your actual trigger code `1`.
* **Fixes extra events:** Masking occurs **before** `find_events` scans for value changes. This prevents system status toggles (like CMS going in or out of range) from registering as new experiment events.
