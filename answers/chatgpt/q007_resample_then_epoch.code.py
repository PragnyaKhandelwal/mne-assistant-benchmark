# Downsample from 1000 Hz to 250 Hz
raw.resample(250)
# Create epochs around all events (-0.2 to 0.5 seconds)
epochs = mne.Epochs(    raw,    events,    event_id=None,    tmin=-0.2,    tmax=0.5,    baseline=None,    preload=True)

raw.resample(250, events=events)

raw, events = raw.resample(250, events=events)
