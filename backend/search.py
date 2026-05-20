"""
Real-time search utilities for AI-generated summaries.

The dashboard will call :func:`search_summaries` on each keystroke.
The implementation is deliberately lightweight: it loads the summaries once 
(on first call) from the JSON file ``data/ai_summaries.json`` and performs 
case-insensitive substring matching against the ``title`` and ``content`` fields.

The function returns a list of dictionaries limited to the top 10 matches, 
sorted by relevance (simple length-based heuristic).
"""

import json
import os
import threading
from typing import List, Dict

# Path to the JSON file that stores AI-generated summaries.
# The file is expected to be a list of objects:
# [
#   {"id": "uuid", "title": "...", "content": "..."},
#   ...
# ]
_SUMMARIES_PATH = os.path.join(
    os.path.dirname(__file__), "..", "data", "ai_summaries.json"
)

# Cached summaries and a lock to protect lazy loading in multi-threaded environments.
_summaries_cache: List[Dict] = []
_cache_lock = threading.Lock()


def _load_summaries() -> List[Dict]:
    """Load summaries from the JSON file into memory (once)."""
    global _summaries_cache
    with _cache_lock:
        if _summaries_cache:
            return _summaries_cache
        try:
            with open(_SUMMARIES_PATH, "r", encoding="utf-8") as f:
                _summaries_cache = json.load(f)
        except FileNotFoundError:
            # Gracefully handle missing data – return empty list.
            _summaries_cache = []
        except json.JSONDecodeError:
            # Corrupt file – also treat as empty.
            _summaries_cache = []
        return _summaries_cache


def _match_score(summary: Dict, query: str) -> int:
    """
    Simple relevance scoring:
    - +2 if query appears in title
    - +1 if query appears in content
    - Shorter summaries are preferred when scores tie.
    """
    q = query.lower()
    score = 0
    if q in summary.get("title", "").lower():
        score += 2
    if q in summary.get("content", "").lower():
        score += 1
    return score


def search_summaries(query: str, limit: int = 10) -> List[Dict]:
    """
    Return up to ``limit`` AI-generated summaries that match ``query``.
    The search is case-insensitive and runs in O(N) where N is the
    number of stored summaries – acceptable for the current dataset size.

    Parameters
    ----------
    query: str
        Keyword(s) typed by the user.
    limit: int, optional
        Maximum number of results to return (default 10).

    Returns
    -------
    List[Dict]
        List of matching summary dicts, each containing at least ``id``,
        ``title`` and ``content`` keys.
    """
    if not query:
        return []

    summaries = _load_summaries()
    lowered_query = query.strip().lower()
    
    # Filter and score
    matches = [
        (summary, _match_score(summary, lowered_query))
        for summary in summaries
        if lowered_query in summary.get("title", "").lower()
        or lowered_query in summary.get("content", "").lower()
    ]

    # Sort by score descending, then by length of content ascending
    matches.sort(
        key=lambda pair: (-pair[1], len(pair[0].get("content", "")))
    )

    # Return only the summary dicts, limited to ``limit``
    return [summary for summary, _ in matches[:limit]]