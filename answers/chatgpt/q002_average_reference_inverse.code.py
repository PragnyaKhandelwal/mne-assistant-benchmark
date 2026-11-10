import mne
# Add an average EEG reference projector
raw.set_eeg_reference(ref_channels='average', projection=True)
