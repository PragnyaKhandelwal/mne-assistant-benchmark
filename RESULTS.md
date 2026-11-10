# Pilot results (November 2026, provisional)

24 questions, 3 free assistants, one attempt per question in a fresh chat, no follow-ups,
MNE-Python 1.13. Discussion: https://github.com/mne-tools/mne-python/issues/14428

**Status:** the 13 automatically checked results are reproducible with `run.py`. The 11
hand-graded results are **provisional suggestions** that have not yet been reviewed by
anyone independent; see [GRADING.md](GRADING.md) to help.

## Who did what

| Step | Done by |
|---|---|
| Choosing forum threads and writing questions, checks and criteria | the author, with help from Claude Code |
| Collecting replies from each assistant (web interfaces) | the author |
| Automatic scoring (13 questions) | `run.py`: runs each reply's code on synthetic data |
| Hand grading (11 questions) | suggested by Claude Code, not yet independently reviewed |

Claude (Sonnet 5.5) is one of the assistants tested, and Claude Code is also a Claude
model, so the hand grades and the design of the checks could favour Claude. The decisions
below are listed so they can be checked.

## Decisions that changed scores

- **q009 check:** the synthetic data were given a measurement date, as in real recordings.
  This turned two replies (Gemini, ChatGPT, earlier runs) from PASS to FAIL and left
  Claude's PASS; their code shifts annotations whenever a date is set. Verified with a
  separate script, but worth re-checking.
- **q001 check:** one system-bit change now starts in the middle of a trigger pulse, so
  masking *after* `find_events` fails. This affected one ChatGPT code block.
- **Code selection:** when a reply contained several alternative code blocks, the block the
  reply itself recommends was run; ChatGPT code that lost its line breaks when copied was
  re-formatted without changing any statement. Each case is listed in
  `answers/<assistant>/README.md`.
- **q011 and q023:** graded by hand / on a reduced criterion because of question-design
  problems ([NOTES.md](NOTES.md)).
- **Strict vs lenient grading** (definition in GRADING.md): changes 3 grades.

## Shared failure patterns

These are the main findings; they do not depend on which assistant "wins".

1. **The MNE 1.13 montage rename** (`standard_1020` / `standard_1005`) accounts for 7 of the
   23 failures. All three fail q024 even though the prompt says "MNE-Python 1.13", and all
   three recommend `standard_1005` for fsaverage (q019).
2. **Recent topics are harder.** Pass rate on 2024-26 vs 2021-23 forum topics: 67% vs 82%
   (Gemini), 78% vs 82% (Claude), 33% vs 73% (ChatGPT). Small samples; a trend only.
3. **Known forum pitfalls still appear:** reusing the original events after resampling
   (2 of 3, q007) and fitting ICA on unfiltered data (1 of 3, q003).
4. **No assistant answered q016** (`mean_flip` on all-positive dSPM estimates, a 2025 topic).
5. **Non-existent or misplaced API**, checked against the MNE source:
   `Raw.set_eeg_reference(copy=...)`, `raw.get_eeg_reference()`, `uint_cast` passed to
   `read_raw_bdf`.
6. **Confident wrong claims about MNE behaviour:** `adjacency=None` described as fully
   connected, BAD-annotation matching described as case-sensitive, `apply_inverse_raw`
   said to skip BAD spans.

Doc pages these point to: [doc_findings.md](doc_findings.md).

## Scores

The differences between assistants are small compared with the run-to-run variation seen
in this pilot (see Limitations), so **the scores should not be read as a ranking**.

| Group | Gemini | Claude | ChatGPT |
|---|---|---|---|
| Recent forum topics, 2024-26 (9) | 6 | 7 | 3 |
| Older forum topics, 2021-23 (11) | 9 | 9 | 8 |
| Known pitfalls from docs/GitHub (3) | 2 | 2 | 3 |
| Version awareness, MNE 1.13 (1) | 0 | 0 | 0 |
| **Total, strict rule (24)** | **17** | **18** | **14** |
| Total, lenient rule (24) | 18 | 18 | 16 |

Groups: recent = q002, q003, q011, q012, q016-q020; older = q006-q010, q013-q015,
q021-q023; pitfalls = q001, q004, q005; version = q024.

| Assistant | Model | Plan |
|---|---|---|
| Gemini (web) | Gemini Flash Lite | free, not logged in |
| Claude (claude.ai) | Claude Sonnet 5.5 | free account |
| ChatGPT (web) | not shown in the free UI | free, logged in, Temporary Chat, Think off |

## Per question

R = automatic (code executed and checked), M = hand-graded (provisional).
⚠ = borderline; the grade depends on strict vs lenient grading or on a judgement call.

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
was graded by hand on the concept; q023 was graded on its generic criterion only.

## Borderline cases

- **Gemini q005, Claude q005:** correct masking code, but neither says that the Status
  channel is not converted to annotations (criterion 1). Claude also places `uint_cast`
  on `read_raw_bdf` (it belongs to `find_events`).
- **Claude q017 vs ChatGPT q017 (judgement call):** both contain a factual error. Claude's
  (BAD matching "case-sensitive") was treated as a side detail and passed; ChatGPT's
  (`apply_inverse_raw` skips BAD spans) concerns the thing asked and failed. This call
  favours Claude and should be checked independently.
- **ChatGPT q018:** recommends rejecting only within the window of interest; leakage
  appears only as a caveat.
- **ChatGPT q020:** says MNE's default is FIR, but its table lists Butterworth/IIR as what
  to report.
- **ChatGPT q021:** opens with "all channels are spatially connected", then correctly
  explains the index-order lattice.

One-line reasons for every hand grade are in `answers/<assistant>/manual_grades.md`, and
the raw replies are in `answers/<assistant>/<id>.md`.

## Limitations

- **One run per question.** Redoing q001-q010 in fresh chats changed five results compared
  with an earlier shared-chat run (kept in git history), so single runs are noisy.
- **Small question set**, and "recent" is defined by forum post date, not by any model's
  training cutoff.
- **Hand grades are not yet independent** (see "Who did what").
- **Free tiers only**, and the model version is not always visible (ChatGPT).
