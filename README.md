# Claude Code + OpenObserve Demo

A tiny sample repo built for one purpose: give Claude Code a task with real shape — a multi-file search, several edits, then a test run — so a resulting OpenTelemetry trace has something interesting in it.

## 1. Set up OpenObserve

This demo uses **self-hosted OpenObserve** to collect and visualize the telemetry generated while Claude Code works on the repository.

Self-hosted OpenObserve is useful when you need:

* Full control over your data and infrastructure
* Custom configurations or integrations
* On-premises deployment requirements

For this demo, a single-node installation is sufficient.

### Install OpenObserve

Download the appropriate binary from the [OpenObserve downloads page](https://openobserve.ai/downloads), then make it executable:

```bash
chmod +x openobserve
```

Run OpenObserve with the root credentials:

```bash
ZO_ROOT_USER_EMAIL="root@example.com" \
ZO_ROOT_USER_PASSWORD="Complexpass#123" \
./openobserve
```

OpenObserve should now be available at:

```text
http://localhost:5080
```

Open the URL in your browser and log in with:

```text
Email: root@example.com
Password: Complexpass#123
```

> **Note:** The credentials above are only for this local demo. For an actual deployment, use your own credentials and follow the OpenObserve deployment documentation.

> **Important:** These instructions are for a single-node installation. For production high-availability setups, refer to the [OpenObserve HA deployment guide](https://openobserve.ai/docs/administration/deployment/ha-deployment/).

You'll need to set `ZO_ROOT_USER_EMAIL` and `ZO_ROOT_USER_PASSWORD` on the first startup. They are not required for subsequent runs.

---

## 2. Configure Claude Code telemetry

Once OpenObserve is running on `http://localhost:5080`, configure Claude Code to send its OpenTelemetry data to OpenObserve.

Run the following commands in the same terminal session where you will run Claude Code:

```bash
export OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:5080/api/default
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=Basic cm9vdEBleGFtcGxlLmNvbTpDb21wbGV4cGFzczEyMz=,stream-name=claude_code"

export OTEL_METRICS_EXPORTER=otlp
export OTEL_LOGS_EXPORTER=otlp
export OTEL_TRACES_EXPORTER=otlp

export CLAUDE_CODE_ENABLE_TELEMETRY=1
export CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1

export OTEL_LOG_TOOL_DETAILS=1
export OTEL_LOG_TOOL_CONTENT=1
export OTEL_LOG_USER_PROMPTS=1
```

These environment variables configure Claude Code to:

* Enable telemetry collection.
* Export **traces, logs, and metrics** using OTLP.
* Send the telemetry to the local OpenObserve instance.
* Include Claude Code tool details and tool content in the telemetry.
* Include user prompts in the telemetry.
* Send the data to the `claude_code` stream in OpenObserve.

After setting these variables, start Claude Code from the same terminal:

```bash
claude
```

Claude Code will now export telemetry while it works on the demo repository.

> **Note:** The `Authorization` header above uses the credentials configured for this local demo. For any shared or production setup, replace it with credentials appropriate for your OpenObserve instance and avoid committing credentials to the repository.

---

## 3. Set up the demo repository

The repository contains a deliberately broken formatting setup so Claude Code has a real multi-file task to work through.

### Repository structure

* `formatting/old_format.py` — the deprecated formatter with no thousands separators and no decimal rounding.
* `formatting/new_format.py` — the replacement formatter, already written and correct.
* `app/invoice.py`
* `app/report.py`
* `app/dashboard.py`
* `app/email_receipt.py` — each imports `formatting.old_format`.
* `tests/` — six tests written against the new formatter's output.

The application is still wired to the old formatter, so the tests should initially fail.

Verify the starting state:

```bash
pip install -r requirements.txt
python3 -m pytest -q
```

Expected result:

```text
6 failed
```

---

## 4. The demo prompt

Run Claude Code in a session with telemetry/tracing enabled and give it this prompt:

> Find every place in this repo that imports the old formatting helper, switch it to the new one, then run the test suite to confirm nothing broke.

Expected behavior:

1. Claude searches for `old_format` usages using Grep/Glob.
2. It reads the relevant files.
3. It edits the four files in `app/`.
4. It runs the test suite using Bash.
5. The tests should finish with:

```text
6 passed
```

The resulting OpenTelemetry trace captures this workflow as a sequence of tool calls and spans.

The Bash test run is expected to be one of the slower spans in the trace. That's the useful moment to highlight during the demo: the LLM responses themselves are relatively fast, while the actual test execution is where time is spent.

---

## 5. What to look for in OpenObserve

After Claude Code completes the task, open OpenObserve and inspect the resulting trace.

You should be able to follow the workflow from the initial Claude Code interaction through:

```text
Claude Code
   ↓
Search / Grep
   ↓
Read files
   ↓
Edit files
   ↓
Run tests
   ↓
6 tests passed
```

This is the key part of the demo: instead of only seeing Claude Code perform the task, the trace gives you visibility into **what Claude did, which tools it used, and where time was spent**.

---

## 6. Resetting between takes

If you want to record the demo more than once, reset the application files to their broken starting state:

```bash
git checkout -- app/
```

Then verify that the tests are failing again:

```bash
python3 -m pytest -q
```

You should once again see:

```text
6 failed
```

You can then run the same Claude Code prompt and inspect the new trace in OpenObserve.
