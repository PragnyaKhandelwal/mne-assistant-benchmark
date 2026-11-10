import numpy as np
import mne
# Convert microvolts to volts
data_volts = data * 1e-6
# Create channel information
info = mne.create_info(    ch_names=ch_names,    sfreq=sfreq,    ch_types=['eeg'] * len(ch_names))
# Set electrode montage (optional but recommended)
info.set_montage('standard_1020')
# Create events array
n_epochs = data.shape[0]
events = np.column_stack([    np.arange(n_epochs),    np.zeros(n_epochs, dtype=int),    np.ones(n_epochs, dtype=int)])
# Create MNE Epochs object
epochs = mne.EpochsArray(    data_volts,    info,    events=events,    event_id={'condition': 1},    tmin=-0.2,    baseline=None)
