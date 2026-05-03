import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Iterator

def load_snapshot(snapshot_path: str) -> Dict:
    """Load snapshot JSON from file."""
    with open(snapshot_path) as f:
        return json.load(f)

def iter_snapshot_files(snapshot_path: str) -> Iterator[Dict]:
    """Yield file metadata dicts from snapshot."""
    snapshot = load_snapshot(snapshot_path)
    for fmeta in snapshot.get("files", []):
        yield fmeta

def get_cdn_urls(snapshot_path: str) -> List[str]:
    """Return list of CDN URLs from snapshot."""
    return [f["cdn_url"] for f in iter_snapshot_files(snapshot_path)]

def snapshot_dir() -> Path:
    """Default snapshots directory."""
    return Path("snapshots")

def latest_snapshot(date: Optional[str] = None) -> Optional[Path]:
    """Find latest snapshot file, optionally filtered by date."""
    snap_dir = snapshot_dir()
    if not snap_dir.exists():
        return None
    candidates = list(snap_dir.glob("snapshot-*.json"))
    if date:
        candidates = [p for p in candidates if date in p.name]
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)