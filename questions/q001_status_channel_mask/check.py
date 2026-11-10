import numpy as np

import mne

SFREQ = 256.0
ONSETS = [256, 768, 1280, 1792]
CODES = [1, 2, 1, 3]


def setup():
    n_times = int(SFREQ * 10)
    rng = np.random.default_rng(0)
    data = np.zeros((3, n_times))
    data[:2] = rng.standard_normal((2, n_times)) * 1e-5
    status = np.zeros(n_times)
    # system bit 16 toggles on and off independently of the triggers,
    # once in the middle of a trigger pulse (as happens in real recordings)
    status[400:700] += 2**16
    status[1285:1500] += 2**16
    for onset, code in zip(ONSETS, CODES):
        status[onset : onset + 10] += code
    data[2] = status
    info = mne.create_info(["EEG1", "EEG2", "Status"], SFREQ, ["eeg", "eeg", "stim"])
    return {"mne": mne, "np": np, "raw": mne.io.RawArray(data, info, verbose=False)}


def check(ns):
    events = ns.get("events")
    if events is None:
        return False, "no variable named `events`"
    events = np.asarray(events)
    if events.ndim != 2 or events.shape[1] != 3:
        return False, f"`events` has shape {events.shape}, expected (n, 3)"
    if events[:, 0].tolist() == ONSETS and events[:, 2].tolist() == CODES:
        return True, "correct events"
    return False, f"got codes {events[:, 2].tolist()} at {events[:, 0].tolist()}"
