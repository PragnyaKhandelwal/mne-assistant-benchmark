import mne
# Load each participant's Evoked file
evokeds = [mne.read_evokeds(fname, condition=0) for fname in fnames]
# Compute grand average
grand_avg = mne.grand_average(evokeds)
# Inspect the result
print(grand_avg)
