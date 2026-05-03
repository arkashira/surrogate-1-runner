import json
import hashlib
import os
from typing import List, Dict, Any

def load_snapshot(path: str = "snapshot.json") -> Dict[str, Any]:
    with open(path) as f:
        return json.load(f)

def deterministic_shard(slug: str, total_shards: int = 16) -> int:
    """Map slug to shard 0..15 deterministically."""
    digest = hashlib.md5(slug.encode()).hexdigest()
    return int(digest, 16) % total_shards

def cdn_url(repo: str, filepath: str) -> str:
    """CDN URL that bypasses HF API auth checks."""
    return f"https://huggingface.co/datasets/{repo}/resolve/main/{filepath}"

def files_for_shard(snapshot: Dict[str, Any], shard_id: int, total_shards: int = 16) -> List[Dict[str, Any]]:
    return [
        f for f in snapshot.get("files", [])
        if deterministic_shard(f.get("slug", ""), total_shards) == shard_id
    ]