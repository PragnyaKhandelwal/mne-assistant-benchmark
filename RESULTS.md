# Pilot results (November 2026)

24 questions, 3 assistants, one attempt per question in a fresh chat, no follow-ups.
MNE-Python 1.13. Discussion: https://github.com/mne-tools/mne-python/issues/14428

| Assistant | Model | Plan |
|---|---|---|
| Gemini (web) | Gemini Flash Lite | free, not logged in |
| Claude (claude.ai) | Claude Sonnet 5.5 | free account |
| ChatGPT (web) | not shown in the free UI | free, logged in, Temporary Chat, Think off |

## Summary

| Group | Gemini | Claude | ChatGPT |
|---|---|---|---|
| Recent forum topics, 2024-26 (9) | 6 | 7 | 3 |
| Older forum topics, 2021-23 (11) | 9 | 9 | 8 |
| Known pitfalls from docs/GitHub (3) | 2 | 2 | 3 |
| Version awareness, MNE 1.13 (1) | 0 | 0 | 0 |
| **Total (24)** | **17** | **18** | **14** |

Groups: recent = q002, q003, q011, q012, q016-q020; older = q006-q010, q013-q015,
q021-q023; pitfalls = q001, q004, q005; version = q024.

## Per question

R = runnable (code executed against synthetic data and checked automatically),
M = graded by hand against the criteria in `questions/<id>/question.toml`.
⚠ = borderline manual grade (see below).

| # | Question | Type | Gemini | Claude | ChatGPT |
|---|---|---|---|---|---|
| q001 | BioSemi status channel mask | R | PASS | PASS | PASS |
| q002 | Average reference for inverse | R | FAIL (applied directly) | PASS | PASS |
| q003 | High-pass before ICA | R | PASS | PASS | FAIL (unfiltered) |
| q004 | Filtering short epochs | M | PASS | PASS | PASS |
| q005 | BDF status vs annotations | M | FAIL ⚠ | FAIL ⚠ | PASS |
| q006 | µV to volts | R | PASS | PASS | PASS |
| q007 | Resample then epoch | R | FAIL (reused events) | PASS | FAIL (reused events) |
| q008 | Grand average from files | R | PASS | PASS | PASS |
| q009 | Epoch onsets to annotations | R | PASS | PASS | PASS |
| q010 | Recording reference not in file | R | FAIL (invalid argument) | FAIL (old montage name) | FAIL (Cz not added) |
| q011 | Noisy channel before average ref | M* | PASS | PASS | PASS |
| q012 | Muscle artifact bursts | R | PASS | PASS | PASS |
| q013 | Epochs without baseline | R | PASS | PASS | PASS |
| q014 | Statistics on clean data only | R | PASS | PASS | PASS |
| q015 | Paired cluster permutation test | R | PASS | PASS | PASS |
| q016 | `mean_flip` on dSPM estimates | M | FAIL | FAIL | FAIL |
| q017 | BAD annotations in source analysis | M | PASS | PASS ⚠ | FAIL ⚠ |
| q018 | Rejection with padded TFR epochs | M | PASS | PASS | FAIL ⚠ |
| q019 | fsaverage template montage (1.13) | M | FAIL | FAIL | FAIL |
| q020 | Reporting filter settings | M | PASS | PASS | FAIL ⚠ |
| q021 | `adjacency=None` in cluster tests | M | PASS | FAIL | FAIL ⚠ |
| q022 | Units of dSPM source PSD | M | PASS | PASS | PASS |
| q023 | PSD vs epoch length | M* | PASS | PASS | PASS |
| q024 | Standard montage in MNE 1.13 | R | FAIL | FAIL | FAIL |

\* q011 is runnable, but every reply used a placeholder channel name or file path, so it
was graded by hand on the concept; q023 was graded on its generic criterion only. Both are
question-design issues, described in [NOTES.md](NOTES.md).

One-line reasons for every manual grade are in `answers/<assistant>/manual_grades.md`,
and the raw replies are in `answers/<assistant>/<id>.md`.

## Grading rule and borderline cases

Manual grades use a **strict** rule: a reply that makes a wrong, definite claim about
the thing asked fails, even if it also gives the right answer elsewhere. Under a
**lenient** rule (main recommendation only), ChatGPT q017 and q021 and Gemini q005 would
pass (Gemini 18, ChatGPT 16). Borderline cases:

- **Gemini q005, Claude q005:** correct masking code, but neither says that the Status
  channel is not converted to annotations (criterion 1). Claude also places `uint_cast`
  on `read_raw_bdf` (it belongs to `find_events`).
- **Claude q017:** correct overall, but says BAD matching is case-sensitive
  (MNE uses `descr.lower().startswith("bad")`).
- **ChatGPT q017:** correct table, then states that `apply_inverse_raw` skips BAD spans by
  default; it has no such option.
- **ChatGPT q018:** recommends rejecting only within the window of interest; leakage
  appears only as a caveat.
- **ChatGPT q020:** says MNE's default is FIR, but its table lists Butterworth/IIR as what
  to report.
- **ChatGPT q021:** opens with "all channels are spatially connected", then correctly
  explains the index-order lattice.

## Observations

1. **Recent topics are harder.** Pass rate on recent vs older forum topics: Gemini 67% vs
   82%, Claude 78% vs 82%, ChatGPT 33% vs 73%. Small samples, so a trend rather than a result.
2. **The MNE 1.13 montage rename accounts for 7 of the 23 failures.** All three fail q024
   even though the prompt says "MNE-Python 1.13", all three recommend `standard_1005` for
   fsaverage (q019), and Claude's otherwise correct q010 crashes on `standard_1020`.
3. **Known forum pitfalls still appear:** reusing the original events after resampling
   (Gemini and ChatGPT, q007) and fitting ICA on unfiltered data (ChatGPT, q003).
4. **No assistant answered q016** (`mean_flip` on all-positive dSPM estimates), a 2025
   forum topic.
5. **Non-existent or misplaced API**, checked against the MNE source:
   `Raw.set_eeg_reference(copy=...)` (Gemini q010), `raw.get_eeg_reference()` (ChatGPT
   q010), `uint_cast` in `read_raw_bdf` (Claude q005).
6. **Confident wrong claims about MNE behaviour:** `adjacency=None` as "fully connected"
   (Claude q021), case-sensitive BAD matching (Claude q017), `apply_inverse_raw` skipping
   BAD spans (ChatGPT q017).

## Limitations

- **One run per question.** Redoing q001-q010 in fresh chats changed five results
  compared with an earlier shared-chat run (kept in git history). Answers vary between
  runs; a future version should repeat each prompt several times.
- **Small question set**, and the recent/older split is by forum post date, not by any
  model's training cutoff.
- **Grading and possible bias.** Manual grades were made by one person. The questions,
  checks and suggested manual grades were drafted with help from Claude Code (a Claude
  model), and Claude scored highest, so independent grading of the manual questions would
  strengthen these results.
- **Free tiers only**, with the model version not always visible (ChatGPT).
