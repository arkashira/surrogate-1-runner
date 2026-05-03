from __future__ import annotations
import json, pyarrow.parquet as pq, pyarrow.compute as pc
import numpy as np, requests, io, os
from typing import List, Dict, Any

REPO = "axentx/surrogate-1-training-pairs"
BASE = f"https://huggingface.co/datasets/{REPO}/resolve/main"

def load_manifest(path: str = "train_manifest.json") -> Dict[str, Any]:
    with open(path) as f:
        return json.load(f)

def cdn_download(file_path: str) -> bytes:
    url = f"{BASE}/{file_path}"
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    return r.content

def project_to_pair(buf: bytes) -> List[Dict[str, str]]:
    tbl = pq.read_table(io.BytesIO(buf), columns=["prompt", "response"])
    # Drop rows where prompt/response are null or empty
    mask = pc.and_(
        pc.is_valid(tbl["prompt"]),
        pc.is_valid(tbl["response"]),
        pc.utf8_length(tbl["prompt"]) > 0,
        pc.utf8_length(tbl["response"]) > 0,
    )
    tbl = tbl.filter(mask)
    return [
        {"prompt": str(p), "response": str(r)}
        for p, r in zip(tbl["prompt"].to_pylist(), tbl["response"].to_pylist())
    ]

def slug_hash(slug: str) -> int:
    # Deterministic, stable across runs
    import hashlib
    return int(hashlib.md5(slug.encode()).hexdigest(), 16)

class CDNDataModule:
    def __init__(self, manifest_path: str = "train_manifest.json", shard_id: int | None = None):
        self.manifest = load_manifest(manifest_path)
        self.shard_id = shard_id  # None = all files

    def load_dataset(self) -> List[Dict[str, str]]:
        pairs = []
        for fpath in self.manifest["files"]:
            # Optional shard filtering (mirrors runner bucket logic)
            if self.shard_id is not None:
                slug = os.path.splitext(os.path.basename(fpath))[0]
                if slug_hash(slug) % 16 != self.shard_id:
                    continue
            buf = cdn_download(fpath)
            pairs.extend(project_to_pair(buf))
        return pairs