import mne

raw.load_data()

mne.add_reference_channels(raw, ref_channels="Cz", copy=False)

montage = mne.channels.make_standard_montage("standard_1020")
raw.set_montage(montage, on_missing="warn")

raw.set_eeg_reference("average", projection=False)
