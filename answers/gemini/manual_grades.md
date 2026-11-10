# Manual grades — Gemini
Grades marked *suggested* were drafted by Claude Code against each question's criteria; confirm or change them.

| question | grade | why (one line) |
|---|---|---|
| q004_filter_epochs_vs_raw | PASS (suggested) | Filter raw first; explains ringing on short epochs; suggests wider epochs then crop. |
| q005_bdf_status_annotations | FAIL (suggested, strict) | Correct 16-bit mask with find_events, but never says Status is not turned into annotations (criterion 1). |
| q011_bad_channel_before_avgref | PASS (suggested, concept) | Auto check crashed on the placeholder channel 'EEG 0XX' (question-design issue, see NOTES.md). Concept right: mark bads before re-referencing; reload; interpolate. |
| q016_label_timecourse_mean_flip | FAIL (suggested) | Suggests post-hoc sign alignment / abs values; never identifies that free-orientation dSPM is all-positive so `mode="mean"` is the right choice. |
| q017_bad_annotations_source | PASS (suggested) | BAD-prefixed spans excluded by Epochs and compute_raw_covariance by default; notes inverse on raw still processes bad spans. |
| q018_tfr_long_epochs_rejection | PASS (suggested) | Explains leakage into the window (worse at low frequencies) and suggests a buffered rejection window. |
| q019_fsaverage_template_montage | FAIL (suggested, outdated) | Recommends `standard_1005` + trans="fsaverage"; in 1.13 that montage no longer exists (tutorial uses `fsaverage_1005`). Also links a YouTube video. |
| q020_reporting_filters | PASS (suggested) | Plot filter is display-only; report FIR/firwin/Hamming/zero-phase, transition bands, length; found in the log. |
| q021_cluster_adjacency_none | PASS (suggested) | Correct: regular lattice by array order along the channel axis; build adjacency with `find_ch_adjacency`. |
| q022_source_psd_units | PASS (suggested) | dSPM is dimensionless (dSPM²/Hz); method="MNE" gives Am²/Hz. |
| q023_psd_epoch_length | PASS (suggested, criterion 2 n/a) | Explains 1/T resolution and leakage. Does not mention MNE's Welch-vs-multitaper defaults, but the prompt never says MNE (see NOTES.md). |

## Quality notes on automatic questions
- q002: main code applies the reference directly (`projection=False`); the projector appears only as an alternative.
- q003: the direct answer fits ICA on unfiltered data; the 1 Hz filtered version is given as "strongly recommended" and that block was scored.
- q007: resamples raw and reuses the 1000 Hz events (the classic forum pitfall).
- q010: concept right (adds Cz back) but passes `copy=False` to `Raw.set_eeg_reference`, which has no such parameter.
- q019, q024: outdated montage names for MNE 1.13.
