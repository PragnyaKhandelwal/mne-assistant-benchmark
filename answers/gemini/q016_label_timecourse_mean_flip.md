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
