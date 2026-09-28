"""Minimal in-memory per-client rate limiter for the public demo endpoint.

Deliberately simple (no Redis, no new dependency): good enough to stop one
noisy client from exhausting Openverse's anonymous rate limit for everyone
else hitting the same free-tier deployment. It resets on restart and only
tracks state within a single process — it is not a defense against a
determined attacker, and Render's free tier only runs one instance anyway,
so that tradeoff is fine here.
"""
import time
from collections import defaultdict, deque
from threading import Lock

WINDOW_SECONDS = 60
MAX_REQUESTS_PER_WINDOW = 10

_hits: dict = defaultdict(deque)
_lock = Lock()


def is_rate_limited(client_id: str) -> bool:
    """Records a hit for client_id and reports whether it's over the limit.

    client_id is typically the caller's IP. Behind Render's proxy this is
    the real client IP for standard web services; if you put this behind a
    different proxy that doesn't preserve it, every caller may share one
    bucket — acceptable degradation for a demo limiter, not a security
    control.
    """
    now = time.monotonic()
    with _lock:
        hits = _hits[client_id]
        while hits and now - hits[0] > WINDOW_SECONDS:
            hits.popleft()
        if len(hits) >= MAX_REQUESTS_PER_WINDOW:
            return True
        hits.append(now)
        return False
