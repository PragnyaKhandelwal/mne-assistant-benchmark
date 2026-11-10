import mne

evokeds = [mne.read_evokeds(fname, condition=0) for fname in fnames]

grand_avg = mne.grand_average(evokeds)
