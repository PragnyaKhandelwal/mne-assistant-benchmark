import mne
import numpy as np
# Get the original sample indices of the remaining epochs
onsets = (epochs.events[:, 0] - raw.first_samp) / raw.info['sfreq']
# Create annotations marking kept epochs
annotations = mne.Annotations(    onset=onsets,    duration=np.zeros(len(onsets)),    description=['kept'] * len(onsets),    orig_time=raw.annotations.orig_time)
# Add annotations to raw in place
raw.set_annotations(raw.annotations + annotations)
