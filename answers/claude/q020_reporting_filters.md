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
