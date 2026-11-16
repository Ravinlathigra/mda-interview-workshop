# Bridging the Gap: MDA Technical Interview Workshop

A one-hour workshop for MDA students at Western University, centred on explaining
technical thinking, responding to follow-ups, and improving an answer through feedback.
The closing section applies those skills to pair-programming interviews with AI agents.

**Presenter:** Ravin Lathigra, MDA alumnus and Staff Data Engineer at Shopify

**Presentation term:** Winter 2026

This is independent educational material and Ravin's professional perspective, not an
official Shopify interview, hiring policy, dataset, or endorsement. Examples are fictional.

## Open the workshop

Open `index.html` for the presenter deck and `workshop.html` for the participant reference.
No installation, Python environment, notebook, or build step is needed.

```sh
open index.html
open workshop.html
```

Both files work directly in a browser. Google Fonts load when internet access is available,
with local fallback fonts when offline. To preview over HTTP, optionally run
`python3 -m http.server 2718 --bind 127.0.0.1`, then open http://localhost:2718/.

## One-hour flow

| Time | Activity |
| --- | --- |
| 0–5 min | Overview and what we are practising |
| 5–12 min | Weak and stronger explanations, with the Why Ladder |
| 12–17 min | Explanation framework, groups, and question selection |
| 17–35 min | Three explanation rounds, six minutes per person |
| 35–45 min | Second attempt at the same question, three minutes per person plus transitions |
| 45–48 min | Debrief: what improved and why? |
| 48–60 min | Pair-programming tips, worked examples, and questions |

The closing section covers permitted agent use, independent validation, and explaining
how a solution serves the business requirement. A ten-minute session crossing midnight
demonstrates calendar-date versus elapsed-time comparisons. A fictional dragon-parking
policy shows why the interviewer must clarify the intended rule.

## Materials and navigation

- `index.html`: one-hour presenter flow with built-in timers. Arrow keys or space advance.
  Timeline dots jump between slides. Links can target a slide, such as
  `index.html#s-pair-dates`.
- `index.html?extended=1#s-extra`: optional original interview simulations, STAR-T project
  pitches, and mock interview rounds. These appear after the closing slide and are outside
  the one-hour agenda. The interactive simulations step through dialogue with arrow keys.
- `workshop.html`: original stream-specific explanation cards, frameworks, mock interview
  bank, and resources, plus a Pair Programming tab. No coding setup is required.
- `guides/facilitator-runbook.md`: timing, group instructions, debrief prompts, and speaker
  notes for the closing examples.

The former Marimo/DuckDB lab and its dependencies have been removed. Previous versions
remain recoverable in Git history.

## Maintainer checks

The checks use Python's standard library and Node.js, with no package installation:

```sh
python3 -m unittest discover -s tests -v
```

They check HTML structure and local links, JavaScript syntax, the one-hour agenda,
timer wiring, optional slides, and the timestamp example's boundary results.
