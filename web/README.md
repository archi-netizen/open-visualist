# OpenVisualist — web

The split-pane front-end from `design_logic.md`: a Writing Zone on the left,
a Curation Zone of sourced public-domain images on the right. Built with
Next.js (App Router) + Tailwind CSS.

## Run it

The API in `../api` must be running first (see the root README).

```bash
npm install
cp .env.example .env.local   # points at the API, defaults to localhost:8000
npm run dev
```

Open http://localhost:3000, and start typing an essay. Three seconds after
you pause, it calls `POST /analyze-and-source` and shows results grouped by
the visual keyword that found them.

## What's implemented vs. what's still aspirational

`design_logic.md` describes a more ambitious interface than what's built so
far. What's here:

- Debounced (3000ms) whole-essay analysis
- Results grouped by matched keyword, with a confidence meter, a license
  shield (green = public domain, yellow = attribution required), and a
  one-click "copy attribution" button using Openverse's own attribution string

What's **not** implemented yet, because the backend doesn't support it:

- **Margin-Highlight** — the design calls for the exact source text to be
  underlined inline. The current backend analyzes the whole essay in one
  shot and doesn't return character offsets, so this UI shows keyword chips
  instead of inline highlights.
- **Sticky Vertical Alignment / per-paragraph sync** — same root cause:
  results are grouped by keyword, not anchored to a specific paragraph,
  because the API isn't paragraph-aware yet.
- **Confidence Meter as a real vision-verification score** — the number
  shown is a simple keyword/title/tag overlap heuristic computed in
  `api/sourcing.py`, not the "secondary vision pass" the README describes.
- Cross-archive search (NASA, Wikimedia) — only Openverse is wired up.
- The WordPress "OpenVisualist Sync" plugin isn't built.

Closing any of these gaps means extending the API first (e.g. having
`/analyze-and-source` return per-paragraph results, or adding a real
vision-model verification step) — the frontend would then consume that
richer response.
