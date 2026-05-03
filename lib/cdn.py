import json
import pyarrow.parquet as pq
import pyarrow as pa
import requests
from io import BytesIO
from typing import List, Dict, Any

CDN_TEMPLATE = "https://huggingface.co/datasets/{repo}/resolve/main/{path}"

def fetch_parquet_via_cdn(repo: str, path: str) -> pa.Table:
    url = CDN_TEMPLATE.format(repo=repo, path=path)
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    return pq.read_table(BytesIO(resp.content))

def project_pair(row: Dict[str, Any]) -> Dict[str, str]:
    # Best-effort projection to {prompt, response}
    prompt = row.get("prompt") or row.get("input") or row.get("question") or ""
    response = row.get("response") or row.get("output") or row.get("answer") or ""
    return {"prompt": str(prompt), "response": str(response)}

def stream_cdn_files(repo: str, files: List[str], max_files: int = None):
    count = 0
    for path in files:
        if max_files is not None and count >= max_files:
            break
        try:
            tbl = fetch_parquet_via_cdn(repo, path)
            for batch in tbl.to_batches(max_chunksize=1000):
                for row in batch.to_pylist():
                    yield project_pair(row)
            count += 1
        except Exception as exc:
            # Log and skip bad files; don't kill whole shard
            print(f"skip {path}: {exc}", flush=True)
            continue