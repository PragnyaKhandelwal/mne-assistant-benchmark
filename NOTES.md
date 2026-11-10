# Pilot notes: issues found in the questions themselves

Fixes made during the pilot, and open issues for the next version. Kept so the
write-up can report them honestly.

- **q001 (fixed):** the synthetic status channel never changed system bits during a
  trigger, so masking *after* `find_events` passed by luck. One system-bit change now
  starts mid-trigger, as in real recordings.
- **q009 (fixed):** the test data had no measurement date. Whether `first_samp` must be
  subtracted depends on it, so the check rewarded code that breaks on real files. The data
  now carry a measurement date.
- **q011 (open):** the prompt does not name the noisy channel, so every assistant used a
  placeholder (`'EEG 0XX'`, example names, or a placeholder file path) and crashed. All
  three had the right concept. Graded by hand for this pilot; for the next version,
  either name the channel in the prompt or make the question manual.
- **Montage rename (finding, not a bug):** MNE 1.13 renamed `standard_1005/1020`. Answers
  that add a montage "for completeness" crash even when their main idea is right
  (Gemini/Claude q010, ChatGPT q006). Recorded as FAIL with a note.
- **q023 (open):** the prompt never says MNE, so the criterion about MNE's default
  estimators (Welch for raw, multitaper for epochs) can't fairly be expected. Graded on the
  generic criterion (frequency resolution ~ 1/T) for this pilot; for the next version, name
  MNE and the functions used in the prompt.
- **Self-contradiction rule (grading):** a reply that states a wrong answer to the asked
  question as a definitive claim fails, even if it also states the right one elsewhere
  (applied to ChatGPT q017 and q021).
- **Runner (fixed):** code blocks nested in markdown lists are indented; the runner now
  dedents them (Claude q024 had failed with an IndentationError before this).
