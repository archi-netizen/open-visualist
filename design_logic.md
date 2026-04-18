🧠 OpenVisualist Design System
This document outlines the front-end logic and UX principles for the OpenVisualist interface.

1. The Contextual Scan (Input Logic)
Debounce Mechanism: The AI does not trigger on every keystroke. It waits for a 3000ms pause in typing or a "Paragraph Break" (Enter key) before analyzing the text block.

Entity Extraction: The logic prioritizes Nouns and Historical Eras found in the text to build the search query.

2. The Split-Pane Orchestration
Fixed Writing Zone: The left 60% of the screen is a minimalist Markdown editor.

Fluid Sourcing Zone: The right 40% is the "Live Archive."

The "Anchor" Logic: As the user scrolls through their essay, the image results in the right pane "stick" to the paragraph that generated them.

3. The "Confidence" Visualizer
Each sourced image must display a Match Score:

High (85%+): Solid green border.

Medium (50-84%): Dashed teal border.

Low (<50%): Hidden by default to prevent "clutter."
