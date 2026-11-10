# Manual grades — Gemini
Grades marked *suggested* were drafted by Claude Code against each question's criteria; confirm or change them.

| question | grade | why (one line) |
|---|---|---|
| q004_filter_epochs_vs_raw | PASS (suggested) | Filter raw first; explains filter (~3.3 s) longer than 0.7 s epoch; advises no high-pass on epochs. Does not suggest padding/cropping. |
| q005_bdf_status_annotations | FAIL (suggested, strict) | Correct mask + find_events, but never says Status is not converted to annotations (criterion 1). Core code correct. |
| q011_bad_channel_before_avgref | PASS (suggested, concept) | Auto check crashed on the placeholder channel 'EEG 0XX' (question-design issue, see NOTES.md). Concept right: mark bads before re-referencing; reload; interpolate. |
| q016_label_timecourse_mean_flip | FAIL (suggested) | Suggests post-hoc sign alignment / abs values; never identifies that free-orientation dSPM is all-positive so `mode="mean"` is the right choice. |
| q017_bad_annotations_source | PASS (suggested) | BAD-prefixed spans excluded by Epochs and compute_raw_covariance by default; notes inverse on raw still processes bad spans. |
| q018_tfr_long_epochs_rejection | PASS (suggested) | Explains leakage into the window (worse at low frequencies) and suggests a buffered rejection window. |
| q019_fsaverage_template_montage | FAIL (suggested, outdated) | Recommends `standard_1005` + trans="fsaverage"; in 1.13 that montage no longer exists (tutorial uses `fsaverage_1005`). Also links a YouTube video. |
| q020_reporting_filters | PASS (suggested) | Plot filter is display-only; report FIR/firwin/Hamming/zero-phase, transition bands, length; found in the log. |

## Quality notes on automatic questions
- q002: reply also contains a conditional block using `standard_1020` (would error in 1.13); main block scored.
- q009: uses `orig_time=raw.info["meas_date"]` after subtracting first_samp — correct only when meas_date is None; shifts annotations on real recordings.
- q010: concept correct (adds Cz back) but the code crashes on MNE 1.13 because of the renamed `standard_1020` montage.
