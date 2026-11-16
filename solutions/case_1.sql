-- Resolve the latest available snapshot BEFORE filtering on current status.
-- Contract: (shop_id, snapshot_at) is unique; status is current, not at session time.
WITH latest_shops AS (
    SELECT
        shop_id,
        status
    FROM shops
    QUALIFY ROW_NUMBER() OVER (
        PARTITION BY shop_id
        ORDER BY snapshot_at DESC
    ) = 1
)
SELECT
    COUNT(*) AS sessions_for_active_shops
FROM sessions
JOIN latest_shops
    USING (shop_id)
WHERE latest_shops.status = 'active';
