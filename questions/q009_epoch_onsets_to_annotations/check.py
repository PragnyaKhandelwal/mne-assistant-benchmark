import numpy as np

import mne


def setup():
    rng = np.random.default_rng(0)
    sfreq = 100.0
    data = rng.standard_normal((2, 6000)) * 1e-6
    info = mne.create_info(["Cz", "Pz"], sfreq, "eeg")
    raw = mne.io.RawArray(data, info, first_samp=1000, verbose=False)
    events = mne.make_fixed_length_events(raw, duration=5.0)
    epochs = mne.Epochs(raw, events, tmin=0, tmax=4.99, baseline=None, preload=True, verbose=False)
    epochs.drop([1, 4], verbose=False)
    return {"mne": mne, "np": np, "raw": raw, "epochs": epochs}


def check(ns):
    raw, epochs = ns["raw"], ns["epochs"]
    if "kept" not in raw.annotations.description:
        return False, "no 'kept' annotations in raw"
    events, _ = mne.events_from_annotations(raw, event_id={"kept": 1}, verbose=False)
    expected = epochs.events[:, 0] + int(round(epochs.tmin * raw.info["sfreq"]))
    if len(events) == len(expected) and np.abs(events[:, 0] - expected).max() <= 1:
        return True, "annotations aligned with epoch starts"
    return False, f"annotations at samples {events[:, 0].tolist()}, expected {expected.tolist()}"
