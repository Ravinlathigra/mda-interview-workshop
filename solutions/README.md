# Reference solutions

Keep this folder out of the candidate's view during the exercise.

## Case 1

The broken join returns 10 rows because `shops` contains two active snapshots for
`shop_id = 101`. That shop owns three sessions, so the join duplicates all three.
The correct result is **7 sessions for active shops**.

The reference query chooses the latest active shop snapshot before joining. A
`COUNT(DISTINCT session_id)` patch also returns 7 for this data, but it can hide the
failed join-grain assumption. Prefer to make the expected dimension grain explicit.

Useful validation queries:

```sql
SELECT shop_id, COUNT(*) AS rows_per_key
FROM shops
GROUP BY shop_id
HAVING COUNT(*) > 1;

SELECT COUNT(*) FROM sessions;
SELECT COUNT(*) FROM sessions JOIN shops USING (shop_id);
```

## Case 2

The broken query counts calendar-day boundaries after truncating timestamps to dates.
Six sessions cross at least one midnight, but only `ses_004` and `ses_007` last 24
hours or longer. The correct result is **2 of 8 sessions, or 25.0%**.

Useful counterexamples include `ses_001` (10 minutes across midnight) and `ses_006`
(23.5 hours across midnight). A good metric name states the definition, such as
`sessions_at_least_24_hours`, rather than the ambiguous `one_day_sessions`.

