from pathlib import Path

import pytest

from lab.database import (
    BROKEN_DURATION_QUERY,
    BROKEN_SESSION_COUNT_QUERY,
    create_connection,
)


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

