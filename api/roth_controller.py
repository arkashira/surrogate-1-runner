"""
Roth (Guide) API controller.

Provides endpoints for retrieving the guide steps.  The primary endpoint
supports an optional ``q`` query parameter that performs a simple keyword
search over the ``title`` and ``description`` fields of each step.

Search semantics:
* Case‑insensitive substring match.
* Results are ordered by relevance – a match in the title is considered more
  relevant than a match in the description.
* If ``q`` is omitted or empty, the full list of steps is returned.
"""

from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional, Dict, Any

router = APIRouter()


# ---------------------------------------------------------------------------
# Mock data source
# ---------------------------------------------------------------------------
# In the real service the steps are loaded from a database or a JSON file.
# For the purpose of this controller we keep a simple in‑memory list.
# Each step is a dict with at least ``id``, ``title`` and ``description``.
# ---------------------------------------------------------------------------
_GUIDE_STEPS: List[Dict[str, Any]] = [
    {
        "id": 1,
        "title": "Initialize the repository",
        "description": "Clone the repo and set up the virtual environment.",
    },
    {
        "id": 2,
        "title": "Configure the dataset",
        "description": "Edit `config.yaml` to point at the desired dataset.",
    },
    {
        "id": 3,
        "title": "Run the ingestion pipeline",
        "description": "Execute `bin/run_ingest.sh` to start processing.",
    },
    # ... more steps would be loaded in production ...
]


def _search_steps(keyword: str) -> List[Dict[str, Any]]:
    """
    Return steps whose title or description contains ``keyword`` (case‑insensitive).

    The list is sorted by relevance:
        * title match → relevance score 2
        * description match → relevance score 1
    Steps with equal relevance retain their original order.
    """
    lowered = keyword.lower()
    results: List[Dict[str, Any]] = []

    for step in _GUIDE_STEPS:
        title_match = lowered in step["title"].lower()
        desc_match = lowered in step["description"].lower()

        if title_match or desc_match:
            relevance = 2 if title_match else 1
            # Store relevance temporarily for sorting
            results.append({**step, "_relevance": relevance})

    # Sort by relevance descending, then by original insertion order (stable sort)
    results.sort(key=lambda s: s["_relevance"], reverse=True)

    # Strip the temporary field before returning
    for r in results:
        r.pop("_relevance", None)

    return results


@router.get("/guide", response_model=List[Dict[str, Any]])
def get_guide_steps(q: Optional[str] = Query(None, description="Keyword to search for")):
    """
    Retrieve guide steps.

    If ``q`` is provided, only steps whose title or description contain the
    keyword are returned, ordered by relevance.  When no steps match, an
    empty list is returned (the front‑end can display a “no results” message).
    """
    if q is None or q.strip() == "":
        # No search term – return the full list
        return _GUIDE_STEPS

    results = _search_steps(q.strip())
    return results