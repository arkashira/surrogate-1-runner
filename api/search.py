"""
Tag‑based search endpoint for knowledge articles.

Articles are stored as JSON files in a directory that can be configured
via the environment variable `KNOWLEDGE_DB_PATH`.  Each file must contain
the keys: id, title, content, tags, created_at (ISO‑8601).

The endpoint accepts a comma‑separated list of tags and returns a list
of matching articles sorted by relevance (number of matched tags, then
recency).  Only the id, title, tags and created_at fields are returned.
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List

from fastapi import APIRouter, HTTPException, Query, status

router = APIRouter()

# Default location – can be overridden by env var
BASE_DIR: Path = Path(os.getenv("KNOWLEDGE_DB_PATH", "/opt/axentx/surrogate-1/knowledge_db"))


def _load_articles() -> List[Dict]:
    """Load all article JSON files from the knowledge‑DB directory."""
    if not BASE_DIR.exists():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Knowledge DB directory {BASE_DIR} does not exist",
        )

    articles: List[Dict] = []
    for file_path in BASE_DIR.glob("*.json"):
        try:
            with file_path.open("r", encoding="utf-8") as f:
                article = json.load(f)
        except Exception as exc:  # pragma: no cover
            # Skip malformed files – they are logged by the caller
            continue

        # Validate required fields
        if all(k in article for k in ("id", "title", "content", "tags", "created_at")):
            articles.append(article)
    return articles


def _rank_articles(articles: Iterable[Dict], tags: List[str]) -> List[Dict]:
    """Return articles sorted by relevance (matching tags) and recency."""
    tag_set = set(tags)

    def relevance(article: Dict) -> int:
        return len(set(article["tags"]).intersection(tag_set))

    # Filter out zero‑relevance articles
    relevant = [a for a in articles if relevance(a) > 0]

    # Sort: first by relevance desc, then by created_at desc
    relevant.sort(
        key=lambda a: (
            relevance(a),
            datetime.fromisoformat(a["created_at"].replace("Z", "+00:00")),
        ),
        reverse=True,
    )
    return relevant


@router.get("/search", response_model=List[Dict], summary="Search articles by tags")
def search_articles(
    tags: str = Query(
        ...,
        description="Comma‑separated list of tags (e.g. 'git:commit1,jira:PROJ-2')",
    ),
) -> List[Dict]:
    """
    Search knowledge articles by tags.

    Parameters
    ----------
    tags : str
        Comma‑separated list of tags.

    Returns
    -------
    List[Dict]
        List of matching articles sorted by relevance.
    """
    tag_list = [t.strip() for t in tags.split(",") if t.strip()]
    if not tag_list:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one tag must be provided",
        )

    articles = _load_articles()
    ranked = _rank_articles(articles, tag_list)

    # Return only the required fields
    return [
        {
            "id": a["id"],
            "title": a["title"],
            "tags": a["tags"],
            "created_at": a["created_at"],
        }
        for a in ranked
    ]