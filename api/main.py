"""API entry point — wires the extraction and sourcing gears together."""
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from .extraction import extract_keywords
from .models import EssayRequest, ImageResult
from .ratelimit import is_rate_limited
from .sourcing import get_openverse_token, source_images

load_dotenv()

app = FastAPI(title="OpenVisualist AI Engine")

# CORS: wide open on purpose — this is meant to be usable from a static
# page (index.html, GitHub Pages, etc.) hosted anywhere. Rate limiting
# below is what keeps a public deployment from being an open tap.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_CONTENT_CHARS = 8000


@app.post("/analyze-and-source", response_model=List[ImageResult])
async def process_essay(request: EssayRequest, http_request: Request):
    """The master switch that connects the Essay to the Gallery."""
    if not request.content or not request.content.strip():
        raise HTTPException(status_code=400, detail="Essay content cannot be empty.")

    if len(request.content) > MAX_CONTENT_CHARS:
        raise HTTPException(
            status_code=413,
            detail=f"Essay is too long (max {MAX_CONTENT_CHARS} characters).",
        )

    client_id = http_request.client.host if http_request.client else "unknown"
    if is_rate_limited(client_id):
        raise HTTPException(
            status_code=429,
            detail="Too many requests — please wait a minute and try again.",
        )

    try:
        keywords = extract_keywords(request.content)
        print(f"ANALYST GEAR: Extracted {keywords}")
    except Exception as e:
        print(f"ANALYST GEAR ERROR: {e}")
        raise HTTPException(
            status_code=502,
            detail="Keyword extraction failed — check that OPENAI_API_KEY is set and valid.",
        )

    if not keywords:
        return []

    # None is fine here — source_images() falls back to Openverse's
    # anonymous access when no OAuth token is available.
    token = get_openverse_token()

    all_results: List[ImageResult] = []
    for kw in keywords:
        all_results.extend(source_images(kw, token))

    return all_results


@app.get("/")
def health_check():
    return {"status": "OpenVisualist AI Engine is humming."}
