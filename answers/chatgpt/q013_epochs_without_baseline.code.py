epochs = mne.Epochs(    raw,    events,    tmin=-0.2,    tmax=0.5,    baseline=None)
data = epochs.get_data()
