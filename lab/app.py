import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


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
    from lab.query_utils import execute_query, markdown_table

    return (
        BROKEN_DURATION_QUERY,
        BROKEN_SESSION_COUNT_QUERY,
        create_connection,
        execute_query,
        markdown_table,
        mo,
    )


@app.cell
def _(mo):
    mo.md("""
    # SQL debugging lab

    You have joined a fictional commerce analytics team. Two production-style
    queries run successfully and return believable answers. Both answers are wrong.

    **Your task:** clarify the metric, inspect the data grain, isolate the failure,
    fix the query, and explain how you know the new answer is trustworthy.

    AI tools are allowed. You remain responsible for every assumption, query, and
    validation claim you present.

    > This lab uses small synthetic data inspired by commerce concepts. It does not
    > use Shopify data and does not represent or imply Shopify endorsement.
    """)
    return


@app.cell
def _(create_connection):
    connection = create_connection()
    return (connection,)


@app.cell
def _(connection, execute_query, markdown_table, mo):
    shop_columns, shop_rows = execute_query(
        connection,
        "SELECT * FROM shops ORDER BY shop_id, snapshot_at",
    )
    session_columns, session_rows = execute_query(
        connection,
        "SELECT * FROM sessions ORDER BY session_id",
    )
    mo.md(
        f"""
        ## Available tables

        `shops` is a dimension-style extract. `sessions` contains one row per session.
        Do not assume either statement is sufficient evidence. Check the data.

        ### shops
        {markdown_table(shop_columns, shop_rows)}

        ### sessions
        {markdown_table(session_columns, session_rows)}
        """
    )
    return


@app.cell
def _(BROKEN_SESSION_COUNT_QUERY, mo):
    mo.md(
        """
        ## Case 1: The session count jumped

        An analyst reports **10 sessions for active shops**. A teammate expected a lower
        number and asks you to investigate before the metric reaches a dashboard.

        Start with the query below. Change it freely. A good investigation shows the
        failing assumption before it applies a fix.
        """
    )
    case_one_query = mo.ui.code_editor(
        value=BROKEN_SESSION_COUNT_QUERY,
        language="sql",
        min_height=230,
    )
    case_one_query
    return (case_one_query,)


@app.cell
def _(case_one_query, connection, execute_query, markdown_table, mo):
    try:
        case_one_columns, case_one_rows = execute_query(
            connection, case_one_query.value
        )
        case_one_output = markdown_table(case_one_columns, case_one_rows)
    except Exception as error:
        case_one_output = f"**Query error:** `{error}`"

    mo.md(f"### Current result\n\n{case_one_output}")
    return


@app.cell
def _(mo):
    case_one_notes = mo.ui.text_area(
        placeholder=(
            "Write your diagnosis, evidence, corrected result, and one validation check."
        ),
        full_width=True,
        rows=6,
        label="Case 1 investigation notes",
    )
    mo.vstack(
        [
            mo.accordion(
                {
                    "Hints, open only when needed": mo.md(
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
        ]
    )
    return


@app.cell
def _(BROKEN_DURATION_QUERY, mo):
    mo.md(
        """
        ## Case 2: One day can mean two different things

        A report says **6 of 8 sessions lasted at least one day**. Product partners read
        that as "at least 24 elapsed hours." Check whether the SQL measures that definition.

        Preserve the original timestamps while you investigate. Show at least one row
        where the current logic and the business definition disagree.
        """
    )
    case_two_query = mo.ui.code_editor(
        value=BROKEN_DURATION_QUERY,
        language="sql",
        min_height=300,
    )
    case_two_query
    return (case_two_query,)


@app.cell
def _(case_two_query, connection, execute_query, markdown_table, mo):
    try:
        case_two_columns, case_two_rows = execute_query(
            connection, case_two_query.value
        )
        case_two_output = markdown_table(case_two_columns, case_two_rows)
    except Exception as error:
        case_two_output = f"**Query error:** `{error}`"

    mo.md(f"### Current result\n\n{case_two_output}")
    return


@app.cell
def _(mo):
    case_two_notes = mo.ui.text_area(
        placeholder=(
            "Define the metric, identify a counterexample, give the corrected result, "
            "and describe your validation."
        ),
        full_width=True,
        rows=6,
        label="Case 2 investigation notes",
    )
    mo.vstack(
        [
            mo.accordion(
                {
                    "Hints, open only when needed": mo.md(
                        """
                        1. Compare calendar boundaries with elapsed duration.
                        2. Inspect sessions that cross midnight.
                        3. Test values just below, exactly at, and above 24 hours.
                        4. Say which definition the metric name should communicate.
                        """
                    )
                }
            ),
            case_two_notes,
        ]
    )
    return


@app.cell
def _(mo):
    mo.md("""
    ## Interview handoff

    For each case, be ready to give a two-minute explanation:

    1. **Metric definition:** what question should the query answer?
    2. **Failure mode:** which assumption failed, and what evidence isolated it?
    3. **Correction:** how does your SQL make the intended grain or time meaning clear?
    4. **Validation:** which independent check would catch a regression?
    5. **Communication:** what would you tell the dashboard owner before publishing?

    Strong candidates can explain the wrong result without relying on the final SQL.
    """)
    return


if __name__ == "__main__":
    app.run()
