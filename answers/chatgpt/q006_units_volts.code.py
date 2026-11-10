import mne
import numpy as np
# Convert microvolts to volts
data_volts = data * 1e-6
# Create channel information
info = mne.create_info(    ch_names=ch_names,    sfreq=sfreq,    ch_types='eeg')
# Create MNE Epochs object
epochs = mne.EpochsArray(    data_volts,    info,    tmin=0,    baseline=None)
