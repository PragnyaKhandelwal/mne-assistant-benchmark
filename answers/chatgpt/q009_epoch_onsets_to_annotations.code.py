import mne
# Get the onset times of the remaining epochs relative to raw
onsets = (epochs.events[:, 0] - raw.first_samp) / raw.info['sfreq']
# Create annotations
annotations = mne.Annotations(    onset=onsets,    duration=[0] * len(onsets),    description=['kept'] * len(onsets))
# Add annotations to raw in place
raw.set_annotations(raw.annotations + annotations)
