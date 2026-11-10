raw_resampled, events_resampled = raw.copy().resample(250, events=events)

epochs = mne.Epochs(
    raw_resampled,
    events_resampled,
    tmin=-0.2,
    tmax=0.5,
    baseline=(None, 0),
    preload=True,
)
