from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Variant:
    """Represents a Claw ecosystem variant."""
    id: str
    name: str
    description: str
    version: str
    created_at: datetime
    updated_at: datetime
    tags: list[str] = None
    metadata: dict = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.metadata is None:
            self.metadata = {}