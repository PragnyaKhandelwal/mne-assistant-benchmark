import numpy as np

import mne


def setup():
    rng = np.random.default_rng(0)
    data = rng.standard_normal((20, 4, 256)) * 10  # microvolts
    return {"mne": mne, "np": np, "data": data, "ch_names": ["Fz", "Cz", "Pz", "Oz"], "sfreq": 256.0}


def check(ns):
    epochs = ns.get("epochs")
    if not isinstance(epochs, mne.BaseEpochs):
        return False, "no Epochs object in `epochs`"
    ratio = epochs.get_data().std() / 10.0
    if abs(ratio - 1e-6) < 0.05e-6:
        return True, "data stored in volts"
    if abs(ratio - 1) < 0.05:
        return False, "data left in microvolts (MNE expects volts)"
    return False, f"unexpected scaling (factor {ratio:.3g})"
