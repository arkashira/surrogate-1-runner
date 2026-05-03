import json
import os
from pathlib import Path
from typing import Iterator, Dict, Any
from huggingface_hub import hf_hub_download

def load_snapshot(path: str) -> Dict[str, Any]:
    with open(path) as f:
        return json.load(f)

def shard_files(snapshot_path: str, shard_id: int, total_shards: int = 16) -> Iterator[Dict[str, str]]:
    """Yield files assigned to this shard by deterministic hash."""
    snap = load_snapshot(snapshot_path)
    for entry in snap["files"]:
        path = entry["path"]
        if hash(path) % total_shards == shard_id:
            yield {
                "remote_path": path,
                "repo": snap["repo"],
                "local_path": hf_hub_download(
                    repo_id=snap["repo"],
                    filename=path,
                    repo_type="dataset",
                )
            }

def cdn_url(repo: str, path: str) -> str:
    return f"https://huggingface.co/datasets/{repo}/resolve/main/{path}"