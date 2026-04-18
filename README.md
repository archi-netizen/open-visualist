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

## Repository Structure

```text
open-visualist/
├── api/                  # Python/FastAPI backend (The "Brain")
│   ├── main.py           # API Entry point
│   ├── extraction.py     # LLM logic for keyword harvesting
│   └── sourcing.py       # Public Domain API integrations
├── web/                  # React/Next.js Front-end
│   ├── components/       # Split-pane UI & Thought-Trace display
│   └── hooks/            # Sideloading & attribution logic
├── wordpress-plugin/     # The "OpenVisualist Sync" WP integration
├── .env.example          # API Keys (OpenAI, Unsplash, Pexels)
└── LICENSE               # MIT

---

## View Mockup
https://kaushambimate.com/openvisualist-ai/
