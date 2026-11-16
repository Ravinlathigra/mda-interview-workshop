# Interviewer guide: SQL debugging lab

## Interview intent

This exercise tests whether a candidate can turn a suspicious metric into a bounded
investigation, communicate what they learn, and validate a correction. SQL fluency
matters, but final-query speed should not dominate the assessment.

AI assistance is allowed but optional. Evaluate the candidate's ownership of the
reasoning. Ask them to explain generated SQL, identify its assumptions, and produce
evidence before accepting it.

## Workshop format: 35 minutes

- 15 minutes: case 1, including metric clarification and investigation
- 15 minutes: case 2, with a role rotation
- 5 minutes: handoffs, independent validation, and observer feedback

Setup happens in the preceding five-minute workshop slot. For a one-to-one practice
interview, use the same timeboxes and weave clarification into each case.

The cases use synthetic, Shopify-inspired commerce concepts. Do not present the data,
queries, or evaluation rubric as Shopify interview material or as endorsed by Shopify.

## Case 1: duplicated shop IDs

The starting query reports 10 sessions for active shops. The candidate should discover
that `shops` contains two active rows for `shop_id = 101`. Its three sessions duplicate
through the join. The corrected result is 7.

Metric-owner answer: use the latest available status per shop, not status at the
session's start. `(shop_id, snapshot_at)` is unique. Select the latest row across
**all statuses**, then filter active. Filtering first incorrectly resurrects a shop
with an older active record and a newer inactive one. The baseline fixture does not
expose that second bug; the regression tests do. Accept a semijoin or distinct count
when the candidate justifies its behavior against this contract and validates it.

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

Metric-owner answer: all eight sessions are in scope, all timestamps are UTC, and
each has a known, non-negative duration. The threshold includes exactly 24 hours.
For an empty population report zero qualifying sessions, zero total, and an undefined
(NULL) percentage. Ask for a policy if null endpoints, negative durations, or timezone
ambiguity are introduced; those are extensions, not hidden requirements.

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
| Communication | Cannot explain evidence or decisions | Narrates steps without rationale | Explains evidence and decisions | Gives a concise stakeholder handoff with remaining risk |
| AI ownership (if used) | Cannot explain generated work | Explains syntax only | Checks assumptions and edits the output | Challenges generated work and validates independently |

If AI was not used, mark that dimension N/A; do not penalize the candidate or require
tool use. Report the five core dimensions out of 15 and AI ownership separately out
of 3 when applicable. There is no validated pass cutoff. Use the evidence to choose
one strength and one next practice action, not to make a hiring recommendation.

Record which hints were given and when, plus one observed behavior per dimension.
Offer the same staged hints across groups. Allow quiet investigation followed by a
short explanation; score clarity of evidence, not accent, verbosity, or thinking aloud
continuously. Do not infer lack of reasoning from a pause.

## Reference material

The executable answers live in `solutions/case_1.sql` and `solutions/case_2.sql`.
Each notebook case loads its answer into a collapsed **Reveal solution** section
with editable SQL, explanation, expected output, and a separate Run button. Keep it
collapsed during investigation and open it together during the debrief.
Automated checks in `tests/test_lab.py` pin the intended broken and corrected results.
