"""Public Domain API integrations.

Currently wired up: Openverse. NASA and Wikimedia are named as future
archives in the README's vision but are not implemented yet — see
Cross-Archive Synthesis in design_logic.md for the intended behaviour.
"""
import os
import urllib.parse
from typing import List, Optional

import requests

from .models import ImageResult

OPENVERSE_CLIENT_ID = os.getenv("OPENVERSE_CLIENT_ID")
OPENVERSE_CLIENT_SECRET = os.getenv("OPENVERSE_CLIENT_SECRET")

OPENVERSE_TOKEN_URL = "https://api.openverse.org/v1/auth_tokens/token/"
OPENVERSE_SEARCH_URL = "https://api.openverse.org/v1/images/"

# Openverse license codes that mean "no attribution required" per
# design_logic.md's Green Shield. Everything else (by, by-sa, by-nc,
# by-nd, ...) gets the Yellow Shield — note some of those also restrict
# commercial use or derivatives, which a single shield doesn't capture;
# the license_url is always included so a user can check the specifics.
PUBLIC_DOMAIN_LICENSES = {"cc0", "pdm"}


def get_openverse_token() -> Optional[str]:
    """Requests an OAuth2 token for higher Openverse rate limits.

    Returns None if no client credentials are configured, or if the
    request fails — callers should fall back to Openverse's anonymous
    (more rate-limited) access rather than treating this as fatal.
    """
    if not OPENVERSE_CLIENT_ID or not OPENVERSE_CLIENT_SECRET:
        return None

    payload = {
        "client_id": OPENVERSE_CLIENT_ID.strip(),
        "client_secret": OPENVERSE_CLIENT_SECRET.strip(),
        "grant_type": "client_credentials",
    }
    try:
        response = requests.post(OPENVERSE_TOKEN_URL, data=payload, timeout=10)
        if response.status_code != 200:
            print(f"CRITICAL AUTH FAIL: Status {response.status_code} - {response.text}")
            return None
        return response.json().get("access_token")
    except Exception as e:
        print(f"TOKEN GEAR ERROR: {e}")
        return None


def _confidence(keyword: str, image: dict) -> int:
    """A lightweight word-overlap heuristic between the search keyword and
    the image's title/tags — NOT the "secondary vision pass" verification
    described in the README. That would need an actual image-understanding
    call and isn't implemented. Scored 55-100 so it never implies an image
    is a bad match (low-overlap results are still real search hits)."""
    kw_words = {w.lower() for w in keyword.split() if len(w) > 2}
    if not kw_words:
        return 55
    title = (image.get("title") or "").lower()
    tag_names = {t.get("name", "").lower() for t in (image.get("tags") or []) if t.get("name")}
    haystack = set(title.split()) | tag_names
    hits = sum(1 for w in kw_words if any(w in h for h in haystack))
    ratio = hits / len(kw_words)
    return round(55 + ratio * 45)


def source_images(keyword: str, token: Optional[str], page_size: int = 3) -> List[ImageResult]:
    """Searches Openverse for a specific keyword.

    Uses the OAuth token when one is available; otherwise falls back to
    Openverse's public access, which works but is more tightly rate-limited.
    """
    clean_kw = keyword.replace("[", "").replace("]", "").replace('"', "").strip()
    if not clean_kw:
        return []

    encoded_kw = urllib.parse.quote(clean_kw)
    search_url = f"{OPENVERSE_SEARCH_URL}?q={encoded_kw}&page_size={page_size}"
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        print(f"LIBRARIAN LOG [{clean_kw}]: Status {response.status_code}")
        response.raise_for_status()
        results = response.json().get("results", [])
    except Exception as e:
        print(f"LIBRARIAN GEAR ERROR: {e}")
        return []

    found_images: List[ImageResult] = []
    for img in results:
        license_code = (img.get("license") or "unknown").lower()
        image_url = img.get("url") or ""
        creator = img.get("creator") or "Public Domain Source"
        found_images.append(ImageResult(
            url=image_url,
            thumbnail=img.get("thumbnail") or image_url,
            title=img.get("title") or "Untitled Archive Piece",
            creator=creator,
            source=img.get("source") or img.get("provider") or "Openverse",
            license_code=license_code,
            license_url=img.get("license_url") or "https://creativecommons.org/",
            requires_attribution=license_code not in PUBLIC_DOMAIN_LICENSES,
            attribution=img.get("attribution") or f"Photo by {creator} via Openverse.",
            foreign_landing_url=img.get("foreign_landing_url") or image_url,
            matched_keyword=keyword,
            confidence=_confidence(keyword, img),
        ))
    return found_images
