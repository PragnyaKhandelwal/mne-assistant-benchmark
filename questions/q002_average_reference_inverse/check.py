import numpy as np

import mne


def setup():
    rng = np.random.default_rng(0)
    ch_names = ["Fz", "Cz", "Pz", "C3", "C4", "O1", "O2", "Fp1"]
    info = mne.create_info(ch_names, 256.0, "eeg")
    data = rng.standard_normal((len(ch_names), 2560)) * 1e-5
    raw = mne.io.RawArray(data, info, verbose=False)
    return {"mne": mne, "np": np, "raw": raw}


def check(ns):
    raw = ns["raw"]
    has_proj = any("Average EEG reference" in p["desc"] for p in raw.info["projs"])
    if has_proj:
        return True, "average reference added as a projector"
    if raw.info["custom_ref_applied"]:
        return False, "average reference applied directly, not as a projector"
    return False, "no average reference set"
