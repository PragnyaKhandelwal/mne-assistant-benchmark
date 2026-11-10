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
