```
from mne.preprocessing import ICAica = ICA(n_components=10, random_state=42)ica.fit(raw)
```

The fitted ICA object is stored in `ica`. You can later use it to identify eye-blink components and remove them from your EEG data.
