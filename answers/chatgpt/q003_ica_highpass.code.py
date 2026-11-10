import mne
from mne.preprocessing import ICA
# Create a filtered copy for ICA fitting
raw_ica = raw.copy().filter(l_freq=1.0, h_freq=None)
# Initialize ICA with 10 components
ica = ICA(    n_components=10,    random_state=42,    max_iter='auto')
# Fit ICA
ica.fit(raw_ica)
