# Manual grades — Gemini
Grades marked *suggested* were drafted by Claude Code against each question's criteria; confirm or change them.

| question | grade | why (one line) |
|---|---|---|
| q004_filter_epochs_vs_raw | PASS (suggested) | Filter raw first; explains filter (~3.3 s) longer than 0.7 s epoch; advises no high-pass on epochs. Does not suggest padding/cropping. |
| q005_bdf_status_annotations | FAIL (suggested, strict) | Correct mask + find_events, but never says Status is not converted to annotations (criterion 1). Core code correct. |

## Quality notes on automatic questions
- q002: reply also contains a conditional block using `standard_1020` (would error in 1.13); main block scored.
- q009: uses `orig_time=raw.info["meas_date"]` after subtracting first_samp — correct only when meas_date is None; shifts annotations on real recordings.
- q010: concept correct (adds Cz back) but the code crashes on MNE 1.13 because of the renamed `standard_1020` montage.
