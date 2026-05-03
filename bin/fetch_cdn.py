#!/usr/bin/env python3
"""
Fetch a single file via CDN and yield {prompt, response} rows.
Supports .jsonl and .parquet (via pyarrow, column projection only).
"""
import sys
import json
from pathlib import Path
from typing import Iterator, Dict, Any

try:
    import pyarrow.parquet as pq
    import pyarrow as pa
    import requests
    from io import BytesIO
except ImportError as e:
    print(f"Missing dep: {e}", file=sys.stderr)
    sys.exit(1)

CDN_PREFIX = "https://huggingface.co/datasets"

def iter_parquet(cdn_url: str, repo: str) -> Iterator[Dict[str, Any]]:
    # Stream download
    resp = requests.get(cdn_url, timeout=60)
    resp.raise_for_status()
    buf = BytesIO(resp.content)
    try:
        table = pq.read_table(buf, columns=["prompt", "response"])
    except (pa.lib.ArrowInvalid, KeyError):
        # Fallback: try common aliases
        try:
            table = pq.read_table(buf, columns=["instruction", "output"])
            # rename for downstream consistency
            table = table.rename_columns(["prompt", "response"])
        except Exception:
            # Last resort: read all and project
            table = pq.read_table(buf)
            if "prompt" not in table.column_names:
                # try to find any text pair
                text_cols = [c for c in table.column_names if table.schema.field(c).type in (pa.string(), pa.large_string())]
                if len(text_cols) >= 2:
                    table = table.select([text_cols[0], text_cols[1]]).rename_columns(["prompt", "response"])
                else:
                    raise ValueError(f"No prompt/response columns found in {cdn_url}")
    df = table.to_pandas()
    for _, row in df.iterrows():
        yield {"prompt": str(row["prompt"]), "response": str(row["response"])}

def iter_jsonl(cdn_url: str) -> Iterator[Dict[str, Any]]:
    resp = requests.get(cdn_url, stream=True, timeout=60)
    resp.raise_for_status()
    for line in resp.iter_lines(decode_unicode=True):
        if not line:
            continue
        obj = json.loads(line)
        # Normalize keys
        prompt = obj.get("prompt") or obj.get("instruction") or obj.get("input") or ""
        response = obj.get("response") or obj.get("output") or obj.get("completion") or ""
        yield {"prompt": str(prompt), "response": str(response)}

def iter_file(cdn_url: str, repo: str) -> Iterator[Dict[str, Any]]:
    if cdn_url.endswith(".parquet"):
        yield from iter_parquet(cdn_url, repo)
    else:
        # assume jsonl or line-delimited json
        yield from iter_jsonl(cdn_url)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: fetch_cdn.py <repo> <cdn_url>", file=sys.stderr)
        sys.exit(1)
    repo = sys.argv[1]
    url = sys.argv[2]
    for row in iter_file(url, repo):
        print(json.dumps(row, ensure_ascii=False))