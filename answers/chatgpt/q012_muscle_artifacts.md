If you're using MNE-Python, a good approach is to detect muscle artifacts using the EEG signal's high-frequency activity, annotate the detected bursts as bad segments, and then create epochs with automatic rejection.

You can use `annotate_muscle_zscore()` for this. It detects muscle activity based on elevated z-scored high-frequency power.

```
import mnefrom mne.preprocessing import annotate_muscle_zscore# Detect muscle artifactsannotations, scores = annotate_muscle_zscore(    raw,    ch_type="eeg",    threshold=4,    min_length_good=0.1,    filter_freq=(110, 140))# Add muscle annotations to the raw dataraw.set_annotations(raw.annotations + annotations)# Create epochs around all events, rejecting epochs overlapping muscle artifactsepochs = mne.Epochs(    raw,    events,    event_id=None,    tmin=-0.2,    tmax=0.5,    baseline=None,    reject_by_annotation=True,    preload=True)
```

How it works:

- `annotate_muscle_zscore()` detects short bursts of high-frequency muscle activity.
- `threshold=4` controls detection sensitivity. Lower values detect more bursts; higher values are more conservative.
- `filter_freq=(110, 140)` targets high-frequency muscle activity.
- The annotations mark detected muscle segments as bad.
- `reject_by_annotation=True` automatically drops any epoch that overlaps a bad segment.

Check the results:

```
# View detected muscle artifactsraw.plot()# Inspect retained and rejected epochsprint(epochs)print("Dropped epochs:", len(epochs.drop_log) - len(epochs))
```

Important: Make sure your sampling frequency is sufficiently high for the 110–140 Hz detection band (at least 280 Hz, preferably higher). Also inspect the annotations visually and adjust the threshold if necessary.

The resulting `epochs` contains only epochs from -0.2 to 0.5 seconds around events that do not overlap detected muscle artifacts.
