import mne
from mne.preprocessing import ICA

raw_filtered = raw.copy().filter(l_freq=1.0, h_freq=None, n_jobs=None)

ica = ICA(n_components=10, random_state=97, max_iter='auto')
ica.fit(raw_filtered)
