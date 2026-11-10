# Identify channels that are noisy or malfunctioning
bad_channels = ['Fp1', 'T8']  # Replace with your actual bad channels
# Mark them as bad
raw.info['bads'] = bad_channels
# Recompute the average reference, in-place
raw.set_eeg_reference(ref_channels='average', projection=False)
# Check the result
raw.plot()
