"""Small display helpers used by the Marimo lab."""

from collections.abc import Sequence
from typing import Any

import duckdb


def execute_query(
    connection: duckdb.DuckDBPyConnection, query: str
) -> tuple[list[str], list[tuple[Any, ...]]]:
    """Run one inspection query, fetching at most 201 rows (200 + overflow marker).

    This guards the exercise against accidental edits to its shared fixture; it is
    not a security sandbox for SQL from untrusted remote users.
    """
    statements = connection.extract_statements(query)
    if len(statements) != 1 or statements[0].type not in (
        duckdb.StatementType.SELECT,
        duckdb.StatementType.EXPLAIN,
    ):
        raise ValueError(
            "Run one SELECT, WITH, DESCRIBE, or EXPLAIN query at a time. "
            "The lab data is read-only."
        )
    connection.execute("BEGIN TRANSACTION")
    try:
        cursor = connection.execute(query)
        columns = [item[0] for item in cursor.description or []]
        return columns, cursor.fetchmany(201)
    finally:
        # EXPLAIN ANALYZE executes its inner statement. Never persist its changes.
        connection.execute("ROLLBACK")


def table_records(
    columns: Sequence[str], rows: Sequence[Sequence[Any]]
) -> list[dict[str, Any]]:
    """Preserve every column, including repeated aliases in diagnostic joins."""
    labels: list[str] = []
    for column in columns:
        label = column
        suffix = 2
        while label in labels:
            label = f"{column} ({suffix})"
            suffix += 1
        labels.append(label)
    return [dict(zip(labels, row, strict=True)) for row in rows]


def markdown_table(columns: Sequence[str], rows: Sequence[Sequence[Any]]) -> str:
    """Render a compact Markdown table without a dataframe dependency."""
    if not columns:
        return "_The query completed without a result set._"

    def clean(value: Any) -> str:
        return str(value).replace("|", "\\|").replace("\n", " ")

    header = "| " + " | ".join(clean(column) for column in columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(clean(value) for value in row) + " |" for row in rows]
    return "\n".join([header, divider, *body])
