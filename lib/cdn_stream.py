import pyarrow.parquet as pq
import pyarrow as pa
import requests
import io
import os
import time
from typing import Iterator, Dict, Any

CDN_TIMEOUT = int(os.getenv("CDN_TIMEOUT", "60"))
MAX_RETRIES = int(os.getenv("CDN_RETRIES", "3"))
BACKOFF_FACTOR = float(os.getenv("CDN_BACKOFF", "1.5"))

def _fetch_with_retry(url: str) -> bytes:
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.get(url, timeout=CDN_TIMEOUT)
            resp.raise_for_status()
            return resp.content
        except Exception as exc:
            if attempt == MAX_RETRIES:
                raise
            sleep = BACKOFF_FACTOR ** attempt
            print(f"CDN retry {attempt}/{MAX_RETRIES} for {url}: {exc} — sleeping {sleep:.1f}s")
            time.sleep(sleep)

def cdn_parquet_reader(cdn_url: str, columns=("prompt", "response")) -> pa.Table:
    """Download a single parquet via CDN and project columns without HF API."""
    buf = io.BytesIO(_fetch_with_retry(cdn_url))
    table = pq.read_table(buf, columns=columns)
    return table

def iter_cdn_shard(cdn_urls: list[str], columns=("prompt", "response")) -> Iterator[Dict[str, Any]]:
    """Yield rows from multiple CDN parquet files."""
    for url in cdn_urls:
        try:
            table = cdn_parquet_reader(url, columns=columns)
            for batch in table.to_batches(max_chunksize=1024):
                for i in range(batch.num_rows):
                    row = {col: batch.column(col)[i].as_py() for col in columns}
                    yield row
        except Exception as exc:
            # Log and skip bad files; don't kill entire shard
            print(f"CDN read failed {url}: {exc}")
            continue