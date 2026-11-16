# Interviewer guide: SQL debugging lab

## Interview intent

This exercise tests whether a candidate can turn a suspicious metric into a bounded
investigation, communicate what they learn, and validate a correction. SQL fluency
matters, but final-query speed should not dominate the assessment.

The interviewer may allow any AI assistant. Evaluate the candidate's ownership of the
reasoning. Ask them to explain generated SQL, identify its assumptions, and produce
evidence before accepting it.

## Suggested format: 35 minutes

- 3 minutes: setup, data dictionary, metric clarification
- 12 minutes: case 1, duplicated dimension key
- 12 minutes: case 2, calendar boundary versus elapsed duration
- 6 minutes: candidate handoff and validation discussion
- 2 minutes: candidate questions

The cases use synthetic, Shopify-inspired commerce concepts. Do not present the data,
queries, or evaluation rubric as Shopify interview material or as endorsed by Shopify.

## Case 1: duplicated shop IDs

The starting query reports 10 sessions for active shops. The candidate should discover
that `shops` contains two active rows for `shop_id = 101`. Its three sessions duplicate
through the join. The corrected result is 7.

Strong evidence includes:

- stating the expected grain of both tables before editing the query
- comparing counts before and after the join
- checking uniqueness of `shops.shop_id`
- choosing the latest shop snapshot or otherwise reducing to one row per shop
- explaining why `COUNT(DISTINCT session_id)` can mask the failed join assumption

If the candidate stalls, use one prompt at a time:

1. "What should one row represent on each side of the join?"
2. "What happens to row count at each step?"
3. "How would you test the uniqueness of the join key?"

## Case 2: calendar day versus elapsed time

The starting query reports 6 of 8 sessions at least one day long. It casts timestamps
to dates and counts calendar boundaries. Only two sessions last at least 24 hours, so
the corrected result is 2 of 8, or 25.0%.

Strong evidence includes:

- asking whether "one day" means a date boundary or 24 elapsed hours
- preserving timestamps during diagnosis
- showing a counterexample such as `ses_001`, which lasts 10 minutes across midnight
- testing below, at, and above the 24-hour threshold
- proposing an unambiguous metric name such as `sessions_at_least_24_hours`

If the candidate stalls, use one prompt at a time:

1. "Can a short session touch two calendar dates?"
2. "Which row would prove the current definition is misleading?"
3. "What condition directly represents 24 elapsed hours?"

## Scoring rubric

Score each dimension from 0 to 3. Record observable evidence rather than impressions.

| Dimension | 0 | 1 | 2 | 3 |
| --- | --- | --- | --- | --- |
| Problem framing | Starts coding without defining the metric | Repeats the prompt | Clarifies definition or grain | Clarifies both and identifies ambiguity early |
| Investigation | Guesses a fix | Runs broad queries without a hypothesis | Uses targeted diagnostics | Isolates a minimal counterexample and updates the hypothesis |
| SQL correction | Does not produce a working correction | Produces a fragile patch | Produces a correct query | Makes grain or time semantics explicit and discusses alternatives |
| Validation | Trusts the new output | Re-runs the same logic | Uses an independent reconciliation | Adds boundary cases and a regression check |
| Communication | Works silently or cannot explain | Narrates steps without rationale | Explains evidence and decisions | Gives a concise stakeholder handoff with remaining risk |
| AI ownership | Cannot explain generated work | Explains syntax only | Checks assumptions and edits the output | Uses AI selectively, challenges it, and validates independently |

A score of 12 or higher out of 18 usually demonstrates the workshop target. Do not use
the number as a hiring recommendation. This rubric supports consistent practice feedback.

## Reference material

The executable answers live in `solutions/case_1.sql` and `solutions/case_2.sql`.
Automated checks in `tests/test_lab.py` pin the intended broken and corrected results.

