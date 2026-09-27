# demo-repo

A tiny sample repo built for one purpose: give Claude Code a task with real
shape (a multi-file search, several edits, then a test run) so a resulting
OpenTelemetry trace has something interesting in it.

## The setup

- `formatting/old_format.py` — the deprecated formatter (no thousands
  separators, no decimal rounding). Four files still import it.
- `formatting/new_format.py` — the replacement, already written and correct.
- `app/invoice.py`, `app/report.py`, `app/dashboard.py`, `app/email_receipt.py`
  — each imports `formatting.old_format`.
- `tests/` — six tests, written against the **new** formatter's output.
  Right now, with the old formatter still wired in, all six fail.

Verify the starting state yourself:
```bash
pip install -r requirements.txt
python3 -m pytest -q
# 6 failed
```

## The demo prompt

Give Claude Code this, in a session with telemetry/tracing turned on:

> Find every place in this repo that imports the old formatting helper,
> switch it to the new one, then run the test suite to confirm nothing broke.

Expected behavior: Claude searches for `old_format` usages (Grep/Glob calls),
reads and edits the four `app/` files (Read + Edit calls), then runs
`python3 -m pytest` (a Bash call) — which should now show `6 passed`.

That Bash test run is, in most environments, the single slowest span in the
resulting trace — which is the moment to point at during the "what you
couldn't see before" beat: the LLM responses are fast, the bottleneck is the
test suite.

## Resetting between takes

If you want to record more than once, reset the repo to its broken starting
state between takes:
```bash
git checkout -- app/
```
