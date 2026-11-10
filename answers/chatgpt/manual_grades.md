# Manual grades — ChatGPT
Grades marked *suggested* were drafted by Claude Code against each question's criteria; confirm or change them.

| question | grade | why (one line) |
|---|---|---|
| q004_filter_epochs_vs_raw | PASS (suggested) | Opens with "Yes, you can", but recommends filtering raw, mentions edge artifacts, suggests longer epochs then crop. |
| q005_bdf_status_annotations | PASS (suggested) | find_events with 16-bit mask and `uint_cast=True` (correct place); explicitly separates Status channel from BDF annotations. |

## Quality notes on automatic questions
- q006: concept correct (µV → V) but crashes on MNE 1.13: `info.set_montage('standard_1020')` inside the main code.
- q009: subtracts first_samp and uses `orig_time=raw.annotations.orig_time` — shifts annotations whenever a measurement date is set.
- q010: says missing Cz "is not a problem" — conceptually wrong.
- Several replies cite MNE dev-build docs hosted on CircleCI artifacts (q004).
