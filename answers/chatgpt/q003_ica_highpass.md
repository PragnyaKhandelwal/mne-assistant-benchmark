For ICA-based blink removal, do not fit ICA directly on the unfiltered data. MNE recommends high-pass filtering at 1 Hz before fitting ICA because slow drifts can reduce ICA performance.

Keep your original `raw` unchanged and fit ICA on a filtered copy:

```
import mnefrom mne.preprocessing import ICA# Create a filtered copy for ICA fittingraw_ica = raw.copy().filter(l_freq=1.0, h_freq=None)# Initialize ICA with 10 componentsica = ICA(    n_components=10,    random_state=42,    max_iter='auto')# Fit ICAica.fit(raw_ica)
```

Your fitted ICA object is now stored in `ica`.

Important:

- `raw` remains unfiltered and unchanged.
- `raw_ica` is used only for ICA fitting.
- `ica` stores the fitted decomposition.
- You can subsequently identify blink-related components using `ica.find_bads_eog()` (if you have EOG channels) or by inspecting component topographies.

Later, after identifying blink components, you can apply the ICA solution to the original unfiltered data:

```
ica.exclude = [0]  # Replace with identified blink component indicesica.apply(raw)
```

This way, you retain the original EEG frequency content while removing blink artifacts.

Reference: [MNE-Python: Repairing artifacts with ICA](https://mne.tools/stable/auto_tutorials/preprocessing/40_artifact_correction_ica.html?utm_source=chatgpt.com).
