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
