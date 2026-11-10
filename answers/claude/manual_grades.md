# Manual grades — Claude
Grades marked *suggested* were drafted by Claude Code against each question's criteria; confirm or change them.

| question | grade | why (one line) |
|---|---|---|
| q004_filter_epochs_vs_raw | PASS (suggested) | Filter raw first; explains kernel longer than epoch and edge effects; suggests padding then crop. |
| q005_bdf_status_annotations | FAIL (suggested, strict) | Correct mask + find_events, but does not say Status is not converted to annotations; also wrongly says `uint_cast` is a `read_raw_bdf` argument (it belongs to `find_events`). |
| q011_bad_channel_before_avgref | PASS (suggested, concept) | Auto check crashed on a placeholder file path (question-design issue, see NOTES.md). Concept right, and the only reply that detects the bad channel automatically (robust z-score). |
| q016_label_timecourse_mean_flip | FAIL (suggested) | Closest of the three but wrong on the key point: claims all-positive free-orientation dSPM "wouldn't show this", when mean_flip on such data is exactly what creates the sign flips. |
| q017_bad_annotations_source | PASS (suggested, with error) | Correct on Epochs, raw covariance and apply_inverse_raw; but wrongly says the BAD match is case-sensitive (MNE uses `descr.lower().startswith("bad")`). |
| q018_tfr_long_epochs_rejection | PASS (suggested) | Explains wavelet leakage and widens the rejection window by the wavelet half-width. |
| q019_fsaverage_template_montage | FAIL (suggested, outdated) | Recommends `standard_1005`; says it can't verify 1.13 specifics (honest, still outdated). |
| q020_reporting_filters | PASS (suggested) | Display-only point; exact FIR defaults (-6 dB edges, 0.1/10 Hz transitions, 33 s at 1 kHz, ripple/attenuation). |
| q021_cluster_adjacency_none | FAIL (suggested) | Wrong core claim: says `adjacency=None` makes channels "fully connected"; the docstring says regular lattice along the last axis. Recommendation to use `find_ch_adjacency` is right. |
| q022_source_psd_units | PASS (suggested) | Dimensionless dSPM²/Hz; (A·m)²/Hz for method="MNE". |
| q023_psd_epoch_length | PASS (suggested, criterion 2 n/a) | 1/T resolution, leakage, variance; asks which toolbox was used. |

## Quality notes on automatic questions
- q001: 8-bit mask (0xFF) — fine here, would drop codes > 255 on 16-bit trigger setups.
- q006: suggests `set_montage("standard_1020")` in an optional block (would error in 1.13); main block scored.
- q009: the only assistant correct with a measurement date set (uses `raw.annotations.append`).
- q010: concept correct (adds Cz back) but crashes on MNE 1.13 because of `standard_1020`.
