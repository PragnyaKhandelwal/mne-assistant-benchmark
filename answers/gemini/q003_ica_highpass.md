To fit ICA reliably on continuous, unfiltered EEG, high-pass filter a **copy** of your data at 1.0 Hz first. ICA is extremely sensitive to low-frequency drifts; filtering a copy improves component separation without altering the original `raw` signal.

```python
import mne
from mne.preprocessing import ICA

# 1. High-pass filter a copy of raw at 1 Hz to remove low-frequency drifts
raw_ica = raw.copy().filter(l_freq=1.0, h_freq=None)

# 2. Initialize ICA with 10 components
ica = ICA(n_components=10, max_iter="auto", random_state=97)

# 3. Fit ICA on the filtered copy (stores fitted ICA in `ica`)
ica.fit(raw_ica)

```

### Why filter a copy first?

* **Drifts degrade decomposition:** Unfiltered slow fluctuations (drifts below 1 Hz) dominate the signal's variance, causing ICA to waste components on drift artifacts rather than cleanly isolating eye blinks.
* **Preserving low frequencies:** Fitting on `raw_ica` isolates the spatial unmixing matrix. When you are ready to remove blinks later, you run `ica.apply(raw)` on your original `raw` object, applying the learned spatial filters to your full-spectrum data without losing lower frequencies.
