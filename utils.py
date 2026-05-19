"""
Utility helpers for the surrogate‑1 API.
"""

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# ----------------------------------------------------------------------
# Public API
# ----------------------------------------------------------------------
def get_excerpt(content: Optional[str], length: int = 100) -> str:
    """
    Return the first `length` characters of `content`.

    If `content` is None, empty, or not a string, an empty string is returned.

    Parameters
    ----------
    content: Optional[str]
        The raw document text.
    length: int
        Maximum number of characters to return (default 100).

    Returns
    -------
    str
        The truncated excerpt.
    """
    if not isinstance(content, str) or not content:
        return ""
    return content[:length]


def get_recent_documents(limit: int = 5) -> List[Dict[str, Any]]:
    """
    Return the most recently updated documents.

    Each entry contains:

    * ``title`` – document title
    * ``updated_at`` – ISO‑8601 timestamp (UTC, ``Z`` suffix)
    * ``excerpt`` – first ``length`` characters of the document body

    The implementation currently uses a placeholder list.
    In production this should be replaced with a real DB/ORM query that:

    * filters to the desired set of documents,
    * orders by ``updated_at`` descending,
    * limits to ``limit`` rows.

    Parameters
    ----------
    limit: int
        Number of documents to return (default 5).

    Returns
    -------
    List[Dict[str, Any]]
        List of document dictionaries.
    """
    # ------------------------------------------------------------------
    # TODO: replace the dummy data below with an actual DB query.
    #   Example (pseudo‑SQL):
    #
    #   SELECT id, title, updated_at, content
    #   FROM documents
    #   ORDER BY updated_at DESC
    #   LIMIT :limit;
    # ------------------------------------------------------------------
    _NOW = datetime.now(timezone.utc).replace(tzinfo=None)  # naive for dummy string
    dummy_docs = [
        {
            "title": "SOP Overview",
            "updated_at": _NOW.isoformat() + "Z",
            "content": "This is a sample procedure document describing how to perform task X. It includes steps, safety notes, and references.",
        },
        {
            "title": "Data Ingestion Guide",
            "updated_at": _NOW.isoformat() + "Z",
            "content": "The ingestion pipeline processes sharded JSONL files, normalizes schema, and stores results in the central dataset repository.",
        },
        {
            "title": "Dedup Strategy",
            "updated_at": _NOW.isoformat() + "Z",
            "content": "Deduplication uses an MD5 hash of the document content to ensure uniqueness across shards and iterations.",
        },
        {
            "title": "Runner Configuration",
            "updated_at": _NOW.isoformat() + "Z",
            "content": "Each runner operates on a deterministic slice of the dataset list, defined by the slug-hash bucket in `bin/dataset-enrich.sh`.",
        },
        {
            "title": "Error Handling",
            "updated_at": _NOW.isoformat() + "Z",
            "content": "Workers catch exceptions, log stack traces, and retry transient failures to ensure reliable batch production.",
        },
    ]

    # Slice to the requested limit (in a real query this is done by the DB)
    docs = dummy_docs[:limit]

    # Build the response payload
    result: List[Dict[str, Any]] = []
    for doc in docs:
        result.append({
            "title": doc["title"],
            "updated_at": doc["updated_at"],
            "excerpt": get_excerpt(doc.get("content"), length=100),
        })

    logger.debug("Fetched %d recent documents", len(result))
    return result