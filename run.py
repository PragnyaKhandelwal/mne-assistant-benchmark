"""Score AI-assistant answers against the MNE question set.

Usage
-----
python run.py --prompts              # print every prompt, to paste into an assistant
python run.py answers/<name>         # score the answers saved in answers/<name>/<id>.md

Each answer file is the assistant's reply, pasted as-is. For "runnable" questions
the Python code blocks in the reply are executed in a fresh subprocess against the
question's synthetic data, and ``check.py`` decides pass/fail. "manual" questions
print their grading criteria for a human to judge.
"""

import json
import os
import re
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).parent
QUESTIONS = ROOT / "questions"
TIMEOUT = 300  # seconds per answer


def load_questions():
    out = []
    for qdir in sorted(p for p in QUESTIONS.iterdir() if p.is_dir()):
        with open(qdir / "question.toml", "rb") as fid:
            meta = tomllib.load(fid)
        meta["dir"] = qdir
        out.append(meta)
    return out


def extract_code(text):
    blocks = re.findall(r"```([^\n]*)\n(.*?)```", text, flags=re.S)
    keep = ("", "python", "py", "python3")
    return "\n\n".join(code for lang, code in blocks if lang.strip().lower() in keep)


def run_one(qdir, answer_file):
    """Executed in the child process: setup, run the answer code, check."""
    sys.path.insert(0, str(qdir))
    import check

    ns = check.setup()
    # <id>.code.py, if present, holds the code selected from the reply (see README)
    override = Path(answer_file).with_suffix(".code.py")
    if override.exists():
        code = override.read_text(encoding="utf-8")
    else:
        code = extract_code(Path(answer_file).read_text(encoding="utf-8"))
    if not code.strip():
        return False, "no Python code block found in the answer"
    try:
        exec(compile(code, "<answer>", "exec"), ns)
    except Exception as exc:
        return False, f"answer code raised {type(exc).__name__}: {str(exc)[:160]}"
    return check.check(ns)


def score(answers_dir):
    rows = []
    for q in load_questions():
        answer = answers_dir / f"{q['id']}.md"
        if not answer.exists():
            rows.append((q["id"], "missing", ""))
            continue
        if q["kind"] == "manual":
            rows.append((q["id"], "manual", "grade by hand, see criteria below"))
            continue
        proc = subprocess.run(
            [sys.executable, __file__, "--_one", str(q["dir"]), str(answer)],
            capture_output=True,
            text=True,
            timeout=TIMEOUT,
            env={**os.environ, "MPLBACKEND": "agg", "MNE_BROWSER_BACKEND": "matplotlib"},
        )
        try:
            passed, msg = json.loads(proc.stdout.strip().splitlines()[-1])
        except (IndexError, ValueError):
            passed, msg = False, f"runner crashed: {proc.stderr.strip()[-300:]}"
        rows.append((q["id"], "PASS" if passed else "FAIL", msg))

    print(f"\nResults for {answers_dir}\n")
    print("| question | result | note |\n|---|---|---|")
    for row in rows:
        print("| " + " | ".join(row) + " |")
    for q in load_questions():
        if q["kind"] == "manual":
            print(f"\n## {q['id']} criteria\n{q['criteria'].strip()}")


def main():
    args = sys.argv[1:]
    if args[:1] == ["--_one"]:
        print(json.dumps(run_one(Path(args[1]), args[2])))
    elif args[:1] == ["--prompts"]:
        for q in load_questions():
            print(f"===== {q['id']}: {q['title']}\n{q['prompt'].strip()}\n")
    elif len(args) == 1:
        score(Path(args[0]))
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
