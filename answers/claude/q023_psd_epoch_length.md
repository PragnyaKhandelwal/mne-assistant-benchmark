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
