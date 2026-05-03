import hashlib
import json
from pathlib import Path
from typing import List, Dict

CDN_TEMPLATE = "https://huggingface.co/datasets/{repo}/resolve/main/{file}"

def deterministic_shard(file_path: str, date: str, n_shards: int = 16) -> int:
    key = f"{date}/{file_path}"
    return int(hashlib.md5(key.encode()).hexdigest(), 16) % n_shards

def load_snapshot(snapshot_path: Path) -> Dict:
    with open(snapshot_path) as f:
        return json.load(f)

def files_for_shard(snapshot: Dict, shard_id: int, n_shards: int = 16) -> List[str]:
    return [
        f for f in snapshot["files"]
        if deterministic_shard(f, snapshot["date"], n_shards) == shard_id
    ]