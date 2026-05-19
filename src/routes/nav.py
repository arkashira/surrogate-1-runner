from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict

from ..database import get_db, Base, engine
from ..models import NavGraph  # <-- your existing ORM model

# --------------------------------------------------------------------------- #
# 1️⃣  Pydantic response models
# --------------------------------------------------------------------------- #
class PageNode(BaseModel):
    """A unique page in the navigation graph."""
    id: int
    title: str
    url: str


class NavTree(BaseModel):
    """Full navigation tree – nodes + edges."""
    nodes: List[PageNode]
    edges: List[Dict[str, int]]  # {"from": node_id, "to": node_id}


# --------------------------------------------------------------------------- #
# 2️⃣  FastAPI router
# --------------------------------------------------------------------------- #
router = APIRouter()


@router.get("/api/navigation", response_model=NavTree)
def get_navigation(db: Session = Depends(get_db)) -> NavTree:
    """
    Return the navigation graph as a tree structure.

    * Nodes are unique pages (id, title, url).
    * Edges are stored as foreign‑key pairs (source_id → target_id).
    """
    # 2.1  Pull all rows
    rows = db.query(NavGraph).all()
    if not rows:
        raise HTTPException(status_code=404, detail="Navigation graph not found")

    # 2.2  Build node set (unique by id)
    node_map: Dict[int, PageNode] = {}
    edges: List[Dict[str, int]] = []

    for row in rows:
        # source node
        if row.source_id not in node_map:
            node_map[row.source_id] = PageNode(
                id=row.source_id,
                title=row.source_title,
                url=row.source_url,
            )
        # target node
        if row.target_id not in node_map:
            node_map[row.target_id] = PageNode(
                id=row.target_id,
                title=row.target_title,
                url=row.target_url,
            )
        # edge
        edges.append({"from": row.source_id, "to": row.target_id})

    return NavTree(nodes=list(node_map.values()), edges=edges)