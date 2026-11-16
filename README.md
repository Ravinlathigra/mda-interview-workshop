# Bridging the Gap: MDA Technical Interview Workshop v2

A two-hour interactive workshop for MDA students at Western University. Version 2 adds
a hands-on SQL debugging interview to the existing explanation, project-story, and mock
interview exercises.

**Presenter:** Ravin Lathigra, MDA alumnus and Staff Data Engineer at Shopify

**Original workshop date:** February 23, 2026

Ravin's employer and role provide professional context only. This independent educational
workshop is not an official Shopify interview, dataset, process, or endorsement.

## What's new in v2

The Marimo and DuckDB lab asks candidates to investigate two queries that run and return
plausible but incorrect results:

1. A shop-dimension join inflates session counts because the shop key is not unique.
2. Date truncation turns midnight crossings into "one day" even when little time elapsed.

Candidates may use AI. The evaluation focuses on metric clarification, hypothesis-driven
debugging, communication, and independent validation. All data is synthetic.

## Run the lab

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
marimo edit lab/app.py
```

Then open the local URL Marimo prints.

## Run the checks

```bash
python -m pytest
marimo check lab/app.py
```

The tests pin the intended failure modes and corrected results.

## Workshop files

### `index.html`: presenter slide deck

The self-contained HTML deck retains the workshop's original visual style and interactive
timers. Version 2 adds the debugging lab to the agenda and presentation flow.

Navigation:

- Arrow keys or spacebar advance slides.
- Mock interview slides use arrow keys to step through each conversation.
- Timeline dots jump to any slide.
- The bottom bar shows progress and slide count.

### `workshop.html`: participant reference app

The self-contained tabbed app includes the workshop frameworks, stream-specific practice
questions, mock interview bank, resources, and a new Debugging Lab tab.

### `lab/`: candidate workspace

- `app.py` is the interactive Marimo notebook.
- `database.py` loads deterministic data into an in-memory DuckDB database.
- `data/` contains the fictional shop and session CSVs.
- `query_utils.py` keeps notebook output lightweight and dependency-free.

### `guides/`: delivery and evaluation

- `candidate-guide.md` explains setup, expectations, and the investigation loop.
- `interviewer-guide.md` includes prompts, reference outcomes, and a behavioral rubric.
- `facilitator-runbook.md` fits the lab into a two-hour workshop and includes recovery steps.

### `solutions/` and `tests/`: protected reference material

The SQL solutions are separate from the candidate notebook. Tests verify the duplicate-key
inflation, the calendar-boundary error, and the expected corrected metrics.

## Static materials

The two HTML files have no build step. Open them directly in a browser:

```bash
open index.html
open workshop.html
```

Google Fonts load from a CDN when internet access is available. The workshop content and
interactions remain in the local files.
