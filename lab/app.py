import marimo

__generated_with = "0.25.2"
app = marimo.App(width="full")


@app.cell
def _():
    from pathlib import Path
    import sys

    import marimo as mo

    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    from lab.database import (
        BROKEN_DURATION_QUERY,
        BROKEN_SESSION_COUNT_QUERY,
        create_connection,
    )
    from lab.query_utils import execute_query

    return (
        BROKEN_DURATION_QUERY,
        BROKEN_SESSION_COUNT_QUERY,
        create_connection,
        execute_query,
        mo,
    )


@app.cell
def _(mo):
    mo.Html(
        """
        <style>
          :root {
            --lab-bg: #07090d;
            --lab-surface: #10141b;
            --lab-surface-2: #151a23;
            --lab-border: #29313d;
            --lab-text: #f3f5f7;
            --lab-muted: #9aa4b2;
            --lab-purple: #a78bfa;
            --lab-blue: #60a5fa;
            --lab-green: #34d399;
            --lab-orange: #fb923c;
          }

          body, html {
            background:
              radial-gradient(circle at 15% 0%, rgba(96,165,250,.12), transparent 32rem),
              radial-gradient(circle at 90% 12%, rgba(167,139,250,.12), transparent 30rem),
              var(--lab-bg) !important;
            color: var(--lab-text) !important;
          }

          #App {
            --background: #07090d;
            --foreground: #f3f5f7;
            --card: #10141b;
            --card-foreground: #f3f5f7;
            --border: #29313d;
            --input: #29313d;
            --muted: #151a23;
            --muted-foreground: #9aa4b2;
            --accent: #1b2430;
            --accent-foreground: #bfdbfe;
            --popover: #111720;
            --popover-foreground: #f3f5f7;
            --cm-background: #090c11;
            background: transparent !important;
            color: var(--lab-text) !important;
          }

          .marimo {
            max-width: 1180px !important;
            margin: 0 auto !important;
            padding: 24px 28px 96px !important;
          }

          .prose, .prose p, .prose li, .prose td, .prose th {
            color: var(--lab-text) !important;
          }

          .prose h1, .prose h2, .prose h3 {
            color: var(--lab-text) !important;
            letter-spacing: -0.025em;
          }

          .prose code {
            color: #c4b5fd !important;
            background: rgba(167,139,250,.1) !important;
          }

          .lab-hero {
            position: relative;
            overflow: hidden;
            padding: clamp(30px, 6vw, 64px);
            border: 1px solid rgba(167,139,250,.28);
            border-radius: 28px;
            background:
              linear-gradient(135deg, rgba(96,165,250,.14), rgba(167,139,250,.13) 52%, rgba(251,146,60,.08)),
              #0d1118;
            box-shadow: 0 28px 90px rgba(0,0,0,.35);
          }

          .lab-hero:after {
            content: "";
            position: absolute;
            width: 280px;
            height: 280px;
            right: -90px;
            top: -120px;
            border-radius: 999px;
            background: rgba(167,139,250,.18);
            filter: blur(40px);
          }

          .lab-kicker, .case-kicker {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-size: 12px;
            line-height: 1;
            font-weight: 750;
            letter-spacing: .14em;
            text-transform: uppercase;
          }

          .lab-kicker { color: #c4b5fd; }
          .case-kicker { color: var(--lab-blue); }
          .case-kicker.orange { color: var(--lab-orange); }

          .lab-hero h1 {
            position: relative;
            z-index: 1;
            max-width: 820px;
            margin: 18px 0 14px;
            color: var(--lab-text);
            font-size: clamp(42px, 7vw, 76px);
            line-height: .98;
            letter-spacing: -.055em;
          }

          .lab-hero p {
            position: relative;
            z-index: 1;
            max-width: 760px;
            margin: 0;
            color: #c3cad4;
            font-size: clamp(17px, 2vw, 21px);
            line-height: 1.55;
          }

          .lab-badges {
            position: relative;
            z-index: 1;
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 28px;
          }

          .lab-badge {
            padding: 8px 12px;
            border: 1px solid var(--lab-border);
            border-radius: 999px;
            color: #cbd2dc;
            background: rgba(7,9,13,.38);
            font-size: 13px;
            font-weight: 650;
          }

          .section-head {
            margin: 44px 0 18px;
          }

          .section-head h2, .case-head h2 {
            margin: 8px 0 6px;
            color: var(--lab-text);
            font-size: clamp(28px, 4vw, 40px);
            line-height: 1.1;
            letter-spacing: -.035em;
          }

          .section-head p, .case-head p {
            margin: 0;
            max-width: 780px;
            color: var(--lab-muted);
            font-size: 16px;
            line-height: 1.55;
          }

          .case-head { margin-bottom: 8px; }

          .result-label {
            margin: 4px 0 2px;
            color: var(--lab-muted);
            font-size: 12px;
            font-weight: 750;
            letter-spacing: .12em;
            text-transform: uppercase;
          }

          .handoff-grid {
            display: grid;
            grid-template-columns: repeat(5, minmax(0, 1fr));
            gap: 12px;
            margin-top: 20px;
          }

          .handoff-item {
            padding: 16px;
            border: 1px solid var(--lab-border);
            border-radius: 16px;
            background: rgba(16,20,27,.76);
          }

          .handoff-item span {
            display: block;
            margin-bottom: 6px;
            color: var(--lab-purple);
            font-size: 12px;
            font-weight: 800;
            letter-spacing: .1em;
          }

          .handoff-item strong {
            color: var(--lab-text);
            font-size: 14px;
          }

          .lab-footer {
            margin-top: 38px;
            padding: 18px 2px;
            border-top: 1px solid var(--lab-border);
            color: #707b8b;
            font-size: 13px;
          }

          .cm-editor {
            border: 1px solid #344050 !important;
            border-radius: 14px !important;
            background: #090c11 !important;
            box-shadow: inset 0 1px 0 rgba(255,255,255,.03);
          }

          [data-testid="marimo-table"] {
            border: 1px solid var(--lab-border) !important;
            border-radius: 14px !important;
            overflow: hidden;
          }

          .marimo table tr {
            background: #10141b !important;
            border-color: #29313d !important;
          }

          .marimo table tr:hover {
            background: #171e29 !important;
          }

          .marimo table th {
            background: #0b0f15 !important;
            color: #9aa4b2 !important;
            border-color: #29313d !important;
          }

          .marimo table td {
            color: #dbe1e9 !important;
            border-color: #29313d !important;
          }

          .marimo [role="tab"] {
            background: #141a23 !important;
            color: #9aa4b2 !important;
            border-color: #29313d !important;
          }

          .marimo [role="tab"][data-state="active"] {
            background: #253144 !important;
            color: #f3f5f7 !important;
          }

          .marimo .bg-card {
            background: #151a23 !important;
            color: #f3f5f7 !important;
            border-color: #344050 !important;
          }

          .marimo .bg-card * {
            color: #f3f5f7 !important;
          }

          textarea {
            border-color: #344050 !important;
            border-radius: 14px !important;
            background: #090c11 !important;
            color: var(--lab-text) !important;
          }

          @media (max-width: 820px) {
            .marimo { padding: 14px 14px 80px !important; }
            .handoff-grid { grid-template-columns: 1fr 1fr; }
            .lab-hero { border-radius: 22px; }
          }
        </style>
        """
    )
    return


@app.cell
def _(mo):
    mo.Html(
        """
        <section class="lab-hero">
          <div class="lab-kicker">MDA technical interview workshop / practical lab</div>
          <h1>Debug the metric,<br>not just the query.</h1>
          <p>
            Two production-style SQL queries run successfully and return believable
            answers. Your job is to decide whether those answers deserve trust.
          </p>
          <div class="lab-badges">
            <span class="lab-badge">DuckDB SQL</span>
            <span class="lab-badge">Synthetic commerce data</span>
            <span class="lab-badge">AI allowed</span>
            <span class="lab-badge">Evidence required</span>
          </div>
        </section>
        """
    )
    return


@app.cell
def _(create_connection):
    connection = create_connection()
    return (connection,)


@app.cell
def _(connection, execute_query, mo):
    shop_columns, shop_rows = execute_query(
        connection,
        "SELECT * FROM shops ORDER BY shop_id, snapshot_at",
    )
    session_columns, session_rows = execute_query(
        connection,
        "SELECT * FROM sessions ORDER BY session_id",
    )

    def records(columns, rows):
        return [dict(zip(columns, row, strict=True)) for row in rows]

    shops_table = mo.ui.table(
        records(shop_columns, shop_rows),
        selection=None,
        pagination=False,
        show_column_summaries=False,
        show_data_types=False,
        show_download=False,
        show_search=False,
        max_height=330,
    )
    sessions_table = mo.ui.table(
        records(session_columns, session_rows),
        selection=None,
        pagination=False,
        show_column_summaries=False,
        show_data_types=False,
        show_download=False,
        show_search=False,
        max_height=390,
    )

    data_section = mo.vstack(
        [
            mo.Html(
                """
                <div class="section-head">
                  <div class="case-kicker">Dataset / inspect before assuming</div>
                  <h2>Two small tables, one hidden trap</h2>
                  <p>
                    <code>shops</code> is a dimension-style extract and
                    <code>sessions</code> should contain one row per session.
                    Treat both claims as hypotheses until the data supports them.
                  </p>
                </div>
                """
            ),
            mo.ui.tabs(
                {
                    "Shops (6 rows)": shops_table,
                    "Sessions (8 rows)": sessions_table,
                }
            ),
        ],
        gap=1,
    )
    mo.style(
        data_section,
        {
            "background": "rgba(16, 20, 27, .88)",
            "border": "1px solid #29313d",
            "border-radius": "24px",
            "padding": "clamp(20px, 3vw, 32px)",
            "margin-top": "26px",
            "box-shadow": "0 18px 55px rgba(0,0,0,.22)",
        },
    )
    return


@app.cell
def _(BROKEN_SESSION_COUNT_QUERY, mo):
    case_one_query = mo.ui.code_editor(
        value=BROKEN_SESSION_COUNT_QUERY,
        language="sql",
        theme="dark",
        min_height=210,
        debounce=350,
        label="Case 1 SQL editor",
    )
    return (case_one_query,)


@app.cell
def _(case_one_query, connection, execute_query, mo):
    case_one_notes = mo.ui.text_area(
        placeholder="Diagnosis, evidence, corrected result, and one validation check...",
        full_width=True,
        rows=5,
        label="Investigation notes",
    )

    try:
        case_one_columns, case_one_rows = execute_query(
            connection, case_one_query.value
        )
        case_one_result = mo.hstack(
            [
                mo.stat(value, label=column, bordered=True)
                for column, value in zip(
                    case_one_columns, case_one_rows[0], strict=True
                )
            ],
            justify="start",
            gap=1,
            wrap=True,
        )
    except Exception as error:
        case_one_result = mo.callout(
            mo.md(f"`{error}`"), kind="danger", title="Query error"
        )

    case_one_panel = mo.vstack(
        [
            mo.Html(
                """
                <div class="case-head">
                  <div class="case-kicker">Case 01 / join grain</div>
                  <h2>The session count jumped</h2>
                  <p>
                    An analyst reports <strong>10 sessions for active shops</strong>.
                    A teammate expected fewer. Find the failed assumption before this
                    metric reaches a dashboard.
                  </p>
                </div>
                """
            ),
            case_one_query,
            mo.Html('<div class="result-label">Live query result</div>'),
            case_one_result,
            mo.accordion(
                {
                    "Need a nudge?": mo.md(
                        """
                        1. State the grain you expect from each table.
                        2. Compare row counts before and after the join.
                        3. Test whether the join key is unique on the dimension side.
                        4. Prefer a fix that makes the intended grain explicit.
                        """
                    )
                }
            ),
            case_one_notes,
        ],
        gap=1.15,
    )
    mo.style(
        case_one_panel,
        {
            "background": "linear-gradient(145deg, rgba(96,165,250,.10), rgba(16,20,27,.94) 34%)",
            "border": "1px solid rgba(96,165,250,.34)",
            "border-radius": "24px",
            "padding": "clamp(22px, 4vw, 38px)",
            "margin-top": "28px",
            "box-shadow": "0 22px 70px rgba(0,0,0,.28)",
        },
    )
    return (case_one_notes,)


@app.cell
def _(BROKEN_DURATION_QUERY, mo):
    case_two_query = mo.ui.code_editor(
        value=BROKEN_DURATION_QUERY,
        language="sql",
        theme="dark",
        min_height=285,
        debounce=350,
        label="Case 2 SQL editor",
    )
    return (case_two_query,)


@app.cell
def _(case_two_query, connection, execute_query, mo):
    case_two_notes = mo.ui.text_area(
        placeholder="Metric definition, counterexample, corrected result, and boundary test...",
        full_width=True,
        rows=5,
        label="Investigation notes",
    )

    try:
        case_two_columns, case_two_rows = execute_query(
            connection, case_two_query.value
        )
        case_two_result = mo.hstack(
            [
                mo.stat(value, label=column, bordered=True)
                for column, value in zip(
                    case_two_columns, case_two_rows[0], strict=True
                )
            ],
            justify="start",
            gap=1,
            wrap=True,
        )
    except Exception as error:
        case_two_result = mo.callout(
            mo.md(f"`{error}`"), kind="danger", title="Query error"
        )

    case_two_panel = mo.vstack(
        [
            mo.Html(
                """
                <div class="case-head">
                  <div class="case-kicker orange">Case 02 / time semantics</div>
                  <h2>One day can mean two different things</h2>
                  <p>
                    A report says <strong>6 of 8 sessions lasted at least one day</strong>.
                    Product partners read that as 24 elapsed hours. Test whether the SQL
                    measures the same definition.
                  </p>
                </div>
                """
            ),
            case_two_query,
            mo.Html('<div class="result-label">Live query result</div>'),
            case_two_result,
            mo.accordion(
                {
                    "Need a nudge?": mo.md(
                        """
                        1. Compare calendar boundaries with elapsed duration.
                        2. Inspect sessions that cross midnight.
                        3. Test values just below, exactly at, and above 24 hours.
                        4. Give the corrected metric an unambiguous name.
                        """
                    )
                }
            ),
            case_two_notes,
        ],
        gap=1.15,
    )
    mo.style(
        case_two_panel,
        {
            "background": "linear-gradient(145deg, rgba(251,146,60,.09), rgba(16,20,27,.94) 34%)",
            "border": "1px solid rgba(251,146,60,.30)",
            "border-radius": "24px",
            "padding": "clamp(22px, 4vw, 38px)",
            "margin-top": "28px",
            "box-shadow": "0 22px 70px rgba(0,0,0,.28)",
        },
    )
    return (case_two_notes,)


@app.cell
def _(mo):
    handoff = mo.Html(
        """
        <section class="section-head">
          <div class="case-kicker">Interview handoff / two minutes per case</div>
          <h2>Make the investigation easy to trust</h2>
          <p>Strong candidates can explain the wrong result without relying on the final SQL.</p>
          <div class="handoff-grid">
            <div class="handoff-item"><span>01</span><strong>Metric definition</strong></div>
            <div class="handoff-item"><span>02</span><strong>Failed assumption</strong></div>
            <div class="handoff-item"><span>03</span><strong>Minimal evidence</strong></div>
            <div class="handoff-item"><span>04</span><strong>Correction</strong></div>
            <div class="handoff-item"><span>05</span><strong>Independent validation</strong></div>
          </div>
        </section>
        <footer class="lab-footer">
          Synthetic educational data. This is not an official Shopify interview,
          dataset, process, or endorsement.
        </footer>
        """
    )
    mo.style(
        handoff,
        {
            "background": "rgba(11, 14, 20, .72)",
            "border": "1px solid #29313d",
            "border-radius": "24px",
            "padding": "clamp(22px, 4vw, 38px)",
            "margin-top": "28px",
        },
    )
    return


if __name__ == "__main__":
    app.run()
