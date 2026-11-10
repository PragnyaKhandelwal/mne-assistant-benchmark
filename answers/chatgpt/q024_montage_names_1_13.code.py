import mne
# Load the standard 10-20 electrode positions
montage = mne.channels.make_standard_montage("standard_1020")
# Apply positions directly to raw (in place)
raw.set_montage(montage)
