import numpy as np

import mne


def setup():
    rng = np.random.default_rng(0)
    names = ["Fp1", "Fp2", "Fz", "Cz", "Pz", "C3", "C4", "O1", "O2"]
    info = mne.create_info(names, 250.0, "eeg")
    data = rng.standard_normal((len(names), 500)) * 1e-6
    return {"mne": mne, "np": np, "raw": mne.io.RawArray(data, info, verbose=False)}


def check(ns):
    raw = ns["raw"]
    if raw.get_montage() is None:
        return False, "no montage set"
    pos = np.array([ch["loc"][:3] for ch in raw.info["chs"]])
    if np.isnan(pos).any() or np.allclose(pos, 0, atol=1e-6):
        return False, "montage set but channels have no positions"
    return True, "template positions set"
