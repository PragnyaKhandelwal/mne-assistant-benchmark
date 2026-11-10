import mne

raw.load_data()

raw.set_eeg_reference(ref_channels='average', projection=False)
