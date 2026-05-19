from __future__ import annotations

from typing import Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class Agent(BaseModel):
    """
    Represents an autonomous “agent” that can own child agents and receive tasks.
    """
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    parent_id: Optional[str] = None
    depth: int = 1                     # 1 = root, 2 = child of root, 3 = grand‑child
    context: Dict[str, str] = Field(default_factory=dict)
    children: List[str] = Field(default_factory=list)


class Task(BaseModel):
    """
    A unit of work that an agent must execute.
    """
    id: str = Field(default_factory=lambda: str(uuid4()))
    agent_id: str
    payload: Dict[str, str] = Field(default_factory=dict)
    context: Dict[str, str] = Field(default_factory=dict)
    status: str = "pending"            # could be pending / in_progress / completed