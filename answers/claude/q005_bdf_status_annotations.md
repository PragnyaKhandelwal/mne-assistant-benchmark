The BDF status channel is a 24-bit word, and only the low bits are your triggers. The usual problems come from the upper bits and from how the channel is read.

## BioSemi status channel layout

- **Bits 0-15**: trigger lines (parallel port; on USB-only setups, usually just bits 0-7)
- **Bits 16-23**: system flags (CMS in range, battery low, speed mode, etc.)

If you don't mask the upper bits, you'll get huge or inconsistent event IDs (e.g. 65536+ or 16777215-ish values) that change when the CMS flag toggles.

## Recommended approach

```python
import mne

raw = mne.io.read_raw_bdf(
    "data.bdf",
    stim_channel="Status",   # or 'auto'
    preload=True,
    # uint_cast=True,        # see below if you get negative values
)

events = mne.find_events(
    raw,
    stim_channel="Status",
    mask=0xFF,               # keep low 8 bits (use 0xFFFF for 16 trigger lines)
    mask_type="and",         # keep only bits in the mask
    shortest_event=1,        # BioSemi pulses can be very short, so don't drop them
    initial_event=False,
    consecutive="increasing",
    verbose=True,
)
print(events[:10])
print(set(events[:, 2]))     # sanity check: should be your known trigger codes
```

## Common gotchas

1. **Masking**: Always set `mask`. `0xFF` for 8-bit triggers, `0xFFFF` for 16-bit. `mask_type="and"` keeps only the masked bits (the default in recent MNE versions; check your version's docs).

2. **Negative or weird values**: The status word is unsigned, but it can be read as signed. Pass `uint_cast=True` to `read_raw_bdf` to cast the stim channel to unsigned integers.

3. **Offset/baseline in the status channel**: Some recordings have a constant high-byte value, so the trigger "returns" to something non-zero rather than 0. Masking fixes this. Otherwise, `find_events` may report a spurious event at the start (use `initial_event=False`) or a constant offset.

4. **Short pulses**: If events are missing, make sure `shortest_event=1`. Also check your sampling rate against the trigger pulse duration. At low sampling rates, brief pulses can fall between samples.

5. **Consecutive triggers**: The default `consecutive='increasing'` drops transitions where the code goes from a higher value to a lower one without returning to 0. If your triggers go e.g. 5 → 3 without a zero between, use `consecutive=True`.

6. **Channel not detected**: If `stim_channel='auto'` fails, pass the name explicitly (`"Status"`), and check `raw.ch_names` and `raw.get_channel_types()`.

7. **Pulse onset vs. offset**: `find_events` returns the onset sample of each change. If you need the pulse duration or offsets, use `output="offset"` or `output="step"`.

## Checking your result

```python
import numpy as np

print(np.unique(events[:, 2], return_counts=True))
mne.viz.plot_events(events, sfreq=raw.info["sfreq"])
```

Compare the counts against what your experiment script should have sent. If they match, the parsing is correct.

If you share a snippet of `events[:20]` or the unique values you're seeing, I can help work out which of these issues you're hitting.
