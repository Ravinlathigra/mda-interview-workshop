# Bridging the Gap: MDA Technical Interview Workshop v2

A two-hour interactive workshop for MDA students at Western University. Version 2 adds
a hands-on SQL debugging interview to the existing explanation, project-story, and mock
interview exercises.

**Presenter:** Ravin Lathigra, MDA alumnus and Staff Data Engineer at Shopify

**Presentation term:** Winter 2026

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

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) once, then run
these commands from the repository root. uv manages Python 3.12 and the environment;
no manual virtual-environment activation is needed. Commit `uv.lock` so everyone
uses the same resolved dependency versions, including CI.

```bash
uv sync --locked
uv run --locked marimo run lab/app.py --host 127.0.0.1 --port 2718
```

Then open http://localhost:2718. Use the SQL editors and Run buttons to investigate;
the app displays all result rows (up to 200), including diagnostic queries.
Download your handoff before refreshing or closing the tab. Queries and notes live
in the current browser session. To edit the notebook source, use
`uv run --locked marimo edit lab/app.py`.

Each case includes a collapsed **Reveal solution** section with the explanation,
editable reference SQL, expected results, and its own **Run solution** button.
Reveal it during the debrief or when reviewing independently. Running a solution
does not replace your candidate query or notes. The handoff exports your candidate
work; copy any reference experiments you want to retain into your notes.

## Run the checks

```bash
uv run --locked pytest
uv run --locked marimo check --strict lab/app.py
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

### `solutions/` and `tests/`: facilitator reference material

The notebook loads reference SQL directly from `solutions/`, so the runnable answers
and tested queries stay in sync. They are available in collapsed sections in each case;
participants can reveal them for the debrief or self-study. Tests verify duplicate-key
inflation, status changes, time boundaries, and query-runner behavior.

## Static materials

The two HTML files have no build step. Open them directly in a browser:

```bash
open index.html
open workshop.html
```

Google Fonts load from a CDN when internet access is available. The workshop content and
interactions remain in the local files.
