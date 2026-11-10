# Manual grades — Claude
Grades marked *suggested* were drafted by Claude Code against each question's criteria; confirm or change them.

| question | grade | why (one line) |
|---|---|---|
| q004_filter_epochs_vs_raw | PASS (suggested) | Filter raw first; explains kernel longer than epoch and edge effects; suggests padding then crop. |
| q005_bdf_status_annotations | FAIL (suggested, strict) | Correct mask + find_events, but does not say Status is not converted to annotations; also wrongly says `uint_cast` is a `read_raw_bdf` argument (it belongs to `find_events`). |

## Quality notes on automatic questions
- q001: 8-bit mask (0xFF) — fine here, would drop codes > 255 on 16-bit trigger setups.
- q006: suggests `set_montage("standard_1020")` in an optional block (would error in 1.13); main block scored.
- q009: the only assistant correct with a measurement date set (uses `raw.annotations.append`).
- q010: concept correct (adds Cz back) but crashes on MNE 1.13 because of `standard_1020`.
