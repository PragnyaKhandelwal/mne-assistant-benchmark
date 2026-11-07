import numpy as np

import mne
import tempfile
from pathlib import Path

EXPECTED = None


def setup():
    global EXPECTED
    rng = np.random.default_rng(0)
    info = mne.create_info(["Fz", "Cz", "Pz"], 250.0, "eeg")
    tmp = Path(tempfile.mkdtemp())
    fnames, datas = [], []
    for sub in range(5):
        data = rng.standard_normal((3, 100)) * 1e-6
        evoked = mne.EvokedArray(data, info, tmin=-0.1, nave=30, comment="target")
        fname = tmp / f"sub-{sub:02d}-ave.fif"
        mne.write_evokeds(fname, evoked, verbose=False)
        fnames.append(str(fname))
        datas.append(data)
    EXPECTED = np.mean(datas, axis=0)
    return {"mne": mne, "np": np, "fnames": fnames}


def check(ns):
    grand_avg = ns.get("grand_avg")
    if not isinstance(grand_avg, mne.Evoked):
        return False, f"`grand_avg` is {type(grand_avg).__name__}, not Evoked"
    if np.allclose(grand_avg.data, EXPECTED, atol=1e-12):
        return True, "grand average over all participants"
    return False, "grand average does not match the mean of all participants"
