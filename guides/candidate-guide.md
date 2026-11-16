# Candidate guide: SQL debugging lab

## What this exercise evaluates

The interviewer cares about how you investigate a plausible result that may be wrong.
You do not need to know DuckDB or Marimo in advance. Standard SQL reasoning is enough.

You will work through two cases using fictional commerce data:

- a session count that grows after joining to a shop dimension
- a duration metric that confuses calendar days with elapsed time

AI tools are allowed. You may use them to recall syntax, generate a diagnostic query,
or challenge an assumption. You must be able to explain and validate anything you keep.

## Start the lab

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
marimo edit lab/app.py
```

Your browser will open the notebook. Work only in the query editors and note fields.
You do not need to change the source files.

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

Do not open the `solutions/` folder until the facilitator begins the debrief.

## Data notice

All shops, sessions, names, timestamps, and results in this repository are synthetic.
The scenario borrows common commerce vocabulary for teaching. It does not use Shopify
data and does not represent or imply Shopify endorsement.

