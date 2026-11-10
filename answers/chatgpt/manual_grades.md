# Manual grades — ChatGPT
Grades marked *suggested* were drafted by Claude Code against each question's criteria; confirm or change them.

| question | grade | why (one line) |
|---|---|---|
| q004_filter_epochs_vs_raw | PASS (suggested) | Opens with "Yes, you can", but recommends filtering raw, warns about edge artifacts on 700 ms epochs, suggests longer epochs then crop. |
| q005_bdf_status_annotations | PASS (suggested) | Masks the upper bits in find_events (recommended over masking afterwards) and separates the Status channel from BDF annotations. |
| q011_bad_channel_before_avgref | PASS (suggested, concept) | Auto check crashed on example channel names (question-design issue, see NOTES.md). Concept right; correctly notes re-referencing again after marking bads also works. |
| q016_label_timecourse_mean_flip | FAIL (suggested) | Suggests pick_ori="normal", morphing, pca_flip; never identifies `mode="mean"` for magnitude dSPM. Ends with an interactive form. |
| q017_bad_annotations_source | FAIL (suggested, borderline) | Table is correct, but then claims `apply_inverse_raw` excludes BAD spans by default "as clarified by an MNE developer" — it has no such option, and this contradicts its own table. |
| q018_tfr_long_epochs_rejection | FAIL (suggested, borderline) | Recommends rejecting only within -0.2..0.8 s as the primary approach; leakage appears only as a caveat. |
| q019_fsaverage_template_montage | FAIL (suggested, outdated) | Recommends `standard_1005`, citing 1.3.1 docs. |
| q020_reporting_filters | FAIL (suggested, borderline) | Says MNE's default is FIR, but its own table lists Butterworth/IIR and "zero-phase for IIR" as what to report; hedges on whether the plot filter is display-only. |
| q021_cluster_adjacency_none | FAIL (suggested, borderline) | Opens with the wrong claim ("all channels are spatially connected"), then correctly explains the index-order lattice. Self-contradiction rule (NOTES.md). |
| q022_source_psd_units | PASS (suggested) | dSPM²/Hz, not a physical unit. |
| q023_psd_epoch_length | PASS (suggested, criterion 2 n/a) | 1/T resolution, cycles per window, leakage; ends with an interactive form. |

## Quality notes on automatic questions
- q001: masks before find_events, but via `astype(np.uint16)` (wraps values) and the private `raw._data`; calls the 24-bit Status channel "16-bit".
- q003: fits ICA on unfiltered data with no mention of high-pass filtering.
- q007: resamples raw and reuses the old events; then hesitates and suggests `events=events`, but never re-creates the epochs.
- q010: says Cz does not need to be added back; also suggests `raw.get_eeg_reference()`, which does not exist.
- q019, q024: outdated montage names for MNE 1.13.
