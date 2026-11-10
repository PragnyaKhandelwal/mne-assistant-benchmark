from mne.preprocessing import ICA
ica = ICA(n_components=10, random_state=42)
ica.fit(raw)
