import numpy as np

import mne

OFFSET = 50e-6


def setup():
    rng = np.random.default_rng(0)
    data = np.zeros((3, 10000))
    data[:2] = rng.standard_normal((2, 10000)) * 1e-6 + OFFSET
    data[2, 1000::1000] = 1
    info = mne.create_info(["Cz", "Pz", "STI"], 250.0, ["eeg", "eeg", "stim"])
    raw = mne.io.RawArray(data, info, verbose=False)
    events = mne.find_events(raw, verbose=False)
    epochs = mne.Epochs(raw, events, tmin=-0.2, tmax=0.5, verbose=False)
    return {"mne": mne, "np": np, "raw": raw, "events": events, "epochs": epochs}


def check(ns):
    data = ns.get("data")
    if data is None or np.ndim(data) != 3:
        return False, "`data` is not an (n_epochs, n_channels, n_times) array"
    mean = np.asarray(data)[:, :2].mean()
    if abs(mean - OFFSET) < 5e-6:
        return True, "DC offset preserved (no baseline correction)"
    return False, f"mean is {mean:.1e} V; baseline correction still applied"
