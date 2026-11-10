import mne

data_volts = data * 1e-6

info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types="eeg")

epochs = mne.EpochsArray(data_volts, info, tmin=-0.2)
