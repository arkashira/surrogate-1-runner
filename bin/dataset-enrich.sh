import json
import os
import random
import requests
from typing import Iterator, Dict

def load_cdn_shard(filelist_path: str, repo: str, shard_id: int, n_shards: int) -> Iterator[Dict]:
    with open(filelist_path) as f:
        payload = json.load(f)
    files = payload["files"]

    for path in files:
        if hash(path) % n_shards != shard_id:
            continue
        url = f"https://huggingface.co/datasets/{repo}/resolve/main/{path}"
        with requests.get(url, timeout=60) as r:
            r.raise_for_status()
            # project to {prompt, response} here
            # yield {"prompt": ..., "response": ...}
            yield {"url": url, "path": path, "raw": r.content}