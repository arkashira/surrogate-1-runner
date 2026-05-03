import io
import json
import hashlib
import pyarrow.parquet as pq
import requests

from lib.dedup import is_duplicate, store_hash  # existing dedup module

CDN_ROOT = "https://huggingface.co/datasets/axentx/surrogate-1-training-pairs/resolve/main"

def stream_cdn_parquet(cdn_url: str, columns=("prompt", "response")):
    """
    Stream a parquet file from CDN and yield rows as dicts.
    Retries and timeouts handled by caller.
    """
    with requests.get(cdn_url, stream=True, timeout=60) as r:
        r.raise_for_status()
        buf = io.BytesIO()
        for chunk in r.iter_content(chunk_size=8192):
            buf.write(chunk)
        buf.seek(0)
        table = pq.read_table(buf, columns=columns)
        for batch in table.to_batches(max_chunksize=1024):
            for row in batch.to_pylist():
                yield row

def process_and_dedup_row(row):
    """Return JSON-serializable record or None if duplicate/invalid."""
    prompt = (row.get("prompt") or "").strip()
    response = (row.get("response") or "").strip()
    if not prompt or not response:
        return None
    blob = f"{prompt}\n{response}".encode()
    md5 = hashlib.md5(blob).hexdigest()
    if is_duplicate(md5):
        return None
    store_hash(md5)
    return {"prompt": prompt, "response": response}