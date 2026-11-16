# Facilitator runbook: workshop v2 debugging lab

## Purpose

This module adds a practical debugging interview to the existing explanation and project
story exercises. Participants practice forming a hypothesis, producing evidence, and
handing off a validated correction. The exercise uses synthetic commerce data.

## Before the session

1. Install the repository once and run the checks:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   python -m pip install -e ".[dev]"
   python -m pytest
   marimo check lab/app.py
   ```

2. Start the notebook with `marimo edit lab/app.py` and confirm both query editors run.
3. Keep `solutions/` closed while candidates work.
4. Ask participants to install dependencies before the session when possible.
5. Have a browser tab with `workshop.html` and a separate tab with the Marimo lab.

## Recommended 120-minute workshop flow

| Time | Activity | Facilitator focus |
| --- | --- | --- |
| 0:00-0:15 | Opening, evaluation lens, live examples | Explain that plausible output still needs evidence |
| 0:15-0:20 | Form groups and open the lab | Groups of two or three, one shared screen |
| 0:20-0:55 | SQL debugging lab | 15 minutes per case, 5 minutes for handoff notes |
| 0:55-1:05 | Lab debrief | Compare failure modes and validation strategies |
| 1:05-1:10 | Break | Keep the lab available for later review |
| 1:10-1:30 | Explanation lab | Shorten to one round per participant |
| 1:30-1:50 | STAR-T project pitch | Require one tradeoff and one validation detail |
| 1:50-1:58 | Mock interview round | Use a stream-specific question |
| 1:58-2:00 | Commitments and close | Capture one practice action |

## Group roles

For each case, assign an investigator, interviewer, and observer. In pairs, the
interviewer also records evidence. Rotate after case 1.

- The investigator shares the screen and narrates the investigation.
- The interviewer asks for definitions, evidence, and validation without giving the fix.
- The observer records one strong behavior and one missed opportunity.

AI is allowed. Ask the investigator to state when AI contributed a query and then explain
the query's assumptions. The observer should record whether the candidate validated it.

## Facilitation cues

At five minutes, ask: "What do you believe is wrong, and what evidence would disprove
that belief?"

At ten minutes, ask: "What is the smallest row or count that demonstrates the failure?"

At the handoff, require five points: definition, diagnosis, evidence, correction, and
validation. Stop a long SQL walkthrough and ask for the stakeholder-facing explanation.

## Debrief

Reveal the reference solutions only after groups present evidence.

For case 1, emphasize that a syntactically correct join can change the fact-table grain.
`COUNT(DISTINCT)` repairs this output but can conceal the model defect.

For case 2, ask participants to compare `ses_001` and `ses_004`. One crosses midnight
after ten minutes. The other lasts 24.5 hours. The metric owner must choose which
definition matters before the engineer chooses SQL.

Close with the common pattern: define the business meaning, inspect grain and boundaries,
isolate a counterexample, correct the logic, and validate independently.

## Recovery plan

If Marimo does not start, run the queries from any DuckDB client after loading the CSVs,
or pair the affected participant with a working group. Do not spend lab time debugging
individual Python installations. The candidate and interviewer guides contain the full
prompt and rubric.

## Attribution note

Present Ravin Lathigra accurately as a Staff Data Engineer at Shopify. Frame observations
as his professional perspective and workshop guidance. Do not describe the lab as an
official Shopify interview, process, dataset, or endorsement.

