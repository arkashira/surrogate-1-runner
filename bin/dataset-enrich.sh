import json
import requests
import pyarrow as pa
import io

with open("snapshots/2026-04-29-manifest.json") as f:
    files = json.load(f)

def cdn_fetch(path):
    url = f"https://huggingface.co/datasets/axentx/surrogate-1-training-pairs/resolve/main/{path}"
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    return resp.content

# Example: stream parquet files and project to {prompt, response}
for f in files:
    if not f["path"].endswith(".parquet"):
        continue
    buf = io.BytesIO(cdn_fetch(f["path"]))
    table = pa.parquet.read_table(buf)
    # project to schema you need