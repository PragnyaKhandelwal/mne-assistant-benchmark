import numpy as np

import mne

NAMES = ["Fz", "C3", "C4", "Pz", "O1", "O2", "F3", "F4"]
EXPECTED = None


def setup():
    global EXPECTED
    rng = np.random.default_rng(0)
    true = rng.standard_normal((len(NAMES) + 1, 2500)) * 1e-5  # last row is Cz
    EXPECTED = (true - true.mean(0))[:-1]
    recorded = true[:-1] - true[-1]
    info = mne.create_info(NAMES, 250.0, "eeg")
    return {"mne": mne, "np": np, "raw": mne.io.RawArray(recorded, info, verbose=False)}


def check(ns):
    raw = ns["raw"]
    if "Cz" not in raw.ch_names:
        return False, "Cz was not added back before averaging"
    data = raw.copy().apply_proj(verbose=False).get_data(picks=NAMES)
    if np.allclose(data, EXPECTED, atol=1e-9):
        return True, "average reference includes Cz"
    return False, "Cz present but data are not average-referenced correctly"
