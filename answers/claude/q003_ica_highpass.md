Here's a standard setup. The key point is that ICA fits poorly on unfiltered data (slow drifts dominate the variance), so the usual approach is to fit on a high-pass filtered *copy* and then apply the result to your original `raw`.

```python
import mne
from mne.preprocessing import ICA

# Fit ICA on a copy high-pass filtered at 1 Hz; leave the original raw untouched
raw_for_ica = raw.copy().load_data().filter(l_freq=1.0, h_freq=None)

ica = ICA(
    n_components=10,
    method="fastica",      # or "picard" if you have python-picard installed
    max_iter="auto",
    random_state=97,       # reproducible results
)
ica.fit(raw_for_ica)
```

**Notes:**

- **Why filter a copy?** A 1 Hz high-pass removes drift that would otherwise bias the decomposition. Because ICA is a linear unmixing, the fitted `ica` can later be applied to your original unfiltered `raw` (or one with different filter settings) via `ica.apply(raw)`.
- **Bad channels:** If you've marked any in `raw.info["bads"]`, they're excluded by default (`picks=None` selects good data channels). Interpolate or drop them before fitting if needed.
- **Very noisy segments:** If there are large non-blink artifacts (e.g., muscle bursts or electrode pops), consider annotating them as `BAD_` first. ICA's `reject_by_annotation=True` default will then skip them.
- **Later, to find blink components:**

```python
eog_idx, scores = ica.find_bads_eog(raw_for_ica)  # if you have an EOG channel
# or, without an EOG channel, use a frontal channel such as Fp1:
# eog_idx, scores = ica.find_bads_eog(raw_for_ica, ch_name="Fp1")
ica.exclude = eog_idx
raw_clean = ica.apply(raw.copy().load_data())
```

With only 10 components, you may want to check that your channel count is at least 10 (the number of components can't exceed the number of channels, or the data rank after average referencing).
