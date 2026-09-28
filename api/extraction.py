"""LLM logic for keyword harvesting.

Turns free-form essay text into a short list of concrete, searchable visual
nouns (the "Semantic Mapping" step described in the README).
"""
import os
import re
from collections import Counter
from typing import List

import openai

# Overridable via env in case gpt-3.5-turbo is retired or you want a
# sharper model for extraction — check OpenAI's current model list.
EXTRACTION_MODEL = os.getenv("OPENAI_EXTRACTION_MODEL", "gpt-3.5-turbo")

SYSTEM_PROMPT = (
    "You are a researcher. Extract 3-5 simple, concrete visual nouns from the "
    "text as a comma-separated list. No extra text."
)


def extract_keywords(content: str) -> List[str]:
    """Asks the LLM for 3-5 concrete visual search terms found in the essay.

    Falls back to a no-LLM heuristic when OPENAI_API_KEY isn't configured —
    this is what makes a public demo deployment possible with zero secrets
    and zero OpenAI cost/abuse risk. If a key IS configured but the call
    fails for some other reason (bad key, quota, network), that's a real
    misconfiguration and is allowed to raise so the caller can surface it,
    rather than being silently masked by the fallback.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return _heuristic_keywords(content)

    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=EXTRACTION_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": content},
        ],
        max_tokens=60,
    )
    raw = response.choices[0].message.content or ""
    return [k.strip() for k in raw.split(",") if k.strip()]


_STOPWORDS = frozenset("""
a an the and or but if while is are was were be been being have has had
do does did doing this that these those it its im ive youre youve i you
he she they we me him her them us my your his our their of to in on at
by for with about against between into through during before after above
below from up down out off over under again further then once here there
when where why how all any both each few more most other some such no
nor not only own same so than too very s t can will just should now as
one two three
""".split())

_WORD_RE = re.compile(r"[A-Za-z][A-Za-z'-]{2,}")


def _heuristic_keywords(content: str, limit: int = 5) -> List[str]:
    """No-LLM fallback: ranks content words by how often they recur (more
    central to the essay), breaking ties toward longer/more specific words.

    Much cruder than real semantic extraction — it has no sense of theme
    or mood, just word frequency — but it's enough to drive an Openverse
    search, which is all a public zero-key demo needs.
    """
    seen_order: List[str] = []
    counts: Counter = Counter()
    for match in _WORD_RE.findall(content):
        word = match.lower()
        if word in _STOPWORDS or len(word) <= 3:
            continue
        counts[word] += 1
        if word not in seen_order:
            seen_order.append(word)

    if not counts:
        return ["archive", "history"]

    ranked = sorted(seen_order, key=lambda w: (-counts[w], -len(w)))
    return ranked[:limit]
