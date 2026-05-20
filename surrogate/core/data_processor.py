"""
Parallel ingest worker – processes a shard of data.
"""

import hashlib
import logging
from dataclasses import dataclass
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)


@dataclass
class WorkerConfig:
    """Configuration for a single worker."""
    worker_id: int
    total_workers: int
    shard_key: str = "slug-hash"

    @property
    def bucket_id(self) -> int:
        """Bucket that this worker is responsible for."""
        return self.worker_id % self.total_workers


class DataProcessor:
    """Processes data items that belong to this worker’s bucket."""

    def __init__(self, config: WorkerConfig):
        self.config = config
        self.processed = 0
        self.errors = 0

    # ------------------------------------------------------------------
    # Sharding helpers
    # ------------------------------------------------------------------
    def _bucket_for(self, item: Dict[str, Any]) -> int:
        """Deterministic bucket for an item based on the shard key."""
        value = str(item.get(self.config.shard_key, ""))
        h = hashlib.md5(value.encode()).hexdigest()
        return int(h[:8], 16) % self.config.total_workers

    def should_process(self, item: Dict[str, Any]) -> bool:
        """Return True if this worker owns the item."""
        return self._bucket_for(item) == self.config.worker_id

    # ------------------------------------------------------------------
    # Normalisation / business logic
    # ------------------------------------------------------------------
    def _normalize(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Strip whitespace, drop None values, etc."""
        return {
            k: v.strip() if isinstance(v, str) else v
            for k, v in item.items()
            if v is not None
        }

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def process_item(self, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process a single item – return None if not this worker’s bucket."""
        if not self.should_process(item):
            return None
        try:
            processed = self._normalize(item)
            self.processed += 1
            return processed
        except Exception as exc:          # pragma: no cover
            self.errors += 1
            logger.exception("Failed to process item %s", item)
            return None

    def process_batch(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process a batch, returning only the items this worker handled."""
        return [self.process_item(it) for it in items if self.process_item(it) is not None]

    def stats(self) -> Dict[str, int]:
        """Return a quick summary of what this worker did."""
        return {
            "worker_id": self.config.worker_id,
            "total_workers": self.config.total_workers,
            "processed": self.processed,
            "errors": self.errors,
        }