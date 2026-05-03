import io
import json
import time
from typing import Dict, Iterator

import pyarrow.parquet as pq
import requests

CDN_TEMPLATE = "https://huggingface.co/datasets/{repo}/resolve/main/{path}"

def cdn_url(repo: str, path: str) -> str:
    return CDN_TEMPLATE.format(repo=repo, path=path)

def fetch_with_retry(url: str, max_retries: int = 5, backoff: float = 1.0) -> bytes:
    for attempt in range(max_retries):
        try:
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            return resp.content
        except Exception as exc:
            if attempt == max_retries - 1:
                raise
            time.sleep(backoff * (2 ** attempt))
    raise RuntimeError("unreachable")

def project_row(raw: Dict[str, object]) -> Dict[str, str]:
    """
    Best-effort projection to {prompt, response}.
    Handles common schema variants seen in surrogate-1 mirrors.
    """
    prompt = raw.get("prompt") or raw.get("input") or raw.get("question") or ""
    response = raw.get("response") or raw.get("output") or raw.get("answer") or ""
    return {"prompt": str(prompt), "response": str(response)}

def stream_parquet_from_cdn(repo: str, path: str) -> Iterator[Dict[str, str]]:
    data = fetch_with_retry(cdn_url(repo, path))
    table = pq.read_table(io.BytesIO(data))
    for batch in table.to_batches(max_chunksize=1000):
        cols = {name: batch.column(name).to_pylist() for name in batch.schema.names}
        n = len(next(iter(cols.values()))) if cols else 0
        for i in range(n):
            raw = {k: v[i] for k, v in cols.items()}
            yield project_row(raw)

def stream_jsonl_from_cdn(repo: str, path: str) -> Iterator[Dict[str, str]]:
    data = fetch_with_retry(cdn_url(repo, path))
    for line in io.BytesIO(data).read().splitlines():
        if not line.strip():
            continue
        raw = json.loads(line)
        yield project_row(raw)

def stream_from_cdn(repo: str, path: str) -> Iterator[Dict[str, str]]:
    if path.endswith(".parquet"):
        yield from stream_parquet_from_cdn(repo, path)
    elif path.endswith(".jsonl"):
        yield from stream_jsonl_from_cdn(repo, path)
    else:
        raise ValueError(f"Unsupported file type: {path}")