# OpenVisualist AI 

> **Context-aware image sourcing for the Public Domain. Stop generating. Start discovering.**

OpenVisualist is an AI-powered curation engine that bridges the gap between long-form writing and the world's vast archives of public domain imagery. Unlike generative AI which creates "synthetic" pixels, OpenVisualist acts as an autonomous librarian—reading your text, understanding the nuance, and sourcing real photography from history.

---

## The Vision
In an era of AI hallucinations, **OpenVisualist** prioritizes the "Provenance of the Real." It is designed for authors, historians, and publishers who need high-quality visuals without the legal or ethical ambiguity of generated art.

## How the AI Works
OpenVisualist doesn't just "search" keywords; it performs **Semantic Mapping**:
1. **Contextual Analysis:** The engine uses LLMs to parse your essay for themes, moods, and specific historical references.
2. **Visual Query Expansion:** It translates abstract concepts (e.g., "industrial melancholy") into concrete search parameters (e.g., "19th-century steel mill, low light, soot").
3. **Archive Sourcing:** It queries Public Domain APIs (Openverse, NASA, Wikimedia, Unsplash CC0) to find exact matches.
4. **Verification:** A secondary vision pass ensures the image composition aligns with the text's intent.

---

## View Mockup
https://kaushambimate.com/openvisualist-ai/

---

## Status

`api/` and `web/` are implemented and work together end-to-end today.
`wordpress-plugin/` and the multi-archive/verification steps under "How the
AI Works" above are still the vision, not yet built — see
`web/README.md` for the precise list of what's real vs. aspirational in the
current UI.

## Quickstart

```bash
git clone https://github.com/archi-netizen/open-visualist
cd open-visualist

# 1. Backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in OPENAI_API_KEY at least
uvicorn api.main:app --reload --port 8000

# 2. Frontend (separate terminal)
cd web
npm install
cp .env.example .env.local
npm run dev
```

Then open http://localhost:3000. See `web/README.md` for what the UI
does and doesn't do yet.

## Repository Structure

```text
open-visualist/
├── api/                  # Python/FastAPI backend (The "Brain")
│   ├── main.py           # API entry point
│   ├── extraction.py     # LLM logic for keyword harvesting
│   ├── sourcing.py       # Public Domain API integrations (Openverse)
│   └── models.py         # Shared Pydantic request/response models
├── web/                  # Next.js front-end (split-pane UI)
│   ├── src/app/           # Pages (App Router)
│   ├── src/components/    # WritingZone, CurationZone, ImageCard, LicenseShield
│   └── src/lib/           # API client + shared types
├── wordpress-plugin/     # Planned — the "OpenVisualist Sync" WP integration (not built yet)
├── design_logic.md       # UX/interaction spec the front-end is built against
├── .env.example          # Backend API keys (OpenAI, Openverse)
└── LICENSE               # MIT

