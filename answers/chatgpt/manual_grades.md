# Manual grades — ChatGPT
Grades marked *suggested* were drafted by Claude Code against each question's criteria; confirm or change them.

| question | grade | why (one line) |
|---|---|---|
| q004_filter_epochs_vs_raw | PASS (suggested) | Opens with "Yes, you can", but recommends filtering raw, mentions edge artifacts, suggests longer epochs then crop. |
| q005_bdf_status_annotations | PASS (suggested) | find_events with 16-bit mask and `uint_cast=True` (correct place); explicitly separates Status channel from BDF annotations. |
| q011_bad_channel_before_avgref | PASS (suggested, concept) | Auto check crashed on example channel names (question-design issue, see NOTES.md). Concept right; correctly notes re-referencing again after marking bads also works. |
| q016_label_timecourse_mean_flip | FAIL (suggested) | Suggests pick_ori="normal", morphing, pca_flip; never identifies `mode="mean"` for magnitude dSPM. Ends with an interactive form. |
| q017_bad_annotations_source | FAIL (suggested, borderline) | Table is correct, but then claims `apply_inverse_raw` excludes BAD spans by default "as clarified by an MNE developer" — it has no such option, and this contradicts its own table. |
| q018_tfr_long_epochs_rejection | FAIL (suggested, borderline) | Recommends rejecting only within -0.2..0.8 s as the primary approach; leakage appears only as a caveat. |
| q019_fsaverage_template_montage | FAIL (suggested, outdated) | Recommends `standard_1005`, citing 1.3.1 docs. |
| q020_reporting_filters | FAIL (suggested, borderline) | Says MNE's default is FIR, but its own table lists Butterworth/IIR and "zero-phase for IIR" as what to report; hedges on whether the plot filter is display-only. |

## Quality notes on automatic questions
- q006: concept correct (µV → V) but crashes on MNE 1.13: `info.set_montage('standard_1020')` inside the main code.
- q009: subtracts first_samp and uses `orig_time=raw.annotations.orig_time` — shifts annotations whenever a measurement date is set.
- q010: says missing Cz "is not a problem" — conceptually wrong.
- Several replies cite MNE dev-build docs hosted on CircleCI artifacts (q004).
