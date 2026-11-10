import mne
from mne.preprocessing import annotate_muscle_zscore
# Detect muscle artifacts
annotations, scores = annotate_muscle_zscore(    raw,    ch_type="eeg",    threshold=4,    min_length_good=0.1,    filter_freq=(110, 140))
# Add muscle annotations to the raw data
raw.set_annotations(raw.annotations + annotations)
# Create epochs around all events, rejecting epochs overlapping muscle artifacts
epochs = mne.Epochs(    raw,    events,    event_id=None,    tmin=-0.2,    tmax=0.5,    baseline=None,    reject_by_annotation=True,    preload=True)
