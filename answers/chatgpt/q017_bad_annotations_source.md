Not automatically in every operation. In MNE-Python, manually annotated bad segments are stored in raw.annotations, but whether they are excluded depends on the function you call and its parameters.

The important distinction is between:
- BAD annotations: Mark portions of continuous data that should generally be excluded from analysis.
- Other annotations: Such as EDGE or experimental event labels, which do not necessarily indicate bad data.
For a resting-state pipeline, you should explicitly check how annotations are handled at each stage, particularly covariance estimation and source reconstruction.
Behavior at each stage
Pipeline operation	Are bad annotations excluded?	Important detail
mne.compute_raw_covariance()	Yes, by default	reject_by_annotation=True
mne.Epochs()	Yes, by default	Drops epochs overlapping bad segments
mne.compute_covariance()	Yes, indirectly	Uses the epochs supplied; bad epochs should already have been dropped
Source estimates from Epochs	Yes, indirectly	Only retained epochs contribute
Source estimates directly from Raw	No automatic exclusion	Annotations do not automatically mask the resulting continuous source estimates

These defaults are documented in MNE's bad-data rejection tutorial.

MNE 1.13.2 documentation+2

1. Covariance estimation
For continuous data:
noise_cov = mne.compute_raw_covariance(    raw,    tmin=0,    tmax=None,    reject_by_annotation=True)



This excludes data chunks overlapping annotations beginning with BAD or bad.

For example:
- BAD_blink → excluded
- BAD_movement → excluded
- BAD_muscle → excluded
- blink → not automatically excluded
Note that compute_covariance() operates on an Epochs or Evoked object, rather than directly filtering annotations in the original Raw object.
2. Epoch creation
events = mne.make_fixed_length_events(    raw,    id=1,    duration=2.0)epochs = mne.Epochs(    raw,    events,    event_id=1,    tmin=0,    tmax=2.0,    baseline=None,    reject_by_annotation=True,    preload=True)



An epoch is rejected if any portion overlaps a bad annotation.

For example, if a 2-second epoch overlaps a BAD_movement segment for just 100 ms, the entire epoch is dropped.

You can inspect the result:
print(epochs)print(epochs.drop_log)




GitHub+1
3. Source reconstruction
This is an important distinction.

If you reconstruct sources from cleaned epochs:
stcs = mne.minimum_norm.apply_inverse_epochs(    epochs,    inverse_operator,    lambda2=1.0 / 9.0,    method="dSPM")



Bad segments have already been excluded during epoch creation, so they cannot contribute to the source estimates.

If you reconstruct directly from continuous Raw data:
stc = mne.minimum_norm.apply_inverse_raw(    raw,    inverse_operator,    lambda2=1.0 / 9.0,    method="dSPM")



MNE's source-reconstruction handling also excludes annotations beginning with BAD by default in current versions. This behavior has been specifically clarified by an MNE developer.

MNE Forum

4. My recommendations for your resting-state pipeline
I would use the following conventions:

First, consistently name bad segments:
BAD_movementBAD_muscleBAD_blinkBAD_electrodeBAD_noise



Second, explicitly enable annotation rejection wherever the parameter is available:
reject_by_annotation=True



Third, verify the annotations before processing:
print(raw.annotations)# Inspect bad annotationsbad_annotations = [    (onset, duration, description)    for onset, duration, description    in zip(        raw.annotations.onset,        raw.annotations.duration,        raw.annotations.description    )    if description.lower().startswith("bad")]print(bad_annotations)



Fourth, check the amount of retained data:
print(f"Original duration: {raw.times[-1]:.2f} seconds")print(f"Retained epochs: {len(epochs)}")print(epochs.drop_log_stats())




Bottom line: You do not need to physically delete manually annotated bad segments from your continuous recording. Keep them in raw.annotations, use descriptions beginning with BAD, and make annotation rejection explicit wherever possible.

This preserves your original continuous recording and makes your resting-state analysis more reproducible.

Official reference: MNE-Python: Rejecting bad data spans and breaks.
