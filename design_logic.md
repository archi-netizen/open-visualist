# OpenVisualist | Website Design Logic

This document defines the interface architecture and the "Agentic UX" principles that govern how OpenVisualist functions as a bridge between text and the Public Domain.

---

## 🛠 1. The Interaction Engine (The "Brain")

OpenVisualist does not use traditional search bars. It uses **Contextual Listening logic**:

* **Debounce Processing:** To prevent API spam and ensure "Deep Thinking," the engine waits for a `3000ms` pause in user typing before triggering a semantic scan.
* **The Semantic Pivot:** The AI identifies "Pivot Entities" (Dates, Locations, Specific Objects) and prioritizes them over descriptive adjectives to ensure historical accuracy in the Public Domain.
* **Cross-Archive Synthesis:** The logic queries multiple archives (Openverse, NASA, Wikimedia) simultaneously and de-duplicates results based on visual similarity.

---

## 🎨 2. The Front-End Layout (The "Split-View")

The UI is designed to minimize "Context Switching." The user should never have to leave their draft to find an image.

### A. The Writing Zone (60% Width)
* **Minimalist Markdown:** A distraction-free environment.
* **The Margin-Highlight:** When the AI identifies a "Visual Hook" in a paragraph, that specific text is subtly underlined in the OpenVisualist accent color (`#00d1b2`).

### B. The Curation Zone (40% Width)
* **Sticky Vertical Alignment:** Results are anchored to the paragraph that generated them. As the user scrolls through their essay, the "Visual Suggestions" scroll in sync.
* **The Confidence Meter:** Every image card displays a "Match Strength" percentage based on the AI's verification of the image metadata against the text intent.

---

## ⚖️ 3. The Provenance Logic (Legal Safety)

One of the core design goals is **Total Legal Transparency**.

* **License Shields:** * 🛡️ **Green Shield:** Public Domain (CC0 / PDM). No attribution required.
    * 🛡️ **Yellow Shield:** Attribution Required (CC-BY).
* **The Attribution Automator:** When an image is selected, the front-end logic automatically generates a legally compliant caption string: `Photo by [Author] via [Source] ([License Link])`.

---

## 🔌 4. WordPress Integration Logic

For the "OpenVisualist Sync" plugin, the design logic follows these rules:

1.  **Block-Level Scanning:** The AI reads the content of individual Gutenberg blocks.
2.  **Sideloading Logic:** Clicking an image triggers a `POST` request that downloads the image to the local WP Media Library to ensure the site is not "hotlinking" and the image remains permanent.
3.  **Automatic Alt-Text:** The AI uses the image's metadata to pre-fill the "Alternative Text" field for SEO and Accessibility.

---

## Design Philosophy Summary
> "OpenVisualist is a tool of discovery, not generation. The design logic must prioritize the **authenticity** of the source and the **flow** of the writer."


---

## Project Mockup
https://kaushambimate.com/openvisualist-ai/
