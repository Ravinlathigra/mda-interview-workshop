"""Deterministic DuckDB setup shared by the lab and its tests."""

from pathlib import Path

import duckdb


LAB_DIR = Path(__file__).resolve().parent
DATA_DIR = LAB_DIR / "data"

BROKEN_SESSION_COUNT_QUERY = """
SELECT
    COUNT(*) AS sessions_for_active_shops
FROM sessions AS sessions
JOIN shops AS shops
    ON sessions.shop_id = shops.shop_id
WHERE shops.status = 'active';
""".strip()

BROKEN_DURATION_QUERY = """
SELECT
    COUNT_IF(
        DATE_DIFF(
            'day',
            CAST(started_at AS DATE),
            CAST(ended_at AS DATE)
        ) >= 1
    ) AS sessions_at_least_one_day,
    COUNT(*) AS total_sessions
FROM sessions;
""".strip()


def _sql_path(path: Path) -> str:
    """Return a quoted SQL literal for a trusted local path."""
    return "'" + str(path).replace("'", "''") + "'"


def create_connection() -> duckdb.DuckDBPyConnection:
    """Create an in-memory database containing the fictional lab data."""
    connection = duckdb.connect(database=":memory:")
    connection.execute(
        f"""
        CREATE TABLE shops AS
        SELECT *
        FROM read_csv(
            {_sql_path(DATA_DIR / 'shops.csv')},
            header = true,
            columns = {{
                'shop_id': 'INTEGER',
                'shop_name': 'VARCHAR',
                'plan': 'VARCHAR',
                'status': 'VARCHAR',
                'snapshot_at': 'TIMESTAMP'
            }}
        );
        """
    )
    connection.execute(
        f"""
        CREATE TABLE sessions AS
        SELECT *
        FROM read_csv(
            {_sql_path(DATA_DIR / 'sessions.csv')},
            header = true,
            columns = {{
                'session_id': 'VARCHAR',
                'shop_id': 'INTEGER',
                'started_at': 'TIMESTAMP',
                'ended_at': 'TIMESTAMP',
                'channel': 'VARCHAR'
            }}
        );
        """
    )
    return connection

