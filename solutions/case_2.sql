-- Measure elapsed time directly. Crossing midnight does not imply 24 hours elapsed.
SELECT
    COALESCE(COUNT_IF(ended_at - started_at >= INTERVAL '24 hours'), 0)
        AS sessions_at_least_24_hours,
    COUNT(*) AS total_sessions,
    ROUND(
        100.0 * COUNT_IF(ended_at - started_at >= INTERVAL '24 hours')
        / NULLIF(COUNT(*), 0),
        1
    ) AS percent_at_least_24_hours
FROM sessions;
