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
