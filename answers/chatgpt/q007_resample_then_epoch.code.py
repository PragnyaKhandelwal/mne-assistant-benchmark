# 1. Low-pass filter continuous data to prevent aliasing
raw_filt = raw.copy()
raw_filt.filter(    l_freq=None,    h_freq=80.0,    picks='eeg')
# 2. Create epochs and decimate by a factor of 4
epochs = mne.Epochs(    raw_filt,    events,    event_id=None,    tmin=-0.2,    tmax=0.5,    baseline=None,    preload=True,    decim=4)
