# Candidate guide: SQL debugging lab

## What this exercise evaluates

The interviewer cares about how you investigate a plausible result that may be wrong.
You do not need to know DuckDB or Marimo in advance. Standard SQL reasoning is enough.

You will work through two cases using fictional commerce data:

- an unexpectedly high session count for active shops
- a report claiming that 6 of 8 sessions lasted at least one day

AI tools are allowed. You may use them to recall syntax, generate a diagnostic query,
or challenge an assumption. You must be able to explain and validate anything you keep.

## Start the lab

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) first.
From the repository root, run the commands below. uv installs the pinned Python and
dependencies; you do not need to activate a virtual environment.

```bash
uv sync --locked
uv run --locked marimo run lab/app.py --host 127.0.0.1 --port 2718
```

Open http://localhost:2718. Edit a query and press its Run button. Results correspond
to the last submitted query, not any unfinished edits. Diagnostic queries display
all rows up to a 200-row preview; an empty result is valid. Run one `SELECT`, `WITH`,
`DESCRIBE`, or `EXPLAIN` statement at a time. The exercise tables cannot be edited
through the query boxes.

Notes survive query runs. Before refreshing or closing, use **Download my handoff**
to save your last submitted queries and notes. Submit your final edits first.

## Metric-owner brief and data dictionary

Ask for clarification before choosing a correction. Use these agreed definitions:

- Case 1 counts sessions belonging to shops whose **latest available snapshot** says
  active. It does not ask whether a shop was active when the session began.
- `shops`: `shop_id`, `shop_name`, `plan`, `status`, `snapshot_at`. Snapshot timestamps
  are unique within each shop. Establish the actual table grain yourself.
- `sessions`: `session_id`, `shop_id`, `started_at`, `ended_at`, `channel`.
  Expected grain is one row per session. All timestamps represent UTC and are stored
  without timezone offsets. End times are present and never precede start times.
- Case 2 includes all eight sessions, including inactive shops. “At least one day”
  means at least **24 elapsed hours**, with equality included.
- The unusually long sessions deliberately test metric semantics. They do not model
  Shopify's session timeout policy or real shop activity.

If a real dataset violated these assumptions, agree on a missing-data or tie-breaking
policy before reporting a metric. Optional: build a small `VALUES` CTE to test boundaries.

## A useful investigation loop

1. Restate the metric in plain language. Ask what one row should represent.
2. Run the provided query and record the current answer.
3. Inspect the source grains, key uniqueness, nulls, and boundary values.
4. Reduce the failure to the smallest query or row that proves the diagnosis.
5. Correct the query. State why the change matches the metric definition.
6. Validate with an independent check and name a regression test.

Narrate your reasoning. If you are uncertain, say what you would test next. A silent,
correct query provides less evidence than a structured investigation.

## What to present

For each case, prepare a two-minute handoff:

- your metric definition and expected grain
- the failed assumption and evidence
- the corrected result and query
- an independent validation check
- any ambiguity you would resolve with the metric owner

## Reveal and run the solutions

Each case has a **Reveal solution** section below the investigation notes. It starts
collapsed so you can investigate first. Open it during the debrief, or whenever you
want the answer during self-study. Read the explanation, then click **Run case 1
solution** or **Run case 2 solution**. You can edit and rerun the reference SQL in
that section without replacing your own query or notes.

Compare the expected results with your evidence and try the suggested validation
checks. The handoff download contains your candidate queries and notes; copy any
reference experiments you want to keep into your notes before downloading.

## Data notice

All shops, sessions, names, timestamps, and results in this repository are synthetic.
The scenario borrows common commerce vocabulary for teaching. It does not use Shopify
data and does not represent or imply Shopify endorsement.
