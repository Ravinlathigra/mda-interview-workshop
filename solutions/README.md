# Reference solutions

Keep this folder out of the candidate's view during the exercise.

## Case 1

The broken join returns 10 rows because `shops` contains two active snapshots for
`shop_id = 101`. That shop owns three sessions, so the join duplicates all three.
The correct result is **7 sessions for active shops**.

The reference query chooses the latest shop snapshot across all statuses, then filters
active before counting joined sessions. Filtering active before ranking would wrongly
include a shop that has since become inactive. The metric uses current/latest status,
not a historical as-of join at the session's start. A
`COUNT(DISTINCT session_id)` patch also returns 7 for this data, but it can hide the
failed join-grain assumption. Prefer to make the expected dimension grain explicit.
Distinct counts and semijoins are acceptable when they honor the same latest-status
contract; explain their tradeoffs. Snapshot timestamps are unique per shop in this lab.

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

The denominator includes all sessions, regardless of shop status. Timestamps represent
UTC and have known, non-negative durations. Equality at 24 hours counts. Tests exercise
one microsecond below, exactly at, and one microsecond above that boundary. Empty input
produces `(0, 0, NULL)`: no qualifying sessions and no meaningful percentage. Missing
endpoints and conflicting snapshot ties require explicit policies in a real dataset.
