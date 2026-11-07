import numpy as np

import mne

NAMES = ["Fz", "Cz", "Pz", "C3", "C4", "T7", "O1", "O2"]


def setup():
    rng = np.random.default_rng(0)
    data = rng.standard_normal((len(NAMES), 5000)) * 1e-5
    data[NAMES.index("T7")] *= 50
    info = mne.create_info(NAMES, 250.0, "eeg")
    return {"mne": mne, "np": np, "raw": mne.io.RawArray(data, info, verbose=False)}


def check(ns):
    raw = ns["raw"]
    has_ref = raw.info["custom_ref_applied"] or any(
        "Average EEG reference" in p["desc"] for p in raw.info["projs"])
    if not has_ref:
        return False, "no average reference set"
    good = [ch for ch in raw.ch_names if ch not in raw.info["bads"] and ch != "T7"]
    std = raw.copy().apply_proj(verbose=False).get_data(picks=good).std()
    if std < 2e-5:
        return True, "noisy channel excluded from the average"
    return False, f"T7 noise spread to good channels (std {std:.1e} V)"
