import json
import requests
from pathlib import Path

def load_via_cdn(manifest_path: str):
    with open(manifest_path) as f:
        m = json.load(f)

    for fmeta in m["files"]:
        url = fmeta["cdn_url"]
        # Stream download with no Authorization header (public CDN).
        resp = requests.get(url, stream=True, timeout=60)
        resp.raise_for_status()
        # Process bytes (e.g., parse parquet/jsonl) and project to {prompt,response}.
        yield process(resp.raw)