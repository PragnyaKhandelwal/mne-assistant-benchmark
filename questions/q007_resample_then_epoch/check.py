import numpy as np

import mne

SFREQ = 1000.0
ONSETS = 1000 + 1300 * np.arange(20)


def setup():
    rng = np.random.default_rng(0)
    n_times = int(SFREQ * 30)
    data = np.zeros((5, n_times))
    data[:4] = rng.standard_normal((4, n_times)) * 2e-6
    bump = 20e-6 * np.exp(-0.5 * ((np.arange(-50, 51)) / 15) ** 2)
    for onset in ONSETS:
        data[:4, onset + 50 : onset + 151] += bump  # peak at 100 ms
        data[4, onset : onset + 20] = 1
    info = mne.create_info(["Fz", "Cz", "Pz", "Oz", "STI"], SFREQ, ["eeg"] * 4 + ["stim"])
    raw = mne.io.RawArray(data, info, verbose=False)
    events = mne.find_events(raw, verbose=False)
    return {"mne": mne, "np": np, "raw": raw, "events": events}


def check(ns):
    epochs = ns.get("epochs")
    if not isinstance(epochs, mne.BaseEpochs):
        return False, "no Epochs object in `epochs`"
    epochs.drop_bad(verbose=False)  # length is unknown until bad epochs are dropped
    if round(epochs.info["sfreq"]) != 250:
        return False, f"epochs are at {epochs.info['sfreq']} Hz, not 250 Hz"
    if len(epochs) != len(ONSETS):
        return False, f"{len(epochs)} epochs instead of {len(ONSETS)} (misaligned events?)"
    evoked = epochs.average(picks="eeg")
    peak = evoked.times[np.argmax(evoked.data.mean(0))]
    if abs(peak - 0.1) <= 0.012:
        return True, "correctly time-locked at 250 Hz"
    return False, f"evoked peak at {peak * 1000:.0f} ms instead of 100 ms"
