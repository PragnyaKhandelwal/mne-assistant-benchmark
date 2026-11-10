Here is the Python code to initialize and fit an ICA object with 10 components on your MNE-Python `raw` object and store it in a variable called `ica`:

```python
import mne
from mne.preprocessing import ICA

# Initialize ICA with 10 components
ica = ICA(n_components=10, random_state=97, max_iter='auto')

# Fit ICA to the raw data
ica.fit(raw)

```

### Important Best Practice

Since you mentioned the EEG is unfiltered, **it is strongly recommended to apply a high-pass filter (typically 1 Hz)** before fitting ICA. Slow drifts and low-frequency artifacts can degrade ICA performance and make it difficult to reliably isolate eye blinks.

If you want to filter your data first (saving the unfiltered data for later analysis), you can do:

```python
# Create a filtered copy just for fitting ICA
raw_filtered = raw.copy().filter(l_freq=1.0, h_freq=None, n_jobs=None)

# Fit ICA on the filtered data
ica = ICA(n_components=10, random_state=97, max_iter='auto')
ica.fit(raw_filtered)

```
