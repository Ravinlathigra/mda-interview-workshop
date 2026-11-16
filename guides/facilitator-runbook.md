# Facilitator runbook: one-hour explanation workshop

## Aim and preparation

Help participants make technical reasoning understandable, respond to a challenge, and
improve an explanation. Finish by applying those same skills to pair-programming interviews.
No coding exercise or software installation is required.

Open `index.html` and share `workshop.html`. Confirm the timers work. Use the default
deck for the one-hour session. The Extra practice link opens the original simulations,
project pitches, and mock rounds separately from the main flow. Do not try to fit them
into this hour. Participants can revisit them later.

Introduce Ravin Lathigra as a Staff Data Engineer at Shopify and MDA alumnus. This is his
independent professional perspective, not an official Shopify interview or hiring policy.
All worked examples are fictional. The presentation term is Winter 2026.

## 60-minute agenda

| Time | Slides / activity | Facilitation |
| --- | --- | --- |
| 0–5 min | Title, format, evaluation lens | Set the goal: make reasoning easy to follow and question |
| 5–12 min | Why Ladder, fraud explanation comparison | Ask what the second answer clarifies beyond the definition |
| 12–17 min | Groups, warm-up, Explanation Pattern, instructions | Form triads, introduce yourselves, choose one question each |
| 17–35 min | First pass, three rounds | Six minutes per person: think 1, explain 2, follow-up 2, feedback 1 |
| 35–45 min | Second attempt | Three minutes each: revise 30s, explain 60s, follow-up 45s, feedback 45s. Allow 1 minute for transitions |
| 45–48 min | Debrief | Ask for a specific improvement and the question that prompted it |
| 48–58 min | Pair-programming closing examples | Roughly two minutes per closing slide |
| 58–60 min | Questions and close | Share the reference page and invite a future practice session |

Keep the opener on screen before the session. The first explanation round starts at
minute 17. If the introduction runs long, shorten the demo discussion, not the second attempt.

## Explanation rounds

Participants choose a Universal or stream-specific explanation card in `workshop.html`.
Keep that question for both attempts. The first pass uses the Think, Explain, Follow-up,
and Feedback timer slides. Return to Think after each role rotation. The second pass uses
the three-minute timer once per participant. Call its phase changes at 2:30, 1:30, and 0:45
remaining. Use the first minute of the second-pass block for instructions and transitions.

- Explainer: use plain language, intuition, a concrete example, and a limitation.
- Listener: ask the card's follow-up, then connect it to a decision or counterexample.
- Observer: name one clear point and one actionable improvement. Check correctness as
  well as delivery. Fluent explanations can still contain faulty reasoning.

In pairs, the listener also gives feedback. Use the third slot to compare explanations
or try a different follow-up. Nobody needs to present to the whole room.

Useful questions: “Who needs this?”, “What would change your answer?”, “Can you give a
small example?”, and “What would you check before trusting that result?” If a claim is
uncertain, record what evidence would settle it instead of inventing an answer.

AI is optional for preparation or critique. The participant gives the explanation in
their own words and responds to follow-ups. No one needs an account or tool installation.

## Closing: pair programming and agents

### 1. Agent use and collaboration

Recommend using an agent when the interview explicitly permits it. Check the rules first,
use approved tools and data, and be transparent about what the agent contributed. Some
interviews prohibit AI. This workshop does not describe any particular employer's policy.

Show the connection to the exercise: an agent can propose code, but the candidate must
explain its assumptions, debug unexpected results, and justify the checks. Give it a small
task, inspect the change, predict expected results, then test. An agent generating both
the implementation and matching tests is not independent evidence of correctness.

### 2. Calendar dates versus elapsed time

Display `s-pair-dates`. Read the timestamps aloud: January 10 at 23:55 to January 11 at
00:05, in UTC. Ask “Did this last a day?” before discussing the table.

There are ten elapsed minutes, but the date changed. Both comparisons have a legitimate
meaning. If the requirement is at least 24 elapsed hours, a date comparison implements
the wrong rule. Do not present calendar-date comparisons as inherently defective.

Ask the audience to say which question each comparison actually answers. This is an
explanation exercise, not a SQL syntax quiz. No notebook or database is needed.

### 3. Debugging and validation

Display `s-pair-debug`. Model the spoken explanation on the slide. The tiny midnight
example disproves the date rule for a duration requirement. Compare unambiguous timestamp
instants to measure elapsed time. Confirm the expected results before running code:

| Duration | At least 24 hours? |
| --- | --- |
| 10 minutes across midnight | No |
| 23h 59m | No |
| 24h exactly | Yes |
| 24h 01m | Yes |

Equality matters because the requirement says “at least.” These checks do not prove all
cases. Ask about missing end times, end-before-start records, and time zones next. Local
calendar days can differ from 24 hours around daylight-saving changes. Agree on a local
zone for date rules and use unambiguous instants for duration rules.

### 4. Business context, even for a silly mock

Display `s-pair-business`: “Charge dragons that stay overnight.” The ten-minute stay
qualifies for a fee on crossing local midnight, but not for a fee after a free 24-hour
allowance. Ask which policy the interviewer intends. For the latter, also ask whether
the fee starts exactly at 24 hours or only after it. Do not silently reuse the previous
“at least 24 hours” rule for this different requirement.

The consequence makes the definition matter: one policy charges the dragon and another
does not. For a purely abstract puzzle, ask for the intended behavior and constraints
instead of forcing a fabricated business story. If clarification is unavailable, state
an assumption and continue.

### 5. Handoff and questions

Use `s-pair-handoff` to connect the hour: clarify the goal, explain a hypothesis, demonstrate
a check, and name what remains uncertain. Narrate decisions instead of every keystroke.
Invite the interviewer to collaborate. Reserve the final two minutes for questions and
sharing `workshop.html`. The original question bank and extra slides remain available.
