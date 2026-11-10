import mne
from mne.preprocessing import ICA

raw_for_ica = raw.copy().load_data().filter(l_freq=1.0, h_freq=None)

ica = ICA(
    n_components=10,
    method="fastica",
    max_iter="auto",
    random_state=97,
)
ica.fit(raw_for_ica)
