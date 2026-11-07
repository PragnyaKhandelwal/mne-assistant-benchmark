import numpy as np

import mne

SFREQ = 500.0
ONSETS = (SFREQ * (2 + 3 * np.arange(19))).astype(int)  # event at 20 s overlaps the burst


def setup():
    rng = np.random.default_rng(0)
    n_times = int(SFREQ * 60)
    data = np.zeros((9, n_times))
    data[:8] = rng.standard_normal((8, n_times)) * 5e-6
    burst = slice(int(20 * SFREQ), int(21 * SFREQ))
    t = np.arange(burst.stop - burst.start) / SFREQ
    data[:8, burst] += 30e-6 * np.sin(2 * np.pi * 125 * t) * rng.standard_normal((8, 1))
    data[8, ONSETS] = 1
    names = ["Fz", "Cz", "Pz", "C3", "C4", "T7", "T8", "Oz", "STI"]
    info = mne.create_info(names, SFREQ, ["eeg"] * 8 + ["stim"])
    raw = mne.io.RawArray(data, info, verbose=False)
    return {"mne": mne, "np": np, "raw": raw, "events": mne.find_events(raw, verbose=False)}


def check(ns):
    epochs = ns.get("epochs")
    if not isinstance(epochs, mne.BaseEpochs):
        return False, "no Epochs object in `epochs`"
    epochs.drop_bad(verbose=False)
    kept = set(epochs.events[:, 0].tolist())
    if int(20 * SFREQ) in kept:
        return False, "the epoch overlapping the muscle burst was kept"
    if len(kept) < len(ONSETS) - 2:
        return False, f"too many clean epochs dropped ({len(kept)}/{len(ONSETS)} kept)"
    return True, f"burst epoch excluded, {len(kept)}/{len(ONSETS)} kept"
