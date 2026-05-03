import json
import pyarrow.parquet as pq
import pyarrow as pa
import requests
from io import BytesIO
from typing import Dict, Iterator, List
import os

HF_DATASET = "axentx/surrogate-1-training-pairs"
CDN_ROOT = f"https://huggingface.co/datasets/{HF_DATASET}/resolve/main"

def cdn_url(path: str) -> str:
    return f"{CDN_ROOT}/{path.lstrip('/')}"

def project_to_pair(raw: Dict) -> Dict:
    """Project heterogeneous schema to {prompt, response} only."""
    return {
        "prompt": raw.get("prompt") or raw.get("input") or raw.get("question") or "",
        "response": raw.get("response") or raw.get("output") or raw.get("answer") or "",
    }

def load_parquet_cdn(path: str) -> Iterator[Dict]:
    """Stream rows from a parquet file via CDN without auth/API."""
    url = cdn_url(path)
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    table = pq.read_table(BytesIO(resp.content))
    schema_names = set(table.schema.names)

    prompt_col = table.column("prompt") if "prompt" in schema_names else None
    response_col = table.column("response") if "response" in schema_names else None

    if prompt_col is not None and response_col is not None:
        for i in range(table.num_rows):
            yield {
                "prompt": prompt_col[i].as_py(),
                "response": response_col[i].as_py(),
            }
    else:
        # Fallback projection for mixed schemas
        for i in range(table.num_rows):
            row = {k: table.column(k)[i].as_py() for k in schema_names}
            yield project_to_pair(row)

def load_jsonl_cdn(path: str) -> Iterator[Dict]:
    """Stream lines from a JSONL file via CDN."""
    url = cdn_url(path)
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    for line in resp.iter_lines(decode_unicode=True):
        if not line:
            continue
        try:
            raw = json.loads(line)
            yield project_to_pair(raw)
        except Exception as e:
            # Skip malformed lines
            continue

def load_manifest_cdn(manifest_path: str = "train/manifest.json") -> Iterator[Dict]:
    """Load all files listed in manifest via CDN."""
    with open(manifest_path) as f:
        manifest = json.load(f)
    for file_info in manifest.get("files", []):
        path = file_info["path"]
        try:
            if path.endswith(".parquet"):
                yield from load_parquet_cdn(path)
            elif path.endswith(".jsonl"):
                yield from load_jsonl_cdn(path)
            else:
                print(f"Unsupported file type, skipping: {path}")
        except Exception as e:
            print(f"Skipping {path}: {e}")