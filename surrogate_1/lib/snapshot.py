import json
import os
from typing import List, Dict

def load_snapshot(snapshot_path: str) -> Dict:
    with open(snapshot_path) as f:
        data = json.load(f)
    return data

def iter_cdn_urls(manifest: Dict):
    for item in manifest.get("files", []):
        yield item["cdn_url"], item["basename"], item["path"]