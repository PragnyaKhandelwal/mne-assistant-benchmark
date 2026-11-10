# MNE assistant benchmark (experimental)

A small set of MNE-Python questions with checkable answers, for measuring how
often AI assistants get MNE analysis questions right, and whether
reviewed "skill" files improve them.

Discussion and context: https://github.com/mne-tools/mne-python/issues/14428

## How it works

Each question lives in `questions/<id>/`:

- `question.toml`: the prompt, sources, the MNE version it was written for,
  and grading criteria.
- `check.py` (runnable questions only): `setup()` builds small synthetic data
  (no dataset download needed) and `check(ns)` decides pass/fail after the
  answer's code has run.

Questions are either **runnable** (the code in the answer is executed and
checked automatically) or **manual** (a person grades the answer against the
criteria).

## Usage

Requires Python 3.11+ and MNE-Python (plus scikit-learn for the ICA question).

```bash
python run.py --prompts              # print prompts to paste into an assistant
python run.py answers/<name>         # score answers saved as answers/<name>/<id>.md
```

Paste each assistant reply unchanged into `answers/<name>/<id>.md`. Python
code blocks are extracted and run in a fresh subprocess. The runner never
calls a model API, so any assistant (hosted or local) can be tested.

### Selecting the code to run

Replies often contain several code blocks: the answer, optional extras, alternatives,
or later steps. Running all of them in sequence can break a correct answer. When that
happens, save the reply unchanged as `<id>.md` and put the code the reply itself
presents as its main or recommended answer in `<id>.code.py` next to it; the runner
uses that file instead. Never change statements inside the selected code (restoring
line breaks lost when copying is fine), and note each selection in that assistant's
`README.md`.

`answers/reference/` holds correct answers and `answers/naive/` common
mistakes; together they check that the checks themselves work.

## Status

Pilot. Questions are drawn from MNE documentation, GitHub discussions and the
MNE Forum, and each one should be reviewed by someone familiar with the topic
before results are reported. Doc pages that confuse assistants are tracked
as a by-product, so the docs can be improved for human readers too.

## License

BSD-3-Clause, see `LICENSE`.
