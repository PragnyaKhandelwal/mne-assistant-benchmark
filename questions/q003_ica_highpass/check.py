import numpy as np

import mne


def setup():
    rng = np.random.default_rng(0)
    ch_names = ["Fp1", "Fp2", "F3", "F4", "C3", "C4", "P3", "P4",
                "O1", "O2", "F7", "F8", "T7", "T8", "Fz", "Pz"]  # fmt: skip
    sfreq = 128.0
    n_times = int(sfreq * 60)
    times = np.arange(n_times) / sfreq
    drift = np.outer(rng.standard_normal(len(ch_names)), np.sin(2 * np.pi * 0.05 * times))
    data = (rng.standard_normal((len(ch_names), n_times)) + 5 * drift) * 1e-5
    info = mne.create_info(ch_names, sfreq, "eeg")
    raw = mne.io.RawArray(data, info, verbose=False)
    return {"mne": mne, "np": np, "raw": raw}


def check(ns):
    ica = ns.get("ica")
    if not isinstance(ica, mne.preprocessing.ICA):
        return False, "no fitted `ica` variable"
    if ica.current_fit == "unfitted":
        return False, "ICA was created but not fitted"
    highpass = ica.info["highpass"]
    if highpass >= 1.0:
        return True, f"fitted on data high-passed at {highpass} Hz"
    return False, f"fitted on data high-passed at only {highpass} Hz"
