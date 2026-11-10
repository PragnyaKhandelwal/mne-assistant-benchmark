In BioSemi BDF files, the 24-bit `'Status'` channel contains both **trigger event codes** and **hardware system status flags** combined into a single signal:

* **Bits 0–15 (Bits 1–16 in BioSemi documentation):** Trigger input channels (experimental events).
* **Bits 16–23 (Bits 17–24 in BioSemi documentation):** Hardware status flags (CMS/DRL range status, battery state, optical link sync, etc.).

---

### 1. Extracting Clean Event Triggers

When reading a BDF file with `mne.io.read_raw_bdf()`, MNE automatically sets `'Status'` as the STIM channel. To isolate experimental triggers from system noise, apply a bitwise mask of $2^{16} - 1$ (`65535`):

```python
import mne

# Load the BDF raw data (Status channel is automatically set as type STIM)
raw = mne.io.read_raw_bdf("sub-01_task-exp_eeg.bdf", preload=True)

# 1. Mask out system status bits (bits 16-23) during event extraction
events = mne.find_events(raw, stim_channel="Status", mask=2**16 - 1, mask_type="and")

```

---

### 2. Handling Bit-Shifted Triggers (8-Bit Hardware Ports)

If your trigger hardware sends 8-bit codes (0–255) over a specific byte line of the parallel port interface, your event values may appear left-shifted (e.g., multiplied by 256):

* **If triggers are in bits 0–7:** Mask with `255` (`2**8 - 1`).
* **If triggers are in bits 8–15:** Bit-shift the extracted event array down by 8 bits:

```python
# If triggers were sent to the upper byte line (bits 8-15):
events[:, 2] >>= 8

```

---

### 3. Extracting Hardware System Flags (CMS/DRL / Battery Status)

If you need to inspect hardware diagnostics (e.g., verifying whether the subject went out of range or battery level dropped during recording), parse specific bits directly from the `'Status'` channel array:

```python
import numpy as np

# Get raw integers from the Status channel
status_data = raw.get_data(picks="Status").astype(int)[0]

# Check CMS bit (Bit 20) — True if CMS electrode is in-range
cms_in_range = (status_data & (1 << 20)) != 0

# Check Battery bit (Bit 22) — True if battery is low
battery_low = (status_data & (1 << 22)) != 0

```
