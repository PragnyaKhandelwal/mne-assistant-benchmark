# Blind grading sheet

Each question below has three replies labelled A, B and C. The labels are shuffled
per question and the assistant names are hidden. Grade each reply PASS or FAIL against
the criteria, with one line of reasoning. See [GRADING.md](../GRADING.md).

## q004_filter_epochs_vs_raw: Filtering short epochs

**Prompt**

I have already epoched my EEG data in MNE-Python (epochs from -0.2 to 0.5 s).
Now I want to apply a 1-40 Hz band-pass filter. Should I filter the epochs
directly? Please explain and give code.

**Criteria**

Pass if the answer:
- recommends filtering the continuous (raw) data before epoching, where possible;
- explains edge effects / that the filter is long relative to short epochs
  (MNE warns when the filter length exceeds the signal length);
- if filtering epochs is unavoidable, suggests longer epochs or padding and cropping afterwards.
Fail if it simply calls `epochs.filter(1, 40)` with no warning about edge effects.

### Reply A

<details><summary>Show reply</summary>

### Direct Answer

**No, you should ideally not filter epoched data directly** if your continuous (Raw) data is available.

In MNE-Python, the standard and recommended pipeline is to apply filters to the **Raw continuous data *before* creating epochs**.

Since your epochs are very short (`-0.2` to `0.5` seconds, totaling just 700 ms), filtering them directly—especially with a 1 Hz high-pass filter—will cause severe **edge artifacts (filter ringing)** that can corrupt a massive portion of your data window.

---

### Why You Should Filter Raw Data Instead

1. **Filter Ringing and Edge Effects:**
Digital filters need a certain amount of time (the filter length/transition bandwidth) to "settle" when they encounter a sharp boundary. When you filter a continuous Raw file, the filter settles once at the beginning of the recording. When you filter individual short epochs, the filter has to settle at the start *and* the end of *every single epoch*.
2. **Impact on Short Epochs:**
A 1 Hz high-pass filter has a relatively long impulse response. On a short 0.7-second epoch, these boundary artifacts can bleed deep into your time of interest (e.g., around your stimulus onset at 0.0 s).

---

### Recommended Pipeline (Filter Raw $\rightarrow$ Epochs)

If you still have access to your Raw object, the correct approach is:

```python
import mne

# 1. Load your raw data
raw = mne.io.read_raw_fif("your_raw_file.fif", preload=True)

# 2. Apply the 1-40 Hz band-pass filter on the CONTINUOUS data
raw.filter(l_freq=1.0, h_freq=40.0, fir_design="firwin")

# 3. Find events and create epochs afterwards
events = mne.find_events(raw)
epochs = mne.Epochs(
    raw, events, event_id=dict(target=1), tmin=-0.2, tmax=0.5, baseline=(-0.2, 0)
)

```

---

### What to Do If You *Only* Have Epochs Saved

If your raw data has already been discarded and you only have saved epochs, MNE does allow you to filter epochs directly using `.filter()`:

```python
# If you must filter epochs directly:
epochs.filter(l_freq=1.0, h_freq=40.0, fir_design="firwin")

```

**If you choose this fallback route, keep these precautions in mind:**

* **Padding:** MNE-Python attempts to mitigate edge artifacts by mirroring/padding the data at the epoch boundaries during filtering, but it is still less ideal than filtering continuous data.
* **Wider Epoch Window:** If possible in the future, extract a wider epoch window (e.g., `-0.5` to `1.0` s) during epoching, apply your filters, and then crop the epochs down to your analysis window (`-0.2` to `0.5` s) to discard the edge artifacts.

</details>

### Reply B

<details><summary>Show reply</summary>

Short answer: you *can* filter epochs directly, but it's usually not the best choice, especially with a 1 Hz high-pass on short epochs. Filter the continuous data *before* epoching if you can.

## Why filtering epochs is problematic

**1. Edge artifacts.** FIR/IIR filters have a transient response at the start and end of the signal. Your epochs are only 0.7 s long, and a 1 Hz high-pass filter needs a long kernel (MNE's default for `l_freq=1` is about 3.3 s, since the transition bandwidth is 1 Hz and the filter length is roughly `3.3 / transition_bandwidth`). The kernel is longer than your epoch, so MNE will warn you that the filter is longer than the signal, and the output near the edges will be distorted.

**2. Your baseline and the time window of interest get contaminated.** Edge distortion lands right in the -0.2 to 0 s baseline period and at the end of the epoch, which can bias baseline correction and late components.

**3. Redundancy at epoch boundaries.** Filtering each epoch independently means every epoch gets its own edge effects, instead of one clean filtering pass over continuous data where edges only occur at the very start and end of the recording.

## Recommended approach: filter the raw data, then epoch

```python
import mne

raw = mne.io.read_raw_fif("my_data_raw.fif", preload=True)

# Filter continuous data first
raw.filter(l_freq=1.0, h_freq=40.0, fir_design="firwin", phase="zero")

events = mne.find_events(raw)  # or mne.events_from_annotations(raw)
epochs = mne.Epochs(
    raw, events, event_id=event_id,
    tmin=-0.2, tmax=0.5,
    baseline=(None, 0),
    preload=True,
)
```

## If you only have epochs (can't go back to raw)

If you truly can't access the continuous data, you can still filter the epochs, but be aware of the limitations:

```python
# epochs must be preloaded
epochs.load_data()

# Option A: low-pass only (usually safe on short epochs)
epochs.filter(l_freq=None, h_freq=40.0, fir_design="firwin")

# Option B: band-pass 1-40 Hz (expect edge artifacts and a MNE warning)
epochs.filter(l_freq=1.0, h_freq=40.0, fir_design="firwin")
```

Practical tips for this case:

- **Low-pass is fine, high-pass is the problem.** A 40 Hz low-pass has a short kernel and works acceptably on short epochs. The 1 Hz high-pass is what causes trouble.
- **Pad the epochs** if you ever re-epoch: use a wider `tmin`/`tmax` (e.g., -1.0 to 1.5 s) for filtering, then crop with `epochs.crop(tmin=-0.2, tmax=0.5)`. This keeps edge artifacts outside your window of interest.
- **Reduce the filter length** if you must (e.g., `filter_length="auto"` is default; you could widen the transition band with `l_trans_bandwidth=2.0`), but this makes the filter less sharp and is a tradeoff.
- **Consider a lower high-pass cutoff** (e.g., 0.1 Hz) if your goal is just to remove slow drifts, since this also reduces filter artifacts for ERP analyses. Note that 1 Hz is often used specifically for ICA, and in that case a common workflow is to fit ICA on a 1 Hz high-passed copy of the data, then apply the solution to a less aggressively filtered version.

## Summary

| Situation | Recommendation |
|---|---|
| Have continuous raw data | Filter raw first, then epoch (best practice) |
| Only have epochs, need low-pass | `epochs.filter(None, 40)` is fine |
| Only have epochs, need 1 Hz high-pass | Possible but expect edge effects; avoid if you can |
| Planning to re-epoch | Epoch with padding, filter, then `epochs.crop()` |

If you tell me what the filtered data will be used for (ERP analysis, ICA, time-frequency, decoding), I can suggest more specific filter settings.

</details>

### Reply C

<details><summary>Show reply</summary>

Yes, you can filter epoched EEG data directly in MNE-Python, but filtering the continuous raw EEG data before epoching is generally the recommended approach.

Since your epochs extend from −0.2 to 0.5 seconds, there is one important consideration: filtering short epochs can introduce edge artifacts, especially near the beginning and end of each epoch.

## 1. Recommended approach: Filter before epoching

Ideally, apply the 1–40 Hz band-pass filter to your continuous EEG data (`Raw` object), and then create epochs.

Why is this better?

- Filtering continuous data avoids repeatedly introducing filter edge effects at every epoch boundary.
- The filter has more surrounding data available to operate on.
- It reduces the risk of distortion near the start and end of your epochs.
- It is generally more reliable for ERP and time-frequency analyses.

### MNE-Python code

```
import mne# Load your continuous EEG dataraw = mne.io.read_raw_fif('raw_data.fif', preload=True)# Apply 1-40 Hz band-pass filterraw.filter(    l_freq=1.0,    h_freq=40.0,    fir_design='firwin')# Create epochs after filteringepochs = mne.Epochs(    raw,    events,    event_id=event_id,    tmin=-0.2,    tmax=0.5,    baseline=None,    preload=True)
```

## 2. If you have already created epochs

If you no longer have access to the continuous raw data, you can filter your existing epochs directly.

MNE supports filtering an `Epochs` object.

```
# Apply 1-40 Hz band-pass filter directly to epochsepochs.filter(    l_freq=1.0,    h_freq=40.0,    fir_design='firwin')
```

This applies the filter independently to each epoch.

Important consideration

Because your epochs are relatively short (700 ms), filtering directly can introduce edge artifacts.

In particular:

- The first part of the epoch (−0.2 s) may be affected.
- The last part of the epoch (+0.5 s) may also be affected.
- A 1 Hz high-pass filter has a relatively long time scale, making short-epoch filtering especially problematic.

## 3. How to check your filtering

You can visualize the filtered epochs:

```
# Plot epochsepochs.plot()# Plot the average ERPevoked = epochs.average()evoked.plot()# Plot the power spectral densityepochs.compute_psd().plot()
```

You can also inspect the filter response:

```
epochs.compute_psd().plot(    fmin=0.1,    fmax=60)
```

## 4. My recommendation for your dataset

| Situation                    | Recommendation                                   |
| ---------------------------- | ------------------------------------------------ |
| Continuous raw EEG available | Filter raw data first                            |
| Only epoched data available  | Filtering epochs is possible, but use caution    |
| ERP analysis                 | Prefer filtering continuous data before epoching |
| Very short epochs            | Avoid filtering directly if possible             |

One additional suggestion: If you still have your continuous EEG data, consider creating longer epochs first, filtering them, and then cropping them to −0.2 to 0.5 seconds.

For example:

```
# Create longer epochsepochs = mne.Epochs(    raw,    events,    event_id=event_id,    tmin=-1.0,    tmax=1.0,    baseline=None,    preload=True)# Filter longer epochsepochs.filter(    l_freq=1.0,    h_freq=40.0,    fir_design='firwin')# Crop to your desired intervalepochs.crop(tmin=-0.2, tmax=0.5)
```

This provides additional data around your analysis window, although filtering continuous raw data before epoching remains preferable.

One question that would help me give you the most appropriate filtering recommendation:

Are you performing ERP analysis (event-related potentials) or frequency-band analysis (such as alpha, beta, or theta power)?

The choice of high-pass cutoff and filtering strategy can differ depending on your analysis.

</details>

| Reply | PASS/FAIL | Reason |
|---|---|---|
| A | | |
| B | | |
| C | | |

---

## q005_bdf_status_annotations: Are BDF status triggers parsed automatically?

**Prompt**

How do I parse the status channel of a BDF file correctly in MNE-Python?

**Criteria**

Pass if the answer:
- says the 'Status' channel is loaded as a stim channel and is NOT converted to
  annotations automatically (only TAL 'BDF Annotations' channels are);
- uses `mne.find_events(raw, stim_channel="Status")`;
- masks the upper bits (e.g. `mask=0xFFFF` or `events[:, 2] &= 2**16 - 1`) because
  bits 16-23 hold system codes (CMS, battery, ...).
Fail if it claims MNE parses status triggers into annotations automatically.

### Reply A

<details><summary>Show reply</summary>

Parsing the status channel of a BioSemi **BDF** file correctly in MNE-Python requires accounting for how BioSemi hardware encodes data.

In BDF files, the status channel (usually named `'Status'`) is a 24-bit word where:

* **Bits 0–15 (lower 16 bits)** contain your actual experiment event triggers/codes.
* **Bits 16–23 (higher bits)** contain hardware/system status flags (e.g., Common Mode Sense [CMS] out-of-range warnings, battery status, electrode connection status).

If you parse events without filtering these upper bits, the system flags will contaminate your event codes, causing erratic or huge integer values.

---

### Method 1: Using `mne.find_events()` with a Mask (Recommended)

The cleanest and most robust way to parse events is to apply a 16-bit bitmask directly inside `mne.find_events()` using the `mask` parameter. This tells MNE to ignore everything above the 16th bit:

```python
import mne

# 1. Load the BDF file (MNE automatically detects 'Status' as a STIM channel)
raw = mne.io.read_raw_bdf("your_recording.bdf", preload=True)

# 2. Extract events using a 16-bit mask (2**16 - 1 = 65535)
events = mne.find_events(raw, mask=2**16 - 1)

print(events[:5])  # Preview the first few events

```

### Method 2: Manual Post-Processing of Events

If you have already extracted the events array without a mask, you can apply a bitwise AND operation on the event values (the third column, `events[:, 2]`) manually:

```python
import numpy as np

events = mne.find_events(raw)

# Keep only the lower 16 bits
events[:, 2] &= 2**16 - 1

```

---

### Troubleshooting Edge Cases

* **Trigger Shifting:** Depending on how your external triggering box or parallel port interface is wired, triggers might occasionally be offset by 8 bits. If your parsed event IDs look completely wrong or are uniformly multiplied by 256, you may need to right-shift the values:
```python
events[:, 2] >>= 8

```


* **Checking Hardware/CMS Status:** If you ever need to inspect system-level flags (like checking whether the CMS rail went out of range during recording), you can query the higher bits explicitly using bitwise operations:
```python
# Example: Checking the 20th bit for CMS status
cms_bit = 20
raw_data = raw.get_data(picks="Status")[0]
cms_out_of_range = (raw_data & (1 << cms_bit)) != 0

```

</details>

### Reply B

<details><summary>Show reply</summary>

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

</details>

### Reply C

<details><summary>Show reply</summary>

In MNE-Python, the correct way to parse the Status channel in a BioSemi BDF file is to load the file using `mne.io.read_raw_bdf()` and extract events using `mne.find_events()`.

There is an important detail: BioSemi stores trigger codes and system-status information in different bits of the Status channel. If you don't account for this, you may get unexpectedly large event values or incorrect trigger codes.

## 1. Load the BDF file

```
import mneimport numpy as npbdf_file = "your_file.bdf"raw = mne.io.read_raw_bdf(    bdf_file,    preload=True,    stim_channel="auto")print(raw.ch_names)print(raw.get_channel_types())
```

By default, MNE recognizes channels named `Status` or `Trigger` (case-insensitive) as stimulus channels.

## 2. Extract events from the Status channel

Use `mne.find_events()`:

```
events = mne.find_events(    raw,    stim_channel="Status",    shortest_event=1,    verbose=True)print(events[:10])
```

The resulting array has three columns:

| Column         | Meaning                   |
| -------------- | ------------------------- |
| `events[:, 0]` | Sample index of the event |
| `events[:, 1]` | Previous trigger value    |
| `events[:, 2]` | New trigger value         |

For example:

```
[[  1024     0     1]
 [  2048     0     2]
 [  3072     0     3]]
```

## 3. Important: Remove BioSemi system-status bits

This is probably the most important part.

BioSemi uses a 24-bit Status channel:

- Bits 1–16: Trigger/event codes.
- Bits 17–24: System-status information (such as CMS and battery status).

Consequently, MNE may return event values larger than your actual trigger codes.

To extract only the trigger codes, use a 16-bit mask:

```
events = mne.find_events(    raw,    stim_channel="Status",    shortest_event=1,    mask=2**16 - 1,    mask_type="and")
```

This retains only the lower 16 bits.

You can also apply the mask afterward:

```
events[:, 2] &= 0xFFFF
```

I recommend applying the mask directly in `mne.find_events()`.

This behavior is documented in the [MNE-Python BDF reader documentation](https://mne.tools/stable/generated/mne.io.read_raw_bdf.html).
## 4. Get event IDs and their occurrences

Once you have extracted the events:

```
event_id = {    "condition_1": 1,    "condition_2": 2,    "condition_3": 3,}print(mne.event.count_events(    raw,    events=events))
```

Alternatively, count occurrences directly:

```
unique, counts = np.unique(events[:, 2], return_counts=True)for event, count in zip(unique, counts):    print(f"Event {event}: {count} occurrences")
```

## 5. Create epochs

You can now use the extracted events for epoching:

```
epochs = mne.Epochs(    raw,    events,    event_id=event_id,    tmin=-0.2,    tmax=0.8,    baseline=(None, 0),    preload=True)epochs.plot()
```

## 6. If the event values are still incorrect

There are a few things worth checking.

A. Check the Status channel directly

```
status = raw.get_data(picks=["Status"])[0]print("Minimum:", status.min())print("Maximum:", status.max())print("Unique values:", np.unique(status)[:30])
```

B. Check whether triggers are shifted by 8 bits

Some synchronization systems encode triggers in shifted bit positions.

If your event codes appear to be multiples of 256, try:

```
events[:, 2] >>= 8
```

Only do this if the acquisition/synchronization hardware confirms that the triggers are shifted.

C. Check whether you are using annotations instead

Some BDF files contain a `BDF Annotations` channel. MNE parses these automatically into `raw.annotations`.

You can extract those events separately:

```
events, event_id = mne.events_from_annotations(raw)
```

Do not confuse annotation-based events with events encoded in the Status channel.

## Recommended complete implementation

For a typical BioSemi EEG recording, I would start with this:

```
import mneimport numpy as np# Load BDFraw = mne.io.read_raw_bdf(    "your_file.bdf",    preload=True)# Extract trigger events (lower 16 bits)events = mne.find_events(    raw,    stim_channel="Status",    mask=0xFFFF,    mask_type="and",    shortest_event=1)# Inspect event codesunique, counts = np.unique(events[:, 2], return_counts=True)print("\nDetected events:")for code, count in zip(unique, counts):    print(f"Trigger {code}: {count} occurrences")# Inspect event timingprint("\nFirst 10 events:")print(events[:10])
```

One important question: Are you working with a BioSemi ActiveTwo recording, or a BDF file generated by another EEG acquisition system? The correct interpretation of the Status bits can depend on the acquisition hardware and trigger configuration.

</details>

| Reply | PASS/FAIL | Reason |
|---|---|---|
| A | | |
| B | | |
| C | | |

---

## q011_bad_channel_before_avgref: Noise spreading to all channels after average reference

**Prompt**

After setting an average reference on my EEG (`raw`), every channel shows the same
large noisy fluctuations that weren't there before. What is going on, and how do I
fix it? Give code that leaves `raw` correctly average-referenced.

**Criteria**

Pass if the noisy channel (T7) is marked as bad (or dropped) before the average
reference is computed, so its noise is not spread to every other channel.

### Reply A

<details><summary>Show reply</summary>

This is most likely a bad-channel contamination problem caused by the common average reference (CAR).

When you apply an average reference, EEG data from every included channel contribute to a common reference signal. That signal is then subtracted from every EEG channel.

Mathematically,

\\[ V_i^{\mathrm{referenced}}(t) = V_i(t)-\frac{1}{N}\sum\_{j=1}^{N}V_j(t) \\]

If one or more channels contain large noise, electrode artifacts, or unusually large fluctuations, they can dominate the average. Because that noisy average is subtracted from every channel, the same fluctuations suddenly appear across all channels.

The important point: Average referencing does not necessarily create new noise. It can spread the influence of existing noisy channels across the entire EEG recording.

## 1. How to fix it in MNE-Python

The solution is to identify bad EEG channels, mark them as bad, and then recompute the average reference.

MNE automatically excludes channels listed in `raw.info['bads']` from the average-reference calculation.
For example:

```
# Identify channels that are noisy or malfunctioningbad_channels = ['Fp1', 'T8']  # Replace with your actual bad channels# Mark them as badraw.info['bads'] = bad_channels# Recompute the average reference, in-placeraw.set_eeg_reference(ref_channels='average', projection=False)# Check the resultraw.plot()
```

The channel names above are examples. Only mark channels that you have actually identified as bad.

Important: If you have already applied average referencing, you can still recompute it after marking the bad channels. For the remaining good channels, subtracting their new average removes the old common reference offset.

## 2. A more careful preprocessing workflow

Ideally, identify bad channels before applying the reference. I recommend keeping an untouched copy of the original data:

```
# Preserve original, unreferenced dataraw_original = raw.copy()# Identify bad channels after inspecting the EEGbad_channels = ['Fp1', 'T8']  # Example only# Mark bad channelsraw.info['bads'] = bad_channels# Apply average referenceraw.set_eeg_reference(    ref_channels='average',    projection=False)# Plot the average-referenced dataraw.plot()
```

This modifies `raw` in-place, so your `raw` object remains the average-referenced recording.

## 3. How to identify the problematic channels

Before deciding which channels to exclude, inspect the original recording:

```
# Plot original data before average referencingraw_original.plot(    duration=10,    n_channels=32,    scalings='auto')
```

Look for channels with:

- Much larger amplitudes than neighboring channels.
- Persistent high-frequency noise.
- Sudden jumps or large irregular fluctuations.
- Flat signals or intermittent electrode contact.

You can also inspect the channel types:

```
print(raw.get_channel_types())print("Bad channels:", raw.info['bads'])
```

## 4. Verify that average referencing worked

For the good EEG channels, the instantaneous average should be approximately zero after average referencing.

```
import numpy as npimport mne# Get good EEG channel indicespicks = mne.pick_types(    raw.info,    eeg=True,    exclude='bads')# Extract EEG datadata = raw.get_data(picks=picks)# Calculate the average across good EEG channelsaverage_signal = np.mean(data, axis=0)print("Maximum residual average:",      np.max(np.abs(average_signal)))
```

The residual should be close to zero (allowing for floating-point precision).

## 5. One additional important consideration

If your original acquisition reference electrode was not included in the recorded channels, simply averaging the available electrodes can introduce a reference bias. MNE documents this situation and provides `mne.add_reference_channels()` to handle it.
Also, if all channels show the same fluctuations even after excluding bad channels, investigate common-mode artifacts, ground/reference electrode problems, and acquisition-related noise. Average referencing cannot remove genuine noise shared by all electrodes.

My recommendation: Don't discard the recording or apply aggressive filtering immediately. First identify the noisy channels, mark them as bad, recompute the average reference, and inspect the result.

Documentation: [MNE-Python: Setting the EEG reference](https://mne.tools/stable/auto_tutorials/preprocessing/55_setting_eeg_reference.html).

</details>

### Reply B

<details><summary>Show reply</summary>

### What is Going On?

When you compute an **average reference**, the software calculates the mean signal across *all* included EEG channels at every time point and subtracts that mean from each individual channel.

If your recording contains a **bad or malfunctioning channel** with massive noise, a movement artifact, or a rail artifact (disconnection), and that channel was **not** marked as bad beforehand, its extreme fluctuations get factored into the global average. When this contaminated average is subtracted from every single channel, that local noise is injected globally into your entire montage. Consequently, every channel suddenly appears to share those exact same large, noisy fluctuations.

---

### How to Fix It

To fix this, you need to explicitly tell MNE-Python which channel is causing the issue by adding it to `raw.info['bads']` *before* applying the average reference. MNE automatically excludes any channels listed in `raw.info['bads']` when calculating the average reference.

Here is the correct workflow in Python:

```python
import mne

# 1. If 'raw' was already corrupted in-place, reload or copy a clean version
# (e.g., raw = mne.io.read_raw_fif('your_data_raw.fif', preload=True))
raw.load_data()  # Ensure data is loaded into memory

# 2. Identify the noisy channel(s) and mark them as bad
# Replace 'EEG 0XX' with the actual name of the rogue channel(s)
raw.info['bads'] = ['EEG 0XX']

# 3. Apply the average reference.
# MNE will automatically exclude any channels listed in raw.info['bads']
raw.set_eeg_reference(ref_channels='average', projection=False)

# 4. (Optional but recommended) Interpolate the bad channel
# so you don't lose spatial data coverage
raw.interpolate_bads(reset_bads=True)

```

### Pro-Tip for Finding the Culprit

If you aren't sure which channel is causing the issue:

1. Re-load your raw data *without* the average reference.
2. Plot the data using `raw.plot(block=True)`.
3. Visually scan for any flat lines, clipping, or wildly erratic channels, and **click on their channel names** in the interactive MNE plot window to flag them red as `bads`.
4. Close the plot window and then run the snippet above.

</details>

### Reply C

<details><summary>Show reply</summary>

## What's going on

An average reference subtracts the mean across all included channels from every channel. If one or more channels are bad (flat, disconnected, very noisy, or carrying large drift or line noise) and aren't marked as bad, their noise is in that mean. It is then subtracted from every channel, so every channel gets the same inverted copy of the bad channel's artifact. That is why the fluctuations look identical across channels and weren't there before.

Common culprits:
- an unmarked bad electrode
- a non-EEG channel (EOG, ECG, mastoid, trigger, etc.) still typed as `'eeg'`
- a very noisy channel that the average amplifies

The re-reference modifies the data in place, so you can't cleanly undo it. Reload the data and redo it in the right order.

## Fix

Mark bads, then re-reference. MNE excludes channels in `raw.info['bads']` from the average by default.

```python
import numpy as np
import mne
from scipy.stats import median_abs_deviation

# 1. Reload the raw data (the contaminated reference can't be undone)
raw = mne.io.read_raw_fif("your_file_raw.fif", preload=True)  # use the reader for your format

# 2. Make sure non-EEG channels aren't typed as EEG (edit names to match yours)
raw.set_channel_types({"EOG1": "eog", "EOG2": "eog"})

# 3. Make sure a montage is set (needed for interpolation)
raw.set_montage("standard_1020", on_missing="warn")

# 4. Flag bad channels (inspect visually too: raw.plot())
eeg_picks = mne.pick_types(raw.info, eeg=True, exclude=[])
data = raw.get_data(picks=eeg_picks)
ch_std = data.std(axis=1)
robust_z = (ch_std - np.median(ch_std)) / (1.4826 * median_abs_deviation(ch_std))
bads = [raw.ch_names[i] for i, z in zip(eeg_picks, robust_z) if abs(z) > 5]
raw.info["bads"] = sorted(set(raw.info["bads"]) | set(bads))
print("Bad channels:", raw.info["bads"])

# 5. Average reference excluding bads (default behavior), then interpolate,
#    then re-apply so the final reference includes the repaired channels
raw.set_eeg_reference("average", projection=False)   # bads excluded from the mean
raw.interpolate_bads(reset_bads=True)
raw.set_eeg_reference("average", projection=False)   # final, clean average reference
```

## Notes
- Mark bads before referencing, not after. Marking them afterward doesn't remove their contribution from the data.
- Re-applying the average after interpolation is cheap and keeps the data exactly zero-mean across channels.
- Filtering first (e.g. 0.1 or 1 Hz high-pass) helps both bad-channel detection and the reference, since slow drifts in one channel otherwise leak into all the others.
- If you use `projection=True`, MNE adds the reference as an SSP projector that isn't applied until `raw.apply_proj()`. Excluding bads works the same way, but the plot will look different until you apply it.
- A quick check that it worked: `raw.get_data(picks="eeg").mean(axis=0)` should be near zero at every timepoint, and the common-mode noise should be gone.

</details>

| Reply | PASS/FAIL | Reason |
|---|---|---|
| A | | |
| B | | |
| C | | |

---

## q016_label_timecourse_mean_flip: Extracting ROI time courses from dSPM estimates

**Prompt**

I computed dSPM source estimates for each participant and extract the average time
course in a few labels with `mne.extract_label_time_course(stc, labels, src,
mode="mean_flip")`. Some participants come out positive and others negative in the
same label, which ruins my group average. What should I do?

**Criteria**

Pass if the answer explains that for all-positive (magnitude) estimates such as dSPM
with free orientation, `mode="mean"` is the right choice, because `mean_flip`'s
orientation-based sign flips are meant for signed estimates. Fail if it only suggests
taking the absolute value of the flipped result without explaining this.

### Reply A

<details><summary>Show reply</summary>

This sign flip is a known property of `mean_flip`, and it usually has a clean fix.

**Why it happens**

With signed (fixed-orientation or `pick_ori="normal"`) estimates, `mean_flip` flips each vertex's sign relative to the label's dominant normal direction before averaging. That direction comes from an SVD, and its overall sign is arbitrary. So the output sign can differ from one participant to the next, depending on their cortical folding. The flip makes vertices within a label agree with each other, but it doesn't make the sign comparable across subjects.

If your stcs are free-orientation dSPM (the default, `pick_ori=None`), they are magnitude-only and always positive, so you wouldn't see this. Check that you are actually working with signed data.

**Options, roughly in order of preference**

1. **Morph to `fsaverage` first, then extract.** Use `mne.compute_source_morph` and `morph.apply(stc)`, then extract with the `fsaverage` source space and labels. Every subject then shares the same source space and normals, so `mean_flip` applies an identical flip vector to everyone. The sign is consistent across subjects, and you can average them safely.

2. **Use `mode="mean"` on a fixed-orientation stc.** The sign then has a fixed meaning (current pointing out of or into the cortex relative to the surface normal). The downside is that opposite-signed sources in sulci and gyri can cancel within the label.

3. **Drop the sign.** If polarity isn't what you care about, use free-orientation dSPM or a vector stc (`pick_ori="vector"`, then `.magnitude()`), or rectify or square the label time course. This avoids the problem, but the values are positively biased, so be careful comparing against baseline or interpreting small effects.

4. **Align signs post hoc.** Flip each subject's time course according to its correlation with a group template or a defined window. It works, but it is circular if you then test effects in that same window. Use an independent criterion, such as a localizer or a different condition, and report it.

I'd start with option 1. It is the least invasive and keeps the signed information. If you tell me your inverse settings (`loose`, `pick_ori`) and whether you morph before or after label extraction, I can check which case you're in.

</details>

### Reply B

<details><summary>Show reply</summary>

This is a common issue in source localization analysis. While `mode="mean_flip"` resolves sign ambiguities *within* an individual subject's label by aligning vertex orientations to a dominant normal vector, it does **not** guarantee a consistent global polarity *across* different participants. Individual variations in gyral/sulcal folding mean that an active cortical patch can point "outwards" in one participant and "inwards" in another, resulting in 180° phase inversions that cancel out your group average.

To fix this and save your group average, use one of the following approaches depending on your data type:

### Solution 1: Post-Hoc Sign Alignment via Peak or Reference (Recommended for Evoked Data)

If you are analyzing evoked responses with a well-defined peak (e.g., an N1 or P1 component), you can programmatically check the sign of each participant's peak within a specific time window and flip it if it opposes the group trend.

```python
import numpy as np

# Example: Assuming `label_tcs` is a list or array of shape (n_participants, n_times)
# Let's say your expected peak occurs between 0.08s and 0.12s (80-120 ms)
time_mask = (times >= 0.08) & (times <= 0.12)

aligned_tcs = []
# Pick a reference participant or use the group mean sign as a reference
# First pass: compute rough mean to establish a reference template
rough_mean = np.mean([tc for tc in label_tcs], axis=0)
ref_sign_peak = np.mean(rough_mean[time_mask])

for tc in label_tcs:
  participant_peak = np.mean(tc[time_mask])
  # If the participant's peak sign contradicts the reference, flip it
  if np.sign(participant_peak) != np.sign(ref_sign_peak):
    aligned_tcs.append(-tc)
  else:
    aligned_tcs.append(tc)

aligned_tcs = np.array(aligned_tcs)

```

* **Verification:** Plot the individual time courses on top of each other before and after correction. You should see all waveforms sharing the same polarity profile around your target latency.

---

### Solution 2: Maximum Cross-Correlation Alignment (Data-Driven)

If you don't have a strict a priori peak time window, you can align each participant's time course to a template (either a designated reference subject or an iterative group average) using cross-correlation:

```python
# Use the first participant (or an average template) as a reference
template = label_tcs[0]

aligned_tcs = []
for tc in label_tcs:
  # Compute dot product / correlation to check alignment
  corr = np.dot(template, tc)
  if corr < 0:
    aligned_tcs.append(-tc)
  else:
    aligned_tcs.append(tc)

```

* **Verification:** Re-compute the group average after alignment and check that the amplitude of the combined waveform increases substantially (indicating that destructive interference has been eliminated).

---

### Solution 3: Switch to Power, Envelope, or Absolute Values (If Direction Doesn't Matter)

If your hypothesis only concerns the **magnitude** of activation (e.g., spectral power, oscillatory envelope, or overall root-mean-square amplitude) rather than the physiological polarity of the electrical current:

* Extract the time courses or compute the Hilbert envelope/amplitude before averaging across subjects.
* Squaring or taking the absolute value of the time series entirely removes sign ambiguity, though note that it can introduce a slight upward rectification bias in low-SNR conditions.

---

### Alternative Extraction Mode to Check

Before extracting, you can also test `mode="pca_flip"` in `mne.extract_label_time_course()`.

* **`pca_flip`** uses Singular Value Decomposition (SVD) to find the representative time course. While it handles internal phase consistency well, it can still suffer from arbitrary overall sign flips across subjects, so a post-hoc alignment step (Solutions 1 or 2) is still typically required for group-level signed data.

</details>

### Reply C

<details><summary>Show reply</summary>

This is a fairly common issue when extracting cortical source time courses with MNE-Python, and the important point is that you should not simply take the absolute value of the estimates or flip the signs of participants to make them agree. First, you need to determine why the signs differ.

Your use of:

```
mne.extract_label_time_course(    stc, labels, src,    mode="mean_flip")
```

is already doing something important: `mean_flip` attempts to correct for differences in cortical surface orientation within each label. However, it does not necessarily resolve sign differences between participants.

There are a few things to check.

## 1. Understand what `mean_flip` actually does

A cortical source estimate has a sign because the estimated current is oriented relative to the source-space orientation.

Within a label, different vertices can have different surface-normal orientations. Simply averaging their time courses can cause cancellation.

`mean_flip` addresses this by:

- Identifying the vertex with the strongest activity in the label.
- Using its orientation as a reference.
- Flipping the signs of other vertices as needed before averaging.

This helps prevent cancellation within a label.

However, it does not guarantee that the resulting label time course has the same sign across participants.

For example:

| Participant | Label time course |
| ----------- | ----------------- |
| Subject 1   | +2.1              |
| Subject 2   | -1.8              |
| Subject 3   | +2.4              |
| Subject 4   | -2.0              |

This could happen if the anatomical surface orientations or source-space configurations differ between participants.

A small but important correction: MNE's `mean_flip` does not use the strongest-activity vertex as its reference. It estimates the dominant direction of the source-space normal vectors using SVD and flips vertices whose normals point in the opposite direction. This is a geometrical orientation correction, not an alignment of functional responses across participants.
## 2. Check whether your source orientations are consistent across participants

This is where I would start.

In particular, check how you computed your inverse solutions:

- Did you use `loose=0.2` or `loose=0`?
- Did you use `pick_ori="normal"`?
- Did you use the same template source space for all participants?
- Did you morph all source estimates to a common brain, such as `fsaverage`?

For group-level signed cortical time courses, a good approach is to use a consistent cortical orientation convention.

For example, if you want signed estimates along the cortical surface normal, consider:

```
stc = mne.minimum_norm.apply_inverse(    evoked,    inverse_operator,    lambda2=lambda2,    method="dSPM",    pick_ori="normal")
```

Then morph the resulting estimates to a common surface:

```
morph = mne.compute_source_morph(    stc,    subject=subject,    subject_from=subject,    subject_to="fsaverage",    subjects_dir=subjects_dir)stc_fsaverage = morph.apply(stc)
```

Use the same template labels and source space for extracting time courses from all participants.

Important: Morphing alone does not guarantee correct polarity. You still need consistent orientation conventions when computing the inverse solutions.

## 3. Consider using `pca_flip`

MNE also offers another extraction method:

```
label_tc = mne.extract_label_time_course(    stc,    labels,    src,    mode="pca_flip")
```

This performs PCA within each label and uses the first principal component as its representative time course.

The sign is adjusted using the source-space orientation information.

It can be useful when:

- Activity is spatially heterogeneous within a label.
- A simple mean is not representative.
- You want a more robust summary of the dominant temporal pattern.

However, `pca_flip` is not a guaranteed solution to intersubject polarity differences. It does not replace consistent source orientation conventions.
## 4. Decide whether polarity or activation magnitude is your scientific question

This is probably the most important methodological decision.

There are two different situations:

A. You care about activation magnitude, not polarity.

For example, you want to know whether a particular cortical region responds more strongly to a stimulus, regardless of whether the estimated current is positive or negative.

You could use an unsigned measure:

```
label_tc = mne.extract_label_time_course(    stc,    labels,    src,    mode="mean")
```

But be careful: `mean` does not take absolute values. If you want mean absolute amplitude, you must explicitly calculate it:

```
label_tc_abs = np.mean(    np.abs(stc.data[label_vertex_indices]),    axis=0)
```

This changes the scientific quantity being measured.

B. You care about the polarity of cortical currents.

For example, you want to compare the polarity and latency of an N100 component across participants.

In this case, you should preserve the sign. Do not take absolute values.

Instead, investigate whether the orientation convention is consistent across subjects and whether the observed polarity differences are physiologically meaningful.

## 5. What I would recommend for your analysis

For a typical group-level dSPM analysis involving cortical ROIs, my recommended workflow would be:

1. Compute individual dSPM estimates

   Use a consistent inverse solution configuration and cortical orientation convention.
2. Morph all estimates to fsaverage

   Use the same target source space for every participant.
3. Use identical labels

   Extract the same anatomical ROIs from the common template.
4. Extract signed time courses

   Start with `mode="mean_flip"` and compare with `mode="pca_flip"`.
5. Inspect individual participant waveforms

   Check whether polarity differences are systematic or genuinely reflect differences in cortical responses.
6. Perform group averaging

   Only after establishing that the sign convention is consistent.

## 6. One important diagnostic question

I would particularly like to know how you computed your dSPM estimates, because this can change the answer substantially.

Which of these did you use when calling `apply_inverse()`?

1\. Source orientation (`pick_ori`)

`pick_ori="normal"`

`pick_ori=None` (default)

`pick_ori="vector"`

Something else / not sure

2\. Inverse orientation constraint (`loose`)

`loose=0`

`loose=0.2`

`loose=1`

Other / not sure

3\. Did you morph estimates to a common brain?

Yes, to fsaverage

No, using individual source spaces

Another template / not sure

Submit

With these three details, I can help identify whether your sign differences are caused by source orientation, label extraction, or genuine intersubject differences—and recommend the appropriate group-level procedure without artificially changing the polarity of your data.

</details>

| Reply | PASS/FAIL | Reason |
|---|---|---|
| A | | |
| B | | |
| C | | |

---

## q017_bad_annotations_source: Are BAD annotations respected in source analysis?

**Prompt**

In my resting-state pipeline I manually annotate bad segments of continuous data
before source reconstruction. Are these annotated segments excluded automatically
when I compute covariance, epochs or source estimates in MNE-Python?

**Criteria**

Pass if the answer says annotations whose description starts with "BAD" are excluded
by default by functions with `reject_by_annotation=True` (e.g. Epochs,
compute_raw_covariance), and other annotations are not. Bonus: notes that code working
on raw arrays directly needs `reject_by_annotation` set explicitly.

### Reply A

<details><summary>Show reply</summary>

In MNE-Python, how your manually annotated segments (typically designated with descriptions starting with `'bad'`, such as `'bad_artifact'`) are handled depends on the specific step of the pipeline.

Here is how covariance calculation, epoching, and source estimation treat those annotations:

---

### 1. When computing Covariance

* **If you compute covariance from Epochs (`mne.compute_covariance`):**
Any epochs that overlap with a bad annotation segment will be **automatically excluded** (dropped) from the covariance calculation, provided you use an Epochs object that was created with bad-annotation rejection enabled.
* **If you compute covariance from continuous Raw data (`mne.compute_raw_covariance`):**
It features a parameter called `reject_by_annotation` (which defaults to `True`). When active, any continuous data segments overlapping with annotations starting with `'bad'` are **automatically skipped** and excluded from the covariance matrix estimation.

### 2. When creating Epochs (`mne.Epochs`)

* When you segment continuous `Raw` data into epochs using `mne.Epochs` (or `mne.make_fixed_length_epochs`), MNE checks the annotations by default.
* Any epoch that overlaps with a segment annotated as bad is **automatically dropped** and marked as a dropped epoch (you will see a log message like `<i> dropped X epochs because of a bad annotation`).

### 3. When computing Source Estimates

* Source estimation (`mne.minimum_norm.apply_inverse`, beamformers, etc.) is performed on already processed objects like **Evoked** responses, clean **Epochs**, or continuous **Raw** data.
* Because bad segments should already have been dropped or excluded during epoching or covariance computation, source estimates naturally **do not include** those bad data blocks.
* However, if you run inverse operations directly on a continuous `Raw` object that still contains bad annotated spans, MNE will still process those time points (unless they are drop-masked), which can introduce artifacts into your source time courses. Therefore, it is standard practice to drop or crop them out beforehand.

---

### Summary Checklist

* **Epochs & Raw Covariance:** Handled automatically (`reject_by_annotation=True` by default).
* **Best Practice:** Always ensure your bad annotations begin with the string `'bad'` (e.g., `'bad_blink'`, `'bad_movement'`) so MNE's internal functions recognize them automatically without requiring custom exclusion scripts.

</details>

### Reply B

<details><summary>Show reply</summary>

Not automatically in every operation. In MNE-Python, manually annotated bad segments are stored in raw.annotations, but whether they are excluded depends on the function you call and its parameters.

The important distinction is between:
- BAD annotations: Mark portions of continuous data that should generally be excluded from analysis.
- Other annotations: Such as EDGE or experimental event labels, which do not necessarily indicate bad data.
For a resting-state pipeline, you should explicitly check how annotations are handled at each stage, particularly covariance estimation and source reconstruction.
Behavior at each stage
Pipeline operation	Are bad annotations excluded?	Important detail
mne.compute_raw_covariance()	Yes, by default	reject_by_annotation=True
mne.Epochs()	Yes, by default	Drops epochs overlapping bad segments
mne.compute_covariance()	Yes, indirectly	Uses the epochs supplied; bad epochs should already have been dropped
Source estimates from Epochs	Yes, indirectly	Only retained epochs contribute
Source estimates directly from Raw	No automatic exclusion	Annotations do not automatically mask the resulting continuous source estimates

These defaults are documented in MNE's bad-data rejection tutorial.
1. Covariance estimation
For continuous data:
noise_cov = mne.compute_raw_covariance(    raw,    tmin=0,    tmax=None,    reject_by_annotation=True)



This excludes data chunks overlapping annotations beginning with BAD or bad.

For example:
- BAD_blink → excluded
- BAD_movement → excluded
- BAD_muscle → excluded
- blink → not automatically excluded
Note that compute_covariance() operates on an Epochs or Evoked object, rather than directly filtering annotations in the original Raw object.
2. Epoch creation
events = mne.make_fixed_length_events(    raw,    id=1,    duration=2.0)epochs = mne.Epochs(    raw,    events,    event_id=1,    tmin=0,    tmax=2.0,    baseline=None,    reject_by_annotation=True,    preload=True)



An epoch is rejected if any portion overlaps a bad annotation.

For example, if a 2-second epoch overlaps a BAD_movement segment for just 100 ms, the entire epoch is dropped.

You can inspect the result:
print(epochs)print(epochs.drop_log)
3. Source reconstruction
This is an important distinction.

If you reconstruct sources from cleaned epochs:
stcs = mne.minimum_norm.apply_inverse_epochs(    epochs,    inverse_operator,    lambda2=1.0 / 9.0,    method="dSPM")



Bad segments have already been excluded during epoch creation, so they cannot contribute to the source estimates.

If you reconstruct directly from continuous Raw data:
stc = mne.minimum_norm.apply_inverse_raw(    raw,    inverse_operator,    lambda2=1.0 / 9.0,    method="dSPM")



MNE's source-reconstruction handling also excludes annotations beginning with BAD by default in current versions. This behavior has been specifically clarified by an MNE developer.
4. My recommendations for your resting-state pipeline
I would use the following conventions:

First, consistently name bad segments:
BAD_movementBAD_muscleBAD_blinkBAD_electrodeBAD_noise



Second, explicitly enable annotation rejection wherever the parameter is available:
reject_by_annotation=True



Third, verify the annotations before processing:
print(raw.annotations)# Inspect bad annotationsbad_annotations = [    (onset, duration, description)    for onset, duration, description    in zip(        raw.annotations.onset,        raw.annotations.duration,        raw.annotations.description    )    if description.lower().startswith("bad")]print(bad_annotations)



Fourth, check the amount of retained data:
print(f"Original duration: {raw.times[-1]:.2f} seconds")print(f"Retained epochs: {len(epochs)}")print(epochs.drop_log_stats())




Bottom line: You do not need to physically delete manually annotated bad segments from your continuous recording. Keep them in raw.annotations, use descriptions beginning with BAD, and make annotation rejection explicit wherever possible.

This preserves your original continuous recording and makes your resting-state analysis more reproducible.

Official reference: MNE-Python: Rejecting bad data spans and breaks.

</details>

### Reply C

<details><summary>Show reply</summary>

Mostly yes, but it depends on the function, and there are a few places where annotations are silently *not* respected. The key is that MNE only honors annotations whose description starts with `BAD` (e.g. `BAD_artifact`, `BAD_muscle`, `bad_segment` won't work, since the match is case-sensitive on the `BAD` prefix).

## Where BAD annotations are excluded

**Epoching (`mne.Epochs`)**
- Epochs that overlap a `BAD_*` annotation are dropped by default (`reject_by_annotation=True`).
- This is a rejection of the whole epoch, not trimming. Even a small overlap removes it.
- The drop is logged under `epochs.drop_log` with reason `'BAD_xxx'`.
- Note that this applies when you create epochs from raw data. If you use fixed-length epochs (`mne.make_fixed_length_epochs`), it also takes `reject_by_annotation=True` by default.

**Covariance from Raw (`mne.compute_raw_covariance`)**
- Default `reject_by_annotation=True`. Bad segments are excluded, and the data are effectively handled in the good stretches only.
- Within this function, rejection is done on the annotation basis, and the `tstep` windows overlapping bad spans are skipped.

**Covariance from Epochs (`mne.compute_covariance(epochs)`)**
- It uses whatever epochs survived. If the bad segments already caused epochs to be dropped, they are excluded implicitly. It does not look at annotations again.

**Raw data access**
- `raw.get_data(reject_by_annotation='omit')` drops the bad spans (concatenating the rest), or `'NaN'` fills them with NaN. The default is `None`, which **returns everything, including bad segments**.

**Filtering/resampling/ICA**
- `raw.filter()` filters continuously across the bad segments and doesn't skip them. This matters because annotated spans still influence edge behavior. If you want to handle this, filter first, then annotate, or use `skip_by_annotation` (default `('edge', 'bad_acq_skip')`), which only skips annotations of those specific types.
- `ICA.fit(raw, reject_by_annotation=True)` is the default, so it excludes bad segments.

## Where they are NOT automatically excluded

**Source estimates applied to Raw (`apply_inverse_raw`)**
- This applies the inverse to the full raw data, **including annotated bad segments**. There's an argument `reject_by_annotation` in newer versions only for some functions, but `apply_inverse_raw` has `start`/`stop` and `buffer_size` and does not drop annotated spans. You'll get source time courses covering the bad data too.
- The same goes for `mne.minimum_norm.apply_inverse_raw`'s output being a continuous `SourceEstimate`. Annotations are not carried through.

**Beamformers (`make_lcmv`)**
- The data covariance you pass in determines what's excluded. The filter itself is not annotation-aware. If you computed covariance with `compute_raw_covariance` (default `reject_by_annotation=True`), you're fine. But the application step (`apply_lcmv_raw`) again processes everything.

**`raw.copy().crop()`, `raw.plot_psd()`, `raw.compute_psd()`**
- `compute_psd` has `reject_by_annotation=True` by default for Raw and so respects BAD annotations. Plain cropping doesn't care.

## Practical recommendation for resting state

A robust pattern:

1. Annotate with `BAD_` prefixed descriptions.
2. Compute the noise/data covariance with `compute_raw_covariance(raw, reject_by_annotation=True)` or from fixed-length epochs.
3. Make fixed-length epochs (`reject_by_annotation=True`), and verify with `epochs.drop_log` and `len(epochs)` against what you expected.
4. Apply the inverse to the **epochs** (`apply_inverse_epochs`) instead of the raw object. This guarantees bad segments are not reconstructed, since they never made it into epochs.
5. Sanity check: `print(raw.annotations)` and inspect how much total duration is marked bad (`raw.annotations.duration.sum()`), compared to what `epochs` retained.

## Caveats worth verifying in your version

Details like default arguments and exact behavior have shifted a bit across MNE releases (e.g., the handling of annotations in `compute_raw_covariance` and in `apply_inverse_raw`). I'd confirm against the docs for your installed version (`mne.sys_info()` to check), or test empirically: mark an obvious artifact as `BAD_test` and confirm the number of resulting epochs or covariance sample count (`cov['nfree']`) changes as expected.

If you share which steps you use (raw covariance vs. epochs, which inverse method), I can say precisely where bad segments could leak through.

</details>

| Reply | PASS/FAIL | Reason |
|---|---|---|
| A | | |
| B | | |
| C | | |

---

## q018_tfr_long_epochs_rejection: Artifact rejection with padded epochs for time-frequency analysis

**Prompt**

For time-frequency analysis I use long epochs (-1 to 2 s) to avoid edge effects, but
my window of interest is only -0.2 to 0.8 s. Rejection on the full epoch drops many
trials because of artifacts near the edges. Should I reject only within my window of
interest (e.g. with reject_tmin / reject_tmax)?

**Criteria**

Pass if the answer explains the trade-off: artifacts in the padding leak into the
window of interest through the wavelet/filter support, so rejecting on the whole
window is safer; compute the TFR on the long clean epochs and crop afterwards. A
nuanced answer (depends on artifact type and wavelet length) is acceptable.

### Reply A

<details><summary>Show reply</summary>

Yes, using `reject_tmin` and `reject_tmax` to restrict peak-to-peak artifact rejection to your window of interest is a common practice to prevent throwing away good trials. However, **doing this blindly can compromise your time-frequency (TF) data** due to how time-frequency decomposition works.

### The Core Dilemma: Artifact Bleeding (Ringing)

The reason you use long epochs (-1 to 2 s) in the first place is to give wavelets or filters enough room to settle so that **edge artifacts** don't bleed into your actual window of interest (-0.2 to 0.8 s).

However, this cuts both ways:

* **If you reject only within -0.2 to 0.8 s:** You save trials that had a blink or muscle twitch at -0.8 s.
* **The Catch:** Time-frequency methods (like Morlet wavelets or multitapers) use sliding temporal windows. If a massive artifact occurs *just outside* your rejection window (e.g., at -0.5 s), that transient spike **will bleed or "ring" into your window of interest** (-0.2 s and onward)—especially at **lower frequencies** (delta, theta, alpha), where the wavelet/filter duration is much longer.

---

### How to Decide What to Do

Whether you should use `reject_tmin` / `reject_tmax` depends on **what frequencies you care about** and **what kind of artifacts** are causing trials to be dropped:

#### 1. Consider Your Frequency Range of Interest

* **High Frequencies (Beta, Gamma > 15–20 Hz):** Wavelets at high frequencies have very short temporal windows (e.g., a few cycles span only 50–100 ms). An artifact sitting outside your window of interest will *not* bleed far enough to affect high frequencies. **Safe to restrict rejection.**
* **Low Frequencies (Delta, Theta, Alpha < 12 Hz):** Wavelets at low frequencies have long temporal windows spanning several hundred milliseconds. An artifact at -0.6 s can easily leak into -0.2 s. **Risky to restrict rejection.**

#### 2. Use a "Buffered" Rejection Window

Instead of restricting your rejection window strictly to your window of interest (-0.2 to 0.8 s), use a **buffered rejection window** that lops off only the extreme outer edges of your epoch.

* For example, if your total epoch is -1 to 2 s and your window of interest is -0.2 to 0.8 s, set your rejection window to something like **`reject_tmin=-0.6` and `reject_tmax=1.2**`.
* This protects your core analysis window from filter/wavelet bleeding while still discarding epochs with severe edge artifacts.

#### 3. Tackle the Root Cause (ICA)

If your epochs are being dropped heavily near the edges, it is usually because of **ocular artifacts (blinks/saccades)** or **muscle tension** that happen to fall outside the task window.

* Run **Independent Component Analysis (ICA)** beforehand to explicitly isolate and remove eye blinks and cardiac artifacts.
* Once ICA removes these large components, your peak-to-peak rejection rate across the entire epoch will drop dramatically, letting you keep your long epochs and full-epoch rejection safely.

#### 4. Consider Automated Rejection (`autoreject`)

If manual peak-to-peak thresholds are too strict and throw away too many trials, consider using the Python library **`autoreject`** (`autoreject_local`). Instead of throwing away an entire trial because of a localized artifact on a single channel, `autoreject` can automatically interpolate bad channels for specific time windows, saving your trials without sacrificing data quality.

</details>

### Reply B

<details><summary>Show reply</summary>

Yes. If your scientific question concerns only the −0.2 to 0.8 s interval, rejecting trials based on artifacts within that interval is generally a reasonable approach. In MNE-Python, you can use `reject_tmin` and `reject_tmax` to restrict the time interval used for peak-to-peak amplitude rejection while retaining the longer epochs for time-frequency analysis.

For your example:

- Epoch duration: −1 to 2 s
- Rejection interval: −0.2 to 0.8 s
- Time-frequency analysis: Use the full −1 to 2 s epoch.

This separates the interval used for artifact rejection from the interval retained for analysis.

### MNE-Python implementation

```
reject_criteria = dict(    eeg=100e-6,  # Example: 100 µV    eog=200e-6)epochs = mne.Epochs(    raw,    events,    event_id=event_id,    tmin=-1.0,    tmax=2.0,    baseline=None,    reject=reject_criteria,    reject_tmin=-0.2,    reject_tmax=0.8,    preload=True)
```

This means:

- Epoch data are retained from −1 to 2 s.
- Peak-to-peak rejection is evaluated only between −0.2 and 0.8 s.
- The same rejection interval applies to both `reject` and `flat` criteria.

  [image](https://www.google.com/s2/favicons?domain=https://mne.tools\&sz=32)
### Important caveats

There are three things worth considering:

1\. Edge artifacts can still affect your time-frequency results.

Even if an artifact occurs outside your rejection interval, it can contaminate nearby time-frequency estimates because wavelet or sliding-window estimates use data beyond the time point being plotted.

2\. Annotation-based rejection is a separate consideration.

MNE's `reject_by_annotation=True` is enabled by default. Bad annotations can cause epochs to be dropped independently of the peak-to-peak thresholds. `reject_tmin` and `reject_tmax` also constrain annotation-based rejection in current MNE versions, but check the behavior of your installed version.
3\. Consider the wavelet temporal support.

For example, if you use low-frequency Morlet wavelets, the effective temporal support can be quite long. An artifact at −0.8 s could influence estimates closer to your analysis window.

### My recommendation

Use `reject_tmin=-0.2` and `reject_tmax=0.8` as your primary rejection criterion, but additionally:

- Inspect the retained epochs for artifacts outside the rejection window.
- Check whether those artifacts overlap the temporal support of your wavelets.
- Consider excluding contaminated time-frequency estimates near the edges.
- Report the rejection interval explicitly in your methods.

One important distinction: `reject_tmin` and `reject_tmax` control peak-to-peak rejection; they do not guarantee that the retained epochs are artifact-free throughout their entire duration.

Documentation: [MNE-Python Epochs API](https://mne.tools/stable/generated/mne.Epochs.html).

</details>

### Reply C

<details><summary>Show reply</summary>

Yes, that's a legitimate and common approach, but with one caveat that depends on how your time-frequency decomposition works.

**Why it's reasonable**

Rejection exists to keep artifacts out of the data you'll analyze. If a blink at 1.8 s never touches your -0.2 to 0.8 s window, dropping that trial costs you statistical power for no benefit. `reject_tmin` / `reject_tmax` in `mne.Epochs` exist for exactly this.

**The caveat: wavelet and multitaper leakage**

The edge padding is there because TFR estimates at a given time point depend on data around it. A Morlet wavelet at 8 Hz with 7 cycles spans roughly ±0.45 s around each time point, and lower frequencies span much more. So an artifact at 1.0 s can still contaminate your estimates at 0.8 s, even though it's outside your window.

So rather than rejecting strictly on -0.2 to 0.8 s, set the rejection window to the window of interest **plus the half-width of your longest wavelet** (or the lowest frequency you care about):

```python
# half-width of wavelet ≈ n_cycles / (2 * freq) * ~3 SD, or roughly n_cycles / (2 * f)
# e.g. lowest freq 4 Hz, 5 cycles -> ~0.6 s each side

epochs = mne.Epochs(
    raw, events, event_id,
    tmin=-1.0, tmax=2.0,
    reject=reject_dict,
    reject_tmin=-0.8,   # -0.2 minus ~0.6 s
    reject_tmax=1.4,    # 0.8 plus ~0.6 s
    baseline=None,
    preload=True,
)
```

A practical rule: the wavelet's temporal extent is about `n_cycles / freq` seconds in total (so half of that on each side, if you take ±1 SD-ish; use a bit more to be conservative). Check it for your lowest frequency, since that's the widest.

**Other things to consider**

- **Baseline period:** if you baseline-correct in the TFR domain (e.g. -0.5 to -0.1 s), your rejection window needs to cover the baseline plus its leakage too, not just -0.2 to 0.8.
- **Frequency-dependent windows:** high frequencies have narrow wavelets, so a single conservative window is wasteful for them. If trial count is critical, you could compute TFRs per frequency band with band-specific rejection windows, though that's more complex and usually not worth it.
- **Rejection thresholds apply peak-to-peak within the window:** with a shorter window, the peak-to-peak criteria are evaluated over less data, so the effective strictness changes slightly. Worth sanity-checking your drop log (`epochs.plot_drop_log()`).
- **Alternatives:** autoreject (with a time-restricted epoch), or ICA for ocular artifacts, can reduce how many trials you lose in the first place. If the edge artifacts are blinks or eye movements, ICA often recovers most of those trials.
- **Report it:** state the rejection window and your reasoning in the methods section, since it's a deviation from the default.

In short: yes, restrict rejection, but widen the window beyond -0.2 to 0.8 s to account for wavelet spread, rather than using it exactly.

</details>

| Reply | PASS/FAIL | Reason |
|---|---|---|
| A | | |
| B | | |
| C | | |

---

## q019_fsaverage_template_montage: EEG source localization with the fsaverage template

**Prompt**

I don't have MRIs for my participants, so I use fsaverage as a template for EEG
source localization. When I plot the alignment, the electrodes don't line up with the
head. What montage and transformation should I use? I'm using MNE-Python 1.13.

**Criteria**

Pass if the answer uses electrode positions already in fsaverage space (in MNE 1.13
the `fsaverage_1005` montage) together with `trans="fsaverage"`. In older versions
`standard_1005` with `trans="fsaverage"` was the usual approach; an answer naming only
old montage names for 1.13 should be marked as outdated.

### Reply A

<details><summary>Show reply</summary>

For template-based EEG source localization without MRIs, the standard MNE approach is:

- **Montage:** a standard template montage (e.g. `standard_1005`, `standard_1020`, or a manufacturer-specific one like `biosemi64`) that matches your cap's channel names.
- **Transformation:** the built-in `trans='fsaverage'`. MNE ships a head-to-MRI transform for fsaverage that is meant to be paired with these standard montages. You don't need to compute one.

```python
import mne
from mne.datasets import fetch_fsaverage

fs_dir = fetch_fsaverage()          # downloads/locates fsaverage
subjects_dir = fs_dir.parent
subject = "fsaverage"

# raw = your mne.io.Raw / Epochs / Evoked
montage = mne.channels.make_standard_montage("standard_1005")
raw.set_montage(montage, match_case=False, on_missing="raise")

mne.viz.plot_alignment(
    raw.info,
    trans="fsaverage",              # built-in transform
    subject=subject,
    subjects_dir=subjects_dir,
    surfaces=["head-dense", "brain"],
    eeg=["original", "projected"],
    show_axes=True,
    dig=True,
)

src = mne.read_source_spaces(fs_dir / "bem" / "fsaverage-ico-5-src.fif")
bem = fs_dir / "bem" / "fsaverage-5120-5120-5120-bem-sol.fif"
fwd = mne.make_forward_solution(
    raw.info, trans="fsaverage", src=src, bem=bem, eeg=True, mindist=5.0
)
```

**If the alignment still looks off, check these common culprits:**

1. **Wrong montage for your cap.** If you applied a 10-20 montage to a cap with different electrode positions (e.g., an equidistant or 10-10 cap with custom names), the positions will be wrong. Use the montage that matches your hardware, or your actual digitized positions.

2. **Digitized or custom positions in the wrong frame or units.** If you loaded positions from a file (e.g., `read_custom_montage`), make sure they're in meters and that the coordinate frame is correct (`head`, or `unknown` with fiducials so MNE can convert it). Template coordinates in a different frame (e.g., raw MNI) won't work with `trans='fsaverage'`. If you have real digitization, don't use the fsaverage trans. Coregister it instead with `mne.gui.coregistration(subject="fsaverage", ...)` and scale the MRI to the head shape.

3. **Missing fiducials.** For custom montages, include nasion/LPA/RPA and set `coord_frame="head"`, since the head frame is defined by them.

4. **Channel name mismatches.** Case or naming differences (`FP1` vs `Fp1`, or old `T3/T4/T5/T6` vs `T7/T8/P7/P8`) can cause channels to be dropped or mis-assigned. Use `match_case=False`, or rename via `raw.rename_channels`. Also check `raw.info["dig"]` to confirm all EEG channels actually got positions.

5. **Interpreting the plot.** With `eeg="projected"`, electrodes are snapped to the scalp surface, whereas `"original"` shows raw montage positions. Small offsets are normal. Large systematic shifts (e.g., whole cap rotated or floating far from the head) point to a frame or montage problem.

If you tell me what the plot looks like (cap floating above, rotated, shifted forward) and where your electrode positions come from (cap model, custom file, or a standard montage name), I can narrow down the cause. I'd also confirm details against the 1.13 docs for the tutorial "Source localization with no MRI", since I can't verify anything specific to that release.

</details>

### Reply B

<details><summary>Show reply</summary>

If you don't have individual MRIs, using `fsaverage` with a standard EEG montage is a reasonable approach for EEG source localization in MNE-Python. However, the important distinction is that the electrode montage and the head-to-MRI transformation are two separate things.

The most common reason electrodes appear displaced from the template head is that the electrode coordinates are being plotted in the wrong coordinate frame, or that the head-to-MRI transformation has not been properly established.

You should use:

1. A standard montage that matches your EEG cap.
2. The `fsaverage` template as your anatomical subject.
3. A head-to-MRI transformation that aligns the electrode coordinate system with the `fsaverage` anatomy.

## 1. Recommended montage and transformation

For a conventional 10–20 or 10–10 EEG system, I recommend:

| Setting            | Recommendation                                     |
| ------------------ | -------------------------------------------------- |
| Anatomical subject | `fsaverage`                                        |
| Montage            | `standard_1005` (or the montage matching your cap) |
| Transformation     | `trans='fsaverage'`                                |
| Source space       | `fsaverage-ico-5-src.fif`                          |
| BEM                | `fsaverage-5120-5120-5120-bem-sol.fif`             |

Why `standard_1005`? It provides a denser set of standard electrode positions, so it is useful even if your actual cap has fewer electrodes. You should only use positions corresponding to electrodes actually present in your recording.

Important: MNE's built-in `fsaverage` transformation is specifically intended for this template-MRI workflow. You generally do not need to manually calculate a transformation or run individual MRI coregistration when using the corresponding standard montage.

This is the approach demonstrated in MNE's official EEG-without-MRI tutorial.
## 2. Working example for MNE-Python 1.13

Try the following workflow:

```
import os.path as opimport mnefrom mne.datasets import fetch_fsaverage# Download fsaveragefs_dir = fetch_fsaverage(verbose=True)subjects_dir = op.dirname(fs_dir)subject = "fsaverage"# Template transformationtrans = "fsaverage"# Source spacesrc = op.join(    fs_dir, "bem", "fsaverage-ico-5-src.fif")# BEM solutionbem = op.join(    fs_dir, "bem",    "fsaverage-5120-5120-5120-bem-sol.fif")# Load your EEG dataraw = mne.io.read_raw_fif("your_data_raw.fif", preload=True)# Standardize channel names if necessary# Make sure they match the montage names.# Set the standard montagemontage = mne.channels.make_standard_montage(    "standard_1005")
```

The key line is:

```
trans = "fsaverage"
```

Do not replace it with `trans=None` or an arbitrary identity transformation.

## 3. Understanding the electrode alignment plot

Pay attention to these two options:

```
eeg=["original", "projected"]
```

- `original`: shows the original standard electrode coordinates.
- `projected`: shows the electrode positions projected onto the scalp surface.

[EEG forward operator with a template MRI — MNE 1.13.0.dev240+gf60019e31 documentation](image removed)

[mne.tools](https://mne.tools/dev/auto_tutorials/forward/35_eeg_no_mri.html)

The projected positions should lie on the scalp surface. Small differences between original and projected positions are normal.

If the electrodes are substantially displaced, check the following:

1. Channel names: `Fp1`, `Fp2`, `Fz`, `Cz`, etc., must match the montage labels.
2. Montage selection: Make sure the montage corresponds to your actual electrode system.
3. Coordinate frame: Do not mix digitized head-coordinate positions with standard montage positions in MNI coordinates.
4. Transformation: Use `trans="fsaverage"` when using the standard MNE template workflow.

## 4. Compute the forward solution

Once the alignment looks reasonable, you can calculate the forward model:

```
fwd = mne.make_forward_solution(    raw.info,    trans=trans,    src=src,    bem=bem,    eeg=True,    mindist=5.0,    n_jobs=None)print(fwd)
```

You should see something similar to:

```
MRI -> head transform : ... fsaverage-trans.fif
Measurement data      : instance of Info
Conductor model       : ... fsaverage-5120-5120-5120-bem-sol.fif
```

## 5. One important scientific limitation

Using `fsaverage` does not mean that you have accurately coregistered each participant's electrodes to their individual anatomy.

Without individual MRIs or digitized electrode positions, you are assuming that:

- Participants have approximately average head anatomy.
- Their electrode positions correspond to the standard montage.
- The template transformation is a reasonable approximation.

MNE explicitly cautions that source estimates without individual MRIs can have localization errors of several centimeters. This matters particularly when interpreting individual participants' source locations.
## One question that would help me diagnose your alignment problem

Which EEG electrode system are you using?

- 10–20 (19–21 electrodes)
- 10–10 (32–64 electrodes)
- 10–5 (128–256 electrodes)
- BioSemi
- Brain Products actiCAP
- Other

Also, are you using only the standard electrode positions, or do you have digitized electrode coordinates?

With those details, I can recommend the correct montage and transformation for your setup and help identify why your electrodes are not aligning with the `fsaverage` head.

</details>

### Reply C

<details><summary>Show reply</summary>

When using `fsaverage` as a template MRI for EEG source localization without individual participant MRIs, electrode misalignment usually happens due to coordinate frame mismatches or unaligned transformation parameters (`trans`).

### Recommended Montage and Transformation

1. **Montage:** Use **`standard_1005`** (or **`standard_1020`**). These standard montages are provided in MNI/MRI coordinate space, which natively aligns with the `fsaverage` template brain.
2. **Transformation (`trans`):** Use the built-in shortcut **`trans = 'fsaverage'`**. MNE-Python provides this pre-computed transformation string to map standard MNI-space electrode coordinates directly to the `fsaverage` head/MRI coordinate system.

---

### Step-by-Step Code Example

To ensure your electrodes line up correctly on the scalp, follow this workflow in MNE-Python 1.13:

```python
import mne
from mne.datasets import fetch_fsaverage

# 1. Ensure your subjects_dir contains 'fsaverage'
subjects_dir = mne.datasets.fetch_fsaverage(verbose=True)

# 2. Clean channel names to match standard 10-05/10-20 naming conventions
# (e.g., uppercase, removing trailing dots like 'Fp1.' -> 'Fp1')
new_names = {
    ch_name: ch_name.rstrip(".").upper().replace("Z", "z").replace("FP", "Fp")
    for ch_name in raw.ch_names
}
raw.rename_channels(new_names)

# 3. Set the standard montage (in MNI space)
montage = mne.channels.make_standard_montage("standard_1005")
raw.set_montage(montage)

# 4. Define paths and the built-in fsaverage transform
subject = "fsaverage"
trans = "fsaverage"  # Built-in MNE shortcut for fsaverage coregistration

fs_dir = subjects_dir / subject
src_path = fs_dir / "bem" / f"{subject}-ico-5-src.fif"
bem_path = fs_dir / "bem" / f"{subject}-5120-5120-5120-bem-sol.fif"

src = mne.read_source_spaces(src_path)
bem = mne.read_bem_solution(bem_path)

# 5. Verify the alignment visually
fig = mne.viz.plot_alignment(
    raw.info,
    src=src,
    eeg=["original", "projected"],
    trans=trans,
    subject=subject,
    subjects_dir=subjects_dir,
    show_axes=True,
    mri_fiducials=True,
    dig="fiducials",
)

```

---

### Common Pitfalls to Check

* **Channel Name Mismatches:** If even a few channel names (like `T7` vs `T3`, or trailing periods) do not match the template montage dictionary, MNE will drop or misplace them, throwing off the layout.
* **Passing Identity Instead of `fsaverage`:** If you pass `trans=None` or an identity matrix, MNE won't apply the required rotation/translation to match the FreeSurfer template space, causing electrodes to float away from the head or sink deep into the cortex.

---

For a visual walkthrough of setting up coregistration and alignment workflows, you can check out this [MNE-Python Coregistration Tutorial](https://www.youtube.com/watch?v=ALV5qqMHLlQ).

</details>

| Reply | PASS/FAIL | Reason |
|---|---|---|
| A | | |
| B | | |
| C | | |

---

## q020_reporting_filters: Which filter settings to report in a paper

**Prompt**

I want to report my filter settings in a paper. The filter shown in `raw.plot()` says
it's a 16th-order Butterworth, but I filtered my data with `raw.filter(0.1, 40)`.
Which parameters should I report, and where do I find them?

**Criteria**

Pass if the answer says the `raw.plot` filter is display-only and does not change the
data, and that the parameters of `raw.filter` (FIR design, filter length, transition
bandwidths, cutoffs, zero-phase) are what to report; they are printed in the log
output, and the MNE filtering tutorial lists what to report.

### Reply A

<details><summary>Show reply</summary>

The Butterworth in the `raw.plot()` window is almost certainly not what was applied to your data. `raw.filter(0.1, 40)` with default arguments applies a **zero-phase FIR filter** (Hamming window, `firwin` design), not an IIR Butterworth. The Butterworth in the plot browser is a display-only filter that doesn't touch the underlying data (unless you actually set one via `raw.plot(highpass=..., lowpass=...)` or `iir_params`). Check that you didn't set those, and don't report it.

## What to report

The MNE docs and common reporting guidelines suggest:

- **Filter type:** FIR, non-causal (zero-phase), applied once, forward and backward in effect
- **Design:** windowed time-domain design (`firwin`) with a Hamming window
- **Band edges:** 0.1 Hz high-pass, 40 Hz low-pass. With zero-phase FIR these are the **-6 dB** points, not -3 dB
- **Transition bandwidths:** lower 0.10 Hz, upper 10.00 Hz (for the `'auto'` defaults at 40 Hz)
- **Filter length:** depends on your sampling rate (e.g. 33001 samples / 33 s at 1000 Hz)
- **Passband ripple / stopband attenuation:** 0.0194 dB / 53 dB (properties of the Hamming window)
- **Software and version:** e.g. MNE-Python 1.x

## Where to find them

1. **The log output.** `raw.filter` prints all of this when it runs (with `verbose=True` or `mne.set_log_level('INFO')`). Rerunning on a copy is the easiest way to get the exact numbers for your sampling rate:
   ```python
   raw.copy().filter(0.1, 40, verbose=True)
   ```
   It will print the filter design block (windows, cutoffs, transition widths, filter length).

2. **`raw.info`.** `raw.info['highpass']` and `raw.info['lowpass']` store the cutoff frequencies but not the method, window, or transition bands.

3. **Reconstruct and inspect the filter directly:**
   ```python
   import mne
   h = mne.filter.create_filter(raw.get_data(), raw.info['sfreq'],
                                l_freq=0.1, h_freq=40)
   mne.viz.plot_filter(h, raw.info['sfreq'])
   ```
   This gives you the frequency response to confirm what you're describing (and a figure for supplementary material, if wanted).

A typical sentence would be: *"Data were filtered with a zero-phase, non-causal FIR filter (Hamming window, 0.1–40 Hz; −6 dB cutoffs; transition bandwidths 0.1 Hz and 10 Hz; filter length 33 s) using MNE-Python v1.x."*

If you do find that you set `iir_params` or `method='iir'` somewhere in your pipeline, tell me and I'll help sort out the Butterworth-specific parameters.

</details>

### Reply B

<details><summary>Show reply</summary>

The filter description you see in raw.plot() (e.g., a 16th-order Butterworth) is used strictly for real-time visualization inside the interactive plotting window to ensure smooth scrolling. It does not alter your underlying data array.

For your paper, you must report the parameters of the actual filter you applied to your data via raw.filter(0.1, 40), which uses an FIR (Finite Impulse Response) filter by default in MNE-Python, rather than the IIR Butterworth filter used by the plotter.

1. Which Parameters Should You Report?
Standard electrophysiology reporting guidelines (like COBIDAS for EEG/MEG) require the following details for your data filter:

Filter Type: Finite Impulse Response (FIR) filter.

Design Method: Windowed-sinc filter (MNE default: fir_design='firwin').

Window Type: Hamming window (fir_window='hamming', the MNE default).

Cutoff Frequencies: Pass-band edges at 0.1 Hz (high-pass) and 40 Hz (low-pass).

Transition Bandwidth: The lower and upper transition widths (automatically calculated by MNE based on your sampling rate and cutoff frequencies).

Filter Length: The total filter length (number of coefficients/taps).

Phase: Zero-phase (non-causal, symmetric, delay-compensated via phase='zero').

2. Where Do You Find These Parameters?
You can easily extract these exact values from two places:

The Python Console Logs: When you ran raw.filter(0.1, 40), MNE automatically printed a detailed breakdown to your console (logging output), including the exact filter length, transition bandwidths, and design parameters.

Programmatically: If you need to inspect or verify them without re-running the full script, you can generate the filter parameters using mne.filter.create_filter():

Python
import mne

# Pass your sampling rate (sfreq) and parameters
info = raw.info
filter_params = mne.filter.create_filter(
    data=None,
    sfreq=info['sfreq'],
    l_freq=0.1,
    h_freq=40
)
Example Methods Text for Your Paper
You can adapt a concise summary like this for your manuscript:

"Continuous data were band-pass filtered between 0.1 and 40 Hz using a finite impulse response (FIR) filter implemented in MNE-Python. The filter was designed using a windowed-sinc approach with a Hamming window (zero-phase, non-causal). [Optional: Insert transition bandwidths and filter length printed from your console log here]."

</details>

### Reply C

<details><summary>Show reply</summary>

The key distinction is that the 16th-order Butterworth shown by `raw.plot()` may not represent the actual filter order used in your filtering operation. You should report the parameters of the filter that was actually applied using `raw.filter(0.1, 40)`.

Assuming you are using MNE-Python, here's what you should report and where to find it.

## 1. Parameters to report in your paper

For your command:

```
raw.filter(0.1, 40)
```

You should report:

| Parameter             | What to report                                                          |
| --------------------- | ----------------------------------------------------------------------- |
| Filter type           | Butterworth (if configured as such; otherwise report the actual design) |
| Filter range          | 0.1–40 Hz                                                               |
| Filter direction      | Zero-phase (default in MNE for the usual IIR filtering configuration)   |
| Filter order          | Actual order used by the filter                                         |
| Filter implementation | IIR or FIR                                                              |
| Sampling frequency    | Your recording's sampling frequency                                     |
| Phase characteristics | Zero-phase, if applicable                                               |

Important: MNE-Python's default filtering method is FIR, not Butterworth. Therefore, `raw.filter(0.1, 40)` does not automatically mean that a Butterworth filter was applied.

## 2. Where to find the actual filter parameters

First, inspect your filtering command and the MNE output in your Python console.

For example:

```
raw.filter(0.1, 40)
```

MNE usually prints information about the filter design, including:

- Filter length
- Lower and upper passband edges
- Transition bandwidths
- Filter type (FIR/IIR)
- Window and design method

If you explicitly used an IIR Butterworth filter, you might have something like:

```
raw.filter(    0.1,    40,    method='iir',    iir_params=dict(order=4, ftype='butter'))
```

You can inspect the IIR filter settings using:

```
raw.filter(    0.1,    40,    method='iir',    iir_params=dict(order=4, ftype='butter'))
```

The actual filter order is then specified explicitly.

## 3. Why does `raw.plot()` show a 16th-order Butterworth?

This is an important detail.

The filter displayed in `raw.plot()` may be a visualization setting used for displaying the data rather than the filter previously applied to your actual recording.

In other words:

- `raw.filter()` applies a filter to the data.
- `raw.plot()` can display data using a separate visualization filter.

These should not be confused when reporting methods in a paper.

## 4. Example of how to write it in your paper

If you used MNE's default FIR filtering:

> The continuous EEG data were band-pass filtered between 0.1 and 40 Hz using a finite impulse response (FIR) filter implemented in MNE-Python.

If you actually used a Butterworth IIR filter:

> The continuous EEG data were band-pass filtered between 0.1 and 40 Hz using a Butterworth infinite impulse response (IIR) filter. The filter order and phase characteristics were [specify actual values].

## One thing I'd like to clarify

Could you share the output of:

```
raw.filter(0.1, 40)
```

Specifically, the messages printed in your Python console when filtering.

I can then help you identify the exact filter type, order, phase, and other parameters to report in your research paper, without accidentally reporting the 16th-order visualization filter as your actual preprocessing filter.

</details>

| Reply | PASS/FAIL | Reason |
|---|---|---|
| A | | |
| B | | |
| C | | |

---

## q021_cluster_adjacency_none: Adjacency in spatio-temporal cluster tests

**Prompt**

I run `mne.stats.spatio_temporal_cluster_1samp_test` on sensor-level data with shape
(n_subjects, n_times, n_channels) and leave `adjacency=None`. How are clusters
formed in that case, and is that OK?

**Criteria**

Pass if the answer explains that `None` assumes a regular lattice along the last axis
(each channel adjacent to the channels before and after it in array order), which is
not meaningful for sensors, and that a real channel adjacency should be built
(e.g. `mne.channels.find_ch_adjacency`).

### Reply A

<details><summary>Show reply</summary>

With `adjacency=None`, MNE treats the spatial dimension as **fully connected**: every channel is considered a neighbor of every other channel. Temporal adjacency is still handled as usual (adjacent time points connect).

**How clusters form**

- A cluster is a set of supra-threshold (time, channel) points connected through time and/or space.
- With full spatial connectivity, any two supra-threshold points that are at *adjacent time samples* are connected, regardless of which channels they're on. So a supra-threshold point at channel Fz at time t and one at Oz at time t+1 are part of the same cluster. Points at the same time on different channels are also connected, so all supra-threshold channels at a given time sample merge into one blob.
- In practice, clusters become essentially "time segments": runs of consecutive samples where *any* channel exceeds threshold get glued together, and clusters are extended across the whole scalp.

**Is that OK?**

Usually no, for sensor-level EEG/MEG data, for a few reasons:

1. **It violates the logic of the method.** Cluster-based inference assumes effects that are spatially contiguous. Ignoring the sensor layout throws away that assumption, so the cluster mass no longer reflects a spatially coherent effect.
2. **Sensitivity drops for focal effects.** Unrelated, scattered supra-threshold points get merged into one big cluster, which makes the cluster statistic dominated by noise-driven points and diffuses the distribution of the max cluster statistic under the null. Real, focal effects can be harder to detect.
3. **The spatial interpretation is meaningless.** A significant cluster tells you almost nothing about *where* the effect is, since you'd be claiming a "cluster" that spans non-neighboring sensors.
4. **It's an odd null/alternative combination.** You've effectively built a test closer to a temporal-only cluster test on the union of channels, but without declaring that intention.

It's defensible only if you deliberately want that (e.g., a pure time-course test where channel identity is irrelevant, or a single-channel / ROI-averaged analysis, in which case you'd just use a 1D temporal test).

**What to do instead**

Provide a sensor adjacency matrix:

```python
from mne.channels import find_ch_adjacency

adjacency, ch_names = find_ch_adjacency(epochs.info, ch_type="eeg")  # or "mag"/"grad"
# make sure the data's channel order matches ch_names

T_obs, clusters, p_values, H0 = mne.stats.spatio_temporal_cluster_1samp_test(
    X,  # (n_subjects, n_times, n_channels)
    adjacency=adjacency,
    n_permutations=1000,
    threshold=None,      # or an explicit t/F threshold
    tail=0,
)
```

Notes:

- `find_ch_adjacency` uses a Delaunay triangulation of the sensor positions, which is reasonable for most setups. You can also use a distance-based or custom matrix (e.g. `mne.channels.read_ch_adjacency` for built-in layouts such as `"neuromag306mag"`).
- For Neuromag data, handle magnetometers and gradiometers separately (different `ch_type`), since they have different units and scale.
- Make sure the channel dimension of `X` matches the adjacency matrix order, and that the data layout really is `(n_subjects, n_times, n_channels)` (the function expects times then space).
- Remember that the cluster-based test supports the claim that *there is an effect*, not that it's located precisely at the extent of the cluster.

</details>

### Reply B

<details><summary>Show reply</summary>

When you set `adjacency=None` in `mne.stats.spatio_temporal_cluster_1samp_test`, MNE assumes that all channels are spatially connected to one another. It does not use the physical sensor layout to determine neighboring channels.

For your data shape:

```
(n_subjects, n_times, n_channels)
```

the clustering is performed over the time × channel dimensions, with the subject dimension used for the one-sample statistical test.

This is an important distinction: `adjacency=None` does not mean that channels are ignored or that clustering happens independently at each channel.

## 1. Exactly how are clusters formed?

With `adjacency=None`, MNE uses a regular lattice (grid) adjacency.

For your 2D data dimensions (time, channels), the neighborhood relationships are:

- Temporal adjacency: immediately neighboring time samples are connected.
- Spatial adjacency: immediately neighboring channel indices are connected.

Consequently, two supra-threshold samples can belong to the same cluster if they are connected through neighboring time samples, neighboring channel indices, or a combination of both.

For example, suppose you have four channels ordered as:

```
channels = ['Fz', 'Cz', 'Pz', 'Oz']
```

MNE effectively treats their spatial arrangement as:

```
Fz — Cz — Pz — Oz
```

This is a one-dimensional chain, not the actual geometry of the EEG/MEG sensor array.

Importantly, MNE does not know that Fz and Cz are physically close, or that Cz and Pz are physically close. It simply uses the channel ordering.

This behavior is documented in the [`adjacency` parameter documentation](https://mne.tools/stable/generated/mne.stats.spatio_temporal_cluster_1samp_test.html).
## 2. Is this OK?

Generally, I would not recommend it for sensor-level EEG or MEG data.

The problem is that your cluster definition depends on the ordering of channels in your input array.

For example, if your channels are ordered alphabetically, two physically distant sensors might become neighbors, while two physically adjacent sensors might not be connected.

This has implications for:

- Which significant samples are grouped into clusters.
- The spatial extent of detected clusters.
- The cluster-level permutation statistics and resulting p-values.

The permutation procedure does not automatically correct an inappropriate adjacency structure. The adjacency structure is part of the statistical hypothesis being tested.

## 3. What should you use instead?

For sensor-level data, I recommend constructing adjacency from the actual sensor positions using `mne.channels.find_ch_adjacency()`.

For EEG:

```
import mneadjacency, ch_names = mne.channels.find_ch_adjacency(    info,    ch_type="eeg")
```

Then run:

```
T_obs, clusters, cluster_p_values, H0 = (    mne.stats.spatio_temporal_cluster_1samp_test(        X,        adjacency=adjacency,        n_permutations=1000,        threshold=None,        tail=0,        n_jobs=-1,        seed=42    ))
```

Here:

- `adjacency` specifies which EEG sensors are spatial neighbors.
- `max_step=1` (the default) specifies that immediately neighboring time samples can be connected.
- Clusters are formed using both spatial and temporal connectivity.

You should ensure that the channel ordering in `X` matches the ordering in `info` and the returned `ch_names`. Also ensure that your `info` contains an appropriate sensor montage.

For MEG, use the appropriate channel type (`"mag"` or `"grad"`).

See MNE's [sensor adjacency documentation](https://mne.tools/stable/generated/mne.channels.find_ch_adjacency.html) and [spatiotemporal clustering tutorial](https://mne.tools/stable/auto_tutorials/stats-source-space/20_cluster_1samp_spatiotemporal.html).
## 4. One important distinction

There are three different adjacency choices worth distinguishing:

| Setting                      | Spatial connectivity        | Temporal connectivity         |
| ---------------------------- | --------------------------- | ----------------------------- |
| `adjacency=None`             | Consecutive channel indices | Yes                           |
| `adjacency=False`            | No spatial connectivity     | No spatial clustering         |
| `adjacency=adjacency_matrix` | Actual sensor neighbors     | Yes, controlled by `max_step` |

For your application, the third option is generally the most appropriate.

My recommendation: Use `find_ch_adjacency()` for EEG/MEG sensor-level cluster permutation tests rather than relying on `adjacency=None`. This makes your spatial cluster definition reflect the actual sensor geometry rather than an arbitrary ordering of channels.

</details>

### Reply C

<details><summary>Show reply</summary>

Leaving `adjacency=None` when running `mne.stats.spatio_temporal_cluster_1samp_test` on sensor-level data is **not OK** and will lead to invalid spatial clustering.

---

### How Clusters Are Formed When `adjacency=None`

According to MNE-Python's documentation, if `adjacency=None`, the function assumes a **regular lattice adjacency** along the dimensions of your data array.

* **Time dimension:** Time points are correctly linked to their immediate temporal neighbors ($t - 1$ and $t + 1$).
* **Channel dimension:** Each channel at index $i$ is treated as a neighbor only to channels at index $i - 1$ and $i + 1$ based strictly on **their sequence in your NumPy array**, rather than their physical layout on the scalp.

### Why This Is Problematic for Sensor Data

In standard MNE datasets, channels are ordered alphabetically, numerically, or arbitrarily by the acquisition system (e.g., `'A1'`, `'A2'`, etc., or sorted channel names).

* An alphabetical or arbitrary index order **does not map to physical space**.
* Channel index `5` might be adjacent to channel index `6` in your array, but physically located on opposite sides of the head.
* Consequently, MNE will group physically unrelated electrodes into the same spatial clusters, completely breaking the assumption of spatial contiguity required for cluster-based permutation tests.

---

### How to Fix It

You must explicitly compute a spatial adjacency matrix using `mne.channels.find_ch_adjacency()` based on your channel layout and pass it to the `adjacency` parameter.

Here is how you properly set it up:

```python
from mne.channels import find_ch_adjacency
from mne.stats import spatio_temporal_cluster_1samp_test

# 1. Compute spatial adjacency for your sensor type (e.g., 'eeg' or 'mag'/'grad')
spatial_adjacency, ch_names = find_ch_adjacency(info, ch_type='eeg')

# 2. Run the test with the proper adjacency matrix
# Note: When passing a 2D spatial adjacency matrix (n_channels, n_channels),
# MNE automatically handles time connectivity using the max_step parameter (default max_step=1).
T_obs, clusters, cluster_pv, H0 = spatio_temporal_cluster_1samp_test(
    X,
    threshold=threshold,
    n_permutations=1024,
    adjacency=spatial_adjacency,
    tail=0
)

```

</details>

| Reply | PASS/FAIL | Reason |
|---|---|---|
| A | | |
| B | | |
| C | | |

---

## q022_source_psd_units: Units of source-space PSD

**Prompt**

I computed source-space power spectra with `mne.minimum_norm.compute_source_psd_epochs`
using dSPM. What units should I put on the y-axis?

**Criteria**

Pass if the answer says dSPM values are noise-normalized and therefore unitless,
whereas method="MNE" gives current-density power (e.g. Am²/Hz or nAm²/Hz). Fail if
it gives a physical unit for dSPM.

### Reply A

<details><summary>Show reply</summary>

If you computed the PSD using `method='dSPM'`, the y-axis should generally be labelled:

dSPM²/Hz (or (noise-normalized units)²/Hz).

It should not be labelled `A²/Hz`, `(nAm)²/Hz`, or `(V/m)²/Hz`, because dSPM estimates are noise-normalized rather than expressed in physical source-current units.

A small but important distinction: dSPM is a noise-normalized, dimensionless estimate. Therefore, its PSD has units of dimensionless²/Hz, conventionally written as `1/Hz`.

For a publication, I would use:

- Y-axis: `dSPM²/Hz`
- X-axis: `Frequency (Hz)`

The MNE discussion explicitly confirms that dSPM source estimates are unitless, and that their derived power quantities do not inherit physical units.
Also, `compute_source_psd_epochs()` does not automatically convert the output to dB. You are working with linear PSD values, not log power.
My recommendation: Label it `dSPM²/Hz` for clarity, rather than simply `Power (a.u.)`.

</details>

### Reply B

<details><summary>Show reply</summary>

With dSPM there are no physical units. dSPM is noise-normalized (a z-like statistic, estimated source amplitude divided by its expected noise standard deviation), so the source time courses are dimensionless. The PSD is the squared amplitude per unit frequency, so the y-axis is:

**dSPM² / Hz**, or equivalently **1/Hz** (arbitrary units)

A label like `"Power (dSPM² / Hz, a.u.)"` is clear and accurate.

- **It is not a physical power.** Unlike `method="MNE"`, where the result would be (A·m)² / Hz, the values here are in noise-normalized units. They depend on your noise covariance estimate and regularization, so absolute values aren't comparable across subjects or datasets with different noise covariances. Comparing relative differences (conditions, frequency bands, regions) within the same inverse operator is fine.
- **Check the normalization in your MNE version.** The function returns a one-sided density in units²/Hz, but the exact scaling can vary slightly between versions, so skim the docstring and source if you need to be rigorous.
- **If you need physical units**, rerun with `method="MNE"` (or `"sLORETA"`/`"eLORETA"`, which are also unitless, so use plain MNE for this).
- **For plotting**, a log y-axis or 10·log10 (dB) is common. If you convert to dB, the label becomes "dB re 1 dSPM²/Hz" or simply "Power (dB)" with a note that it's relative.

</details>

### Reply C

<details><summary>Show reply</summary>

When you compute source-space power spectra using `mne.minimum_norm.compute_source_psd_epochs` with **dSPM** (Dynamic Statistical Parametric Mapping), the units on the y-axis are **$(\text{dSPM})^2/\text{Hz}$** (often expressed simply as **dimensionless power per Hz**, **$\text{dSPM}^2 / \text{Hz}$**, or **arbitrary units (a.u.)**).

### Why these units?

1. **Standard MNE (`method='MNE'`):** If you use the standard linear inverse operator, the source estimates represent current dipole moments. For MEG, these are typically in **Ampere-meters ($\text{Am}$)**, meaning the resulting PSD units would be $\text{Am}^2/\text{Hz}$.
2. **dSPM (`method='dSPM'`):** dSPM normalizes the minimum-norm estimate at each vertex by dividing it by the estimated noise standard deviation (derived from the noise covariance matrix). Because you divide an amplitude by its noise standard deviation, the resulting dSPM values are **dimensionless** (similar to a $Z$-score or a noise-normalized statistical map).
3. **Power Spectral Density:** Taking the PSD of a dimensionless, noise-normalized time series squares those values and divides by frequency resolution, yielding **$(\text{dSPM})^2/\text{Hz}$**.

### How to label your plot:

* **Precise label:** $(\text{dSPM})^2/\text{Hz}$
* **General/Publication-friendly label:** **Power ($\text{dSPM}^2/\text{Hz}$)** or **Power (arbitrary units)**.

Because dSPM values are unitless noise-normalized metrics, reviewers and readers do not expect strict physical units (like $\text{Am}^2/\text{Hz}$) on the y-axis, making $(\text{dSPM})^2/\text{Hz}$ or arbitrary units standard practice.

</details>

| Reply | PASS/FAIL | Reason |
|---|---|---|
| A | | |
| B | | |
| C | | |

---

## q023_psd_epoch_length: Why the PSD changes with epoch length

**Prompt**

I computed the power spectrum of the same resting-state EEG once from 2-second epochs
and once from 10-second epochs (and once from the continuous data). The spectra
differ, especially at low frequencies. Is something wrong?

**Criteria**

Pass if the answer explains that frequency resolution is about 1 / window length, so
short epochs give poor low-frequency estimates, and that MNE uses different default
estimators for raw (Welch) and epochs (multitaper), which also changes the result.

### Reply A

<details><summary>Show reply</summary>

No, **nothing is wrong with your code or your data!** Finding that power spectra differ across different epoch lengths—especially at low frequencies—is a classic, well-understood phenomenon in EEG signal processing.

This difference arises from fundamental mathematical properties of Fourier analysis, windowing, and the nature of EEG signals. Here is why your 2-second, 10-second, and continuous spectra look different, and why low frequencies are affected the most.

---

### 1. Frequency Resolution ($\Delta f = 1/T$)

The frequency resolution of a Fourier-based power spectrum (or FFT/Welch's method) is strictly determined by the duration of the analysis window ($T$):


$$\Delta f = \frac{1}{T}$$

* **2-second epochs ($T = 2\text{ s}$):** Your frequency resolution is $1 / 2 = 0.5\text{ Hz}$. Your lowest non-zero frequency bin is $0.5\text{ Hz}$, meaning you cannot resolve anything below that, and bins are spaced widely apart.
* **10-second epochs ($T = 10\text{ s}$):** Your frequency resolution is $1 / 10 = 0.1\text{ Hz}$. You get five times more data points in the low-frequency range ($0.1\text{ Hz}, 0.2\text{ Hz}, 0.3\text{ Hz}\dots$), allowing you to accurately capture slow waves, delta rhythms, and slow drifts.

Because the bin centers and widths are completely different, the power mapped into those bins will naturally look dissimilar, especially where the spectrum changes rapidly (which is heavily concentrated at low frequencies).

### 2. Spectral Leakage and Windowing

When you chop continuous data into short epochs (like 2 seconds), you apply a window function (e.g., Hann, Hamming) to prevent spectral leakage.

* Shorter windows have **wider main spectral lobes** in the frequency domain.
* This means power from higher frequencies or broader spectral shapes "bleeds" into neighboring bins. At low frequencies (like the delta band, $1–4\text{ Hz}$), a wide main lobe can heavily distort the estimated power because the bin width is a significant fraction of the frequency itself.

### 3. Slow Drifts, Artifacts, and Edge Effects

EEG signals are notoriously non-stationary and contain high-amplitude, very slow fluctuations (sweat artifacts, movement, electrode drifts, or slow cortical potentials well below $0.5\text{ Hz}$).

* **Continuous data / Long epochs:** Capture these slow trends smoothly as part of the low-frequency continuum.
* **Short epochs (2 seconds):** Chopping the data abruptly creates artificial "edges" in every epoch. Even with windowing, sudden truncation of slow waves introduces high-energy transient artifacts (spectral leakage from sharp boundaries) that disproportionately inflate or distort power in the lowest frequency bins.

### 4. Welch's Method and Variance vs. Resolution

If you used Welch's method to estimate the PSD:

* **2-second epochs** give you many more overlapping segments, resulting in a smoother estimate with **lower variance**, but poor frequency resolution.
* **10-second epochs** give you fewer segments (higher variance if total recording time is constant), but high frequency resolution.

---

### What should you do?

* **If you care about low frequencies (Delta, Theta, or slow oscillations):** Stick to longer epochs (e.g., 4 to 10 seconds or longer) or analyze the continuous data (with proper high-pass filtering beforehand, e.g., $0.5\text{ Hz}$ high-pass) to avoid edge distortion.
* **If you care about higher frequencies (Alpha, Beta, Gamma):** 2-second epochs are often used because they provide enough stationary chunks for reliable averaging, and higher frequencies are far enough from $0\text{ Hz}$ that epoch-length resolution limits matter less.
* **Best Practice:** Always apply an appropriate high-pass filter (e.g., $0.1$ or $0.5\text{ Hz}$) *before* epoching to remove slow drifts that cause low-frequency distortion in short windows.

</details>

### Reply B

<details><summary>Show reply</summary>

Nothing is necessarily wrong. Differences like this are expected, and they come mostly from how epoch length sets the frequency resolution and the bias/variance trade-off of the estimate.

**1. Frequency resolution**
Resolution is 1/T: 0.5 Hz for 2 s epochs, 0.1 Hz for 10 s epochs, and finer still for continuous data. With 2 s epochs, the lowest nonzero frequency bin is 0.5 Hz, and delta (1-4 Hz) has only a handful of bins. Any structure narrower than the resolution gets smeared. A 10 Hz alpha peak, for example, looks broader and lower in the 2 s spectrum than in the 10 s one.

**2. Spectral leakage and windowing**
Each epoch is multiplied by a taper (typically Hann). Power from strong low-frequency content, especially slow drifts and the 1/f background, leaks into neighboring bins. Short epochs have fewer cycles of slow activity, so this leakage is proportionally worse at low frequencies. A 2 s window barely contains one cycle of a 0.5-1 Hz component, so the estimate there is poor and often biased upward.

**3. Variance (averaging)**
Welch-style estimates average over epochs. Many 2 s epochs give a smoother spectrum per frequency bin; fewer 10 s epochs give a noisier one but with sharper detail. With continuous data and a single long periodogram, you get maximum resolution but a very noisy estimate unless you segment and average (Welch) or use multitaper.

**4. Low-frequency artifacts and detrending**
Slow drifts, electrode/sweat artifacts, and DC offsets matter more in short epochs. If you detrend or demean each epoch, you remove different amounts of low-frequency power depending on epoch length. High-pass filtering in preprocessing, and its cutoff relative to the epoch length, also interacts with this. Epoch rejection also changes things: longer epochs are more likely to contain an artifact and get dropped, so you may be averaging different subsets of data.

**5. Normalization and units**
Check that all three are computed as PSD (µV²/Hz) with the same scaling. Raw FFT amplitude or power not normalized by window length and sampling rate will differ by construction. Also confirm whether you compare linear or log power: log-scaled spectra exaggerate low-power differences.

**What to check**
- Are the differences mostly below ~2-4 Hz? That points to leakage, detrending, and drift, which is the expected pattern.
- Do the spectra agree at mid-range frequencies (e.g., 8-30 Hz) after accounting for smoothness? If so, the pipeline is probably fine.
- Are the same data being used? Compare the amount of retained data per method.
- Are the same window, overlap, and detrending settings applied in all three?

**Recommendations**
- For a fair comparison, use Welch with the same window length and overlap, or multitaper with matched frequency smoothing.
- If you care about low frequencies, use epochs of at least several seconds, with a high-pass filter well below your lowest frequency of interest.
- Report the epoch length, taper, overlap, and detrending with your results, since the choice affects values, especially below 4 Hz.

If you share your toolbox (MNE, EEGLAB, FieldTrip), the exact function calls, and what the difference looks like (a shifted offset, a different slope, or a different peak shape), I can help pin down which of these effects is dominant.

</details>

### Reply C

<details><summary>Show reply</summary>

No — this is not necessarily a mistake. In fact, it is quite normal for power spectra computed from 2-second epochs, 10-second epochs, and continuous EEG to differ, particularly at low frequencies.

The main reason is that the length of the data segment used for spectral estimation affects the frequency resolution and the stability of the power spectral density (PSD) estimate.

There are several important reasons for this.

## 1. Frequency resolution depends on epoch duration

The fundamental frequency resolution of a Fourier-based spectral estimate is:

\\[ \Delta f = \frac{1}{T} \\]

where \\(T\\) is the duration of the analyzed segment.

For your three conditions:

| Data segment                  | Frequency resolution |
| ----------------------------- | -------------------- |
| 2-second epochs               | 0.5 Hz               |
| 10-second epochs              | 0.1 Hz               |
| Continuous data (e.g., 5 min) | 0.0033 Hz            |

This has an important consequence, especially for delta and theta activity.

For example, a 2-second epoch has relatively poor resolution for distinguishing activity at 0.5 Hz, 1 Hz, and 1.5 Hz. A 10-second epoch can distinguish these frequencies much better.

Therefore, low-frequency spectral estimates are generally more sensitive to epoch duration.

## 2. Low frequencies need longer observation periods

Low-frequency oscillations have long periods:

| Frequency | Duration of one cycle |
| --------- | --------------------- |
| 0.5 Hz    | 2 seconds             |
| 1 Hz      | 1 second              |
| 2 Hz      | 0.5 seconds           |
| 4 Hz      | 0.25 seconds          |
| 8 Hz      | 0.125 seconds         |
| 10 Hz     | 0.1 seconds           |

Consider 0.5 Hz activity. A 2-second epoch contains only one complete cycle. That is generally insufficient for a reliable estimate of its spectral power.

A 10-second epoch contains five cycles, allowing a more stable estimate.

This is particularly relevant when studying:

- Delta activity (0.5–4 Hz).
- Very slow oscillations.
- Slow-wave activity.
- Low-frequency changes associated with sleep or drowsiness.

Consequently, you may see substantial differences in delta power between 2-second and 10-second epochs.

## 3. Spectral leakage and windowing

Another important factor is spectral leakage.

When you analyze a finite EEG segment, you effectively cut the signal at its boundaries. If the signal does not begin and end at similar amplitudes and phases, this discontinuity can spread spectral energy into neighboring frequencies.

This is called spectral leakage.

[Time and Frequency Domain Analysis of IMU-Based Orientation Estimation Algorithms with Comparison to Robotic Arm Orientation as Reference](image removed)

[mdpi.com](https://www.mdpi.com/1424-8220/25/16/5161)

Shorter epochs can be particularly sensitive to this problem because:

- Boundary effects constitute a larger proportion of the analyzed signal.
- Slow oscillations may not complete an integer number of cycles.
- Energy from strong frequencies can spread into neighboring frequency bins.

Applying a Hann (Hanning) window before calculating the FFT can reduce spectral leakage, although it does not eliminate all spectral estimation problems.

## 4. Why continuous EEG can give a different spectrum

The continuous EEG spectrum is not necessarily equivalent to the average of the spectra obtained from shorter epochs.

Several factors contribute:

A. Nonstationarity

Resting-state EEG changes over time. For example, a participant may become drowsy, blink, move, or change their level of alertness.

A continuous spectrum combines these different periods.

B. Artifact contamination

Slow electrode drift, movement artifacts, sweating, and eye movements can introduce substantial low-frequency power.

If the continuous recording contains these artifacts, its delta power may be higher than the power calculated from artifact-free epochs.

C. Detrending and filtering

The way you remove the DC component, linear trends, and slow drifts can substantially influence the low-frequency spectrum.

D. Averaging

If you calculate a PSD for each epoch and then average the PSDs, you obtain an estimate that differs in statistical properties from calculating the PSD of the entire continuous recording.

Importantly, averaging multiple short-epoch PSD estimates can reduce variance, but it does not restore the frequency resolution lost through short epochs.

## 5. What should you expect in your results?

As a general expectation:

| Frequency range  | Expected sensitivity to epoch length                  |
| ---------------- | ----------------------------------------------------- |
| Delta (0.5–4 Hz) | High                                                  |
| Theta (4–8 Hz)   | Moderate                                              |
| Alpha (8–13 Hz)  | Lower                                                 |
| Beta (13–30 Hz)  | Relatively low                                        |
| Gamma (30+ Hz)   | Generally lower, depending on sampling and processing |

These are general expectations, not guaranteed outcomes. Artifact contamination, windowing, and signal characteristics can change the pattern.

You might therefore observe that:

- Delta power differs considerably between 2-second and 10-second epochs.
- Alpha power is relatively similar.
- Beta power is also relatively similar.

This would not automatically indicate an error in your analysis.

## 6. How I would recommend comparing the three methods

If your goal is to determine whether epoch duration affects your resting-state EEG results, I would recommend the following approach.

1. Use the same preprocessing for all three datasets, including filtering, referencing, and artifact rejection.
2. Use the same spectral estimation method (e.g., Welch's method).
3. Use the same windowing function.
4. Keep the sampling frequency identical.
5. Make sure PSD normalization is identical (e.g., power per Hz).
6. Compare integrated band power rather than relying only on individual frequency-bin values.

One particularly important point: If you use Welch's method, specify the window length explicitly. Using 2-second epochs with 2-second Welch windows is not equivalent to using 10-second epochs with 10-second Welch windows.

Also, zero-padding an FFT can produce more closely spaced frequency bins, but it does not improve the actual frequency resolution.

## 7. An important distinction for your analysis

There are two different comparisons you could make:

- Comparison A: Calculate PSD using 2-second epochs versus 10-second epochs, allowing the spectral window length to change. This tests the effect of spectral estimation duration.
- Comparison B: Use the same 2-second Welch window for both datasets, but average the resulting PSD estimates over different amounts of data. This tests the effect of the amount of data used for averaging.

These answer different scientific questions.

If you want to investigate whether the epoch duration itself influences your results, I would perform both comparisons.

## 8. Three questions that would help me interpret your results

I would like to know three details about your analysis:

1\. Which method did you use to calculate the power spectrum?

Welch's method

FFT (Fourier transform)

Multitaper method

Other / not sure

2\. What was your EEG sampling frequency?

128 Hz

250 Hz

256 Hz

500 Hz

1000 Hz

Other

3\. Where did you observe the largest differences?

Mainly delta (0.5–4 Hz)

Delta and theta (0.5–8 Hz)

Across almost all frequencies

Mainly alpha and beta

Submit answers

With these details, I can help you determine whether your differences are expected consequences of spectral estimation or whether there might be an issue with your EEG processing pipeline.

</details>

| Reply | PASS/FAIL | Reason |
|---|---|---|
| A | | |
| B | | |
| C | | |

---
