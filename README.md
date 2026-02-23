# Bridging the Gap — MDA Workshop 2026

A 2-hour interactive workshop helping MDA students at Western University prepare for technical interviews across data and engineering streams.

**Presenter:** Ravin Lathigra (MDA Alumnus, Senior Data Developer @ Shopify)
**Date:** February 23, 2026

---

## Files

### `index.html` — Presenter Slide Deck

The main presentation file. A single-page HTML slide deck with 36 slides covering:

- **Frameworks** — The "Why" Ladder, Explanation Pattern, STAR-T Checklist
- **Live Demos** — Precision/recall comparison (good vs. bad answers side by side)
- **Interactive Mock Interviews** — Two click-through interview simulations with annotated commentary:
  - *The Recipe Follower* (slide 8) — A candidate who follows the textbook perfectly but never questions it. Covers p-values, A/B testing, effect size, and multiple comparisons.
  - *The Chef* (slide 9) — A candidate who explains an ETL pipeline with business context, tradeoff awareness, and honest self-critique at every step.
- **Timed Exercises** — Built-in countdown timers for each exercise phase (think, explain, follow-up, feedback, writing, pitches, mock rounds)
- **Triad Activities** — Structured group exercises where students practice explaining concepts and pitching projects

**Navigation:**
- Arrow keys or spacebar to advance slides
- On mock interview slides (8 and 9), arrow keys step through the conversation instead of changing slides
- Click timeline dots on the left edge to jump to any slide
- Bottom bar shows progress and slide counter

**No dependencies.** Opens directly in any browser. Google Fonts loaded via CDN for typography.

---

### `workshop.html` — Student Reference App

A tabbed reference app shared with students. Contains all workshop materials in one self-contained page:

| Tab | Contents |
|-----|----------|
| **Home** | Frameworks recap (Why Ladder, Explanation Pattern, STAR-T) with examples for every stream |
| **Universal** | 5 concept explanation cards applicable to all streams |
| **BA/DA** | 6 stream-specific cards + universal cards |
| **Data Science** | 6 stream-specific cards + universal cards |
| **DE/MLE** | 6 stream-specific cards + universal cards |
| **SWE** | 6 stream-specific cards + universal cards |
| **AI/SWE** | 6 stream-specific cards + universal cards |
| **Mock Interviews** | 26 questions across 5 categories (A-E) with follow-ups, "listen for" hints, and full "great answer" examples |
| **Resources** | Study guides by stream, recommended resources, post-workshop plan, personal commitment prompts |

**Features:**
- Exercise cards with hidden follow-up questions (click to reveal)
- Expandable mock interview questions with detailed model answers
- Category filters on the Mock Interviews tab
- Stream-specific question routing (e.g., BA/DA sees categories A, C, E)

**No dependencies.** Opens directly in any browser. All data is inline in the HTML.

---

## Usage

Both files are fully self-contained HTML. No build step, no server, no dependencies beyond a browser.

```
open index.html      # present the slides
open workshop.html   # share with students
```

For the workshop: share `index.html` with students after the session so they can revisit the interactive mock interviews and step through them at their own pace.
