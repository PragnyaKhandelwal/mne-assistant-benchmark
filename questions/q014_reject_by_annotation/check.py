import numpy as np

import mne

EXPECTED = None


def setup():
    global EXPECTED
    rng = np.random.default_rng(0)
    data = rng.standard_normal((4, 5000)) * 1e-5
    data[:, 1250:1750] += rng.standard_normal((4, 500)) * 1e-3
    info = mne.create_info(["Fz", "Cz", "Pz", "Oz"], 250.0, "eeg")
    raw = mne.io.RawArray(data, info, verbose=False)
    raw.set_annotations(mne.Annotations([5.0], [2.0], ["BAD_artifact"]))
    EXPECTED = np.var(np.delete(data, np.s_[1250:1750], axis=1), axis=1)
    return {"mne": mne, "np": np, "raw": raw}


def check(ns):
    variances = ns.get("variances")
    if variances is None or np.shape(variances) != (4,):
        return False, "`variances` is not an array of shape (n_channels,)"
    if np.allclose(variances, EXPECTED, rtol=0.02):
        return True, "variance computed on clean data"
    return False, "variance includes the BAD_ spans"
