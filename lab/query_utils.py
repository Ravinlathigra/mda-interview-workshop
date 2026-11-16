"""Small display helpers used by the Marimo lab."""

from collections.abc import Sequence
from typing import Any

import duckdb


def execute_query(
    connection: duckdb.DuckDBPyConnection, query: str
) -> tuple[list[str], list[tuple[Any, ...]]]:
    """Run one candidate query and return column names and rows."""
    cursor = connection.execute(query)
    columns = [item[0] for item in cursor.description or []]
    return columns, cursor.fetchall()


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

