from pathlib import Path

import pytest

from lab.database import (
    BROKEN_DURATION_QUERY,
    BROKEN_SESSION_COUNT_QUERY,
    create_connection,
)
from lab.query_utils import execute_query, table_records


ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def connection():
    database = create_connection()
    yield database
    database.close()


def scalar(connection, query: str):
    return connection.execute(query).fetchone()[0]


def test_fixture_preserves_the_duplicate_shop_key(connection):
    duplicate_rows = connection.execute(
        """
        SELECT shop_id, COUNT(*)
        FROM shops
        GROUP BY shop_id
        HAVING COUNT(*) > 1
        """
    ).fetchall()
    assert duplicate_rows == [(101, 2)]


def test_case_one_broken_query_inflates_the_count(connection):
    assert scalar(connection, BROKEN_SESSION_COUNT_QUERY) == 10


def test_case_one_reference_solution_restores_session_grain(connection):
    query = (ROOT / "solutions" / "case_1.sql").read_text()
    assert scalar(connection, query) == 7


def test_case_two_broken_query_counts_calendar_boundaries(connection):
    count, total = connection.execute(BROKEN_DURATION_QUERY).fetchone()
    assert (count, total) == (6, 8)


def test_case_two_reference_solution_measures_elapsed_time(connection):
    query = (ROOT / "solutions" / "case_2.sql").read_text()
    count, total, percentage = connection.execute(query).fetchone()
    assert (count, total, percentage) == (2, 8, 25.0)


def test_short_cross_midnight_session_is_a_counterexample(connection):
    calendar_days, elapsed_minutes = connection.execute(
        """
        SELECT
            DATE_DIFF('day', CAST(started_at AS DATE), CAST(ended_at AS DATE)),
            DATE_DIFF('minute', started_at, ended_at)
        FROM sessions
        WHERE session_id = 'ses_001'
        """
    ).fetchone()
    assert calendar_days == 1
    assert elapsed_minutes == 10


def test_latest_status_is_selected_before_filtering_active(connection):
    connection.execute("""
        INSERT INTO shops VALUES
            (101, 'Maple Outfitters', 'plus', 'inactive', TIMESTAMP '2026-03-01'),
            (103, 'Harbour Home', 'basic', 'active', TIMESTAMP '2026-03-01')
    """)
    query = (ROOT / "solutions" / "case_1.sql").read_text()
    # Remove shop 101's three sessions, add shop 103's one session: 7 - 3 + 1.
    assert scalar(connection, query) == 5


def test_older_snapshot_does_not_multiply_sessions(connection):
    connection.execute("""
        INSERT INTO shops VALUES
            (102, 'Northern Stationery', 'basic', 'active', TIMESTAMP '2025-12-01')
    """)
    query = (ROOT / "solutions" / "case_1.sql").read_text()
    assert scalar(connection, query) == 7


@pytest.mark.parametrize("duration, expected", [
    ("23 hours 59 minutes 59.999999 seconds", 0),
    ("24 hours", 1),
    ("24 hours 0.000001 seconds", 1),
    ("0 seconds", 0),
])
def test_duration_threshold_measures_elapsed_time(connection, duration, expected):
    connection.execute("DELETE FROM sessions")
    connection.execute("""
        INSERT INTO sessions VALUES (
            'boundary', 101, TIMESTAMP '2026-01-01 23:59:59.5',
            TIMESTAMP '2026-01-01 23:59:59.5' + CAST(? AS INTERVAL), 'web'
        )
    """, [duration])
    query = (ROOT / "solutions" / "case_2.sql").read_text()
    assert connection.execute(query).fetchone() == (expected, 1, expected * 100.0)


def test_empty_population_has_no_percentage(connection):
    connection.execute("DELETE FROM sessions")
    query = (ROOT / "solutions" / "case_2.sql").read_text()
    assert connection.execute(query).fetchone() == (0, 0, None)


def test_query_runner_preserves_multiple_rows_and_empty_results(connection):
    columns, rows = execute_query(connection, "SELECT session_id FROM sessions ORDER BY session_id")
    assert columns == ["session_id"]
    assert len(rows) == 8
    assert rows[-1] == ("ses_008",)
    assert execute_query(connection, "SELECT session_id FROM sessions WHERE false") == (["session_id"], [])


@pytest.mark.parametrize("query", [
    "DELETE FROM sessions",
    "DROP TABLE shops",
    "SELECT 1; DELETE FROM sessions",
    "SELECT 1; SELECT 2",
    "",
])
def test_query_runner_rejects_mutations_and_multiple_statements(connection, query):
    with pytest.raises(ValueError, match="one SELECT"):
        execute_query(connection, query)
    assert scalar(connection, "SELECT COUNT(*) FROM sessions") == 8


def test_query_runner_supports_ctes_and_bounds_preview(connection):
    columns, rows = execute_query(connection, "WITH n AS (SELECT range AS n FROM range(500)) SELECT * FROM n ORDER BY n")
    assert columns == ["n"]
    assert len(rows) == 201  # One extra row tells the UI that the preview was truncated.
    assert rows[-1] == (200,)


def test_result_table_preserves_duplicate_column_aliases():
    assert table_records(["id", "id", "id (2)"], [(101, 102, 103)]) == [
        {"id": 101, "id (2)": 102, "id (2) (2)": 103}
    ]


def test_explain_analyze_cannot_change_the_fixture(connection):
    execute_query(connection, "EXPLAIN ANALYZE DELETE FROM sessions")
    assert scalar(connection, "SELECT COUNT(*) FROM sessions") == 8


def test_failed_query_leaves_runner_usable(connection):
    import duckdb

    with pytest.raises(duckdb.Error):
        execute_query(connection, "SELECT missing_column FROM sessions")
    assert execute_query(connection, "SELECT COUNT(*) AS count FROM sessions") == (["count"], [(8,)])
