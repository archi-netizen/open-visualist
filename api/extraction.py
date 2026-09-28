"""LLM logic for keyword harvesting.

Turns free-form essay text into a short list of concrete, searchable visual
nouns (the "Semantic Mapping" step described in the README).
"""
import os
from typing import List

import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

# Overridable via env in case gpt-3.5-turbo is retired or you want a
# sharper model for extraction — check OpenAI's current model list.
EXTRACTION_MODEL = os.getenv("OPENAI_EXTRACTION_MODEL", "gpt-3.5-turbo")

SYSTEM_PROMPT = (
    "You are a researcher. Extract 3-5 simple, concrete visual nouns from the "
    "text as a comma-separated list. No extra text."
)


def extract_keywords(content: str) -> List[str]:
    """Asks the LLM for 3-5 concrete visual search terms found in the essay.

    Raises whatever the OpenAI client raises (e.g. AuthenticationError) —
    the caller decides how to surface that to the API consumer.
    """
    response = openai.chat.completions.create(
        model=EXTRACTION_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": content},
        ],
        max_tokens=60,
    )
    raw = response.choices[0].message.content or ""
    return [k.strip() for k in raw.split(",") if k.strip()]
