import json
import os
from typing import List, Dict

def load_manifest(path: str) -> List[Dict]:
    with open(path) as f:
        data = json.load(f)
    return data.get("files", [])

def iter_cdn_urls(manifest_path: str):
    for entry in load_manifest(manifest_path):
        yield entry["cdn_url"], entry["path"]