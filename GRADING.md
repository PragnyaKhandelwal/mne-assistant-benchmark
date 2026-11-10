# Help wanted: independent grading

The 11 hand-graded questions are the least objective part of this pilot. So far they
have only *suggested* grades, drafted with help from Claude Code. Claude is also one of
the assistants tested, so independent grades from people who know MNE are the most
useful contribution right now.

## How to grade

1. Open [grading/blind_sheet.md](grading/blind_sheet.md). Each question shows the prompt,
   the grading criteria, and three replies labelled A, B and C. Labels are shuffled per
   question and assistant names are hidden.
2. For each reply, write PASS or FAIL and one line of reasoning. If you think the
   criteria themselves are wrong or incomplete, say so; that matters as much as the grades.
3. Please grade before looking at `answers/*/manual_grades.md`, which would reveal both
   the assistants and the suggested grades.
4. Send your grades as an issue in this repository (or a comment on
   mne-tools/mne-python#14428). Partial grading (even one question) is welcome.

## Notes on blinding

- Citation widgets and links that named an assistant were removed; nothing else in the
  replies was changed.
- Some stylistic cues remain (for example, code that lost its line breaks when copied
  from one web interface). Please grade on content.
- The A/B/C mapping is kept privately and will be published together with the results
  of independent grading.

## Grading rule used for the suggested grades

A reply that makes a wrong, definite claim about the thing asked fails, even if it also
gives the right answer elsewhere ("strict"). If you prefer grading on the main
recommendation only ("lenient"), say which rule you used.
