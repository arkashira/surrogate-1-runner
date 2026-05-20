"""
A battle‑tested, single‑responsibility processor for JSON datasets.

Features
--------
* Shard‑aware: split a directory into N shards for parallel runs.
* Deduplication: keeps a persistent MD5 hash set so a file is never processed twice.
* Robust I/O: uses pathlib, context‑managers, and detailed logging.
* Extensible: expose a `process_record(record: dict) -> dict | None` hook for custom logic.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Set

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler(sys.stdout))


class Processor:
    """Process a JSON file once and write the result to an output directory."""

    def __init__(
        self,
        shard_id: int,
        dataset_path: Path,
        output_path: Path,
        md5_store_path: Path,
        shard_count: int = 16,
    ) -> None:
        self.shard_id = shard_id
        self.dataset_path = dataset_path
        self.output_path = output_path
        self.md5_store_path = md5_store_path
        self.shard_count = shard_count

        self.md5_store: Set[str] = set()
        self._load_md5_store()

    # ------------------------------------------------------------------ #
    #  Persistence helpers
    # ------------------------------------------------------------------ #
    def _load_md5_store(self) -> None:
        if self.md5_store_path.exists():
            try:
                self.md5_store = set(json.loads(self.md5_store_path.read_text()))
                log.debug(f"Loaded {len(self.md5_store)} MD5 hashes")
            except Exception as exc:
                log.warning(f"Failed to load MD5 store: {exc}")

    def _save_md5_store(self) -> None:
        try:
            self.md5_store_path.write_text(json.dumps(list(self.md5_store)))
            log.debug(f"Saved {len(self.md5_store)} MD5 hashes")
        except Exception as exc:
            log.error(f"Failed to save MD5 store: {exc}")

    # ------------------------------------------------------------------ #
    #  Core processing
    # ------------------------------------------------------------------ #
    def _file_md5(self, path: Path) -> str:
        """Return the MD5 of the canonical JSON representation."""
        data = json.loads(path.read_text())
        # Sort keys to make hash deterministic
        canonical = json.dumps(data, sort_keys=True, separators=(",", ":"))
        return hashlib.md5(canonical.encode("utf-8")).hexdigest()

    def process_file(self, path: Path) -> None:
        """Process a single file – skip if duplicate."""
        md5 = self._file_md5(path)
        if md5 in self.md5_store:
            log.debug(f"Skipping duplicate: {path.name}")
            return

        # Hook for custom logic – default is identity
        record = json.loads(path.read_text())
        processed = self.process_record(record)
        if processed is None:
            log.debug(f"Record filtered out: {path.name}")
            return

        # Persist
        out_path = self.output_path / f"processed_{path.name}"
        out_path.write_text(json.dumps(processed, indent=2, sort_keys=True))
        self.md5_store.add(md5)
        log.info(f"Processed: {path.name} -> {out_path.name}")

    def process_record(self, record: Dict) -> Dict | None:
        """Override in subclasses to transform a record."""
        return record

    # ------------------------------------------------------------------ #
    #  Sharding logic
    # ------------------------------------------------------------------ #
    def _shard_files(self) -> List[Path]:
        all_files = sorted(self.dataset_path.glob("*.json"))
        shard_size = (len(all_files) + self.shard_count - 1) // self.shard_count
        start = self.shard_id * shard_size
        end = start + shard_size
        return all_files[start:end]

    def run(self) -> None:
        """Entry‑point for a single shard."""
        self.output_path.mkdir(parents=True, exist_ok=True)
        for file_path in self._shard_files():
            try:
                self.process_file(file_path)
            except Exception as exc:
                log.error(f"Failed to process {file_path}: {exc}")
        self._save_md5_store()