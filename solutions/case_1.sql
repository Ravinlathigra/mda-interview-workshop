-- One row per active shop before joining to one row per session.
WITH active_shops AS (
    SELECT
        shop_id
    FROM shops
    WHERE status = 'active'
    QUALIFY ROW_NUMBER() OVER (
        PARTITION BY shop_id
        ORDER BY snapshot_at DESC
    ) = 1
)
SELECT
    COUNT(*) AS sessions_for_active_shops
FROM sessions
JOIN active_shops
    USING (shop_id);

