import pyarrow.parquet as pq
import pyarrow as pa
import json
import sys
import hashlib
from typing import Iterator, Dict

def project_to_pair(batch: pa.Table) -> Iterator[Dict[str, str]]:
    """Project batch to {prompt, response} only."""
    prompts = batch.column("prompt").to_pylist() if "prompt" in batch.column_names else [""] * len(batch)
    responses = batch.column("response").to_pylist() if "response" in batch.column_names else [""] * len(batch)
    for p, r in zip(prompts, responses):
        if p and r:
            yield {"prompt": str(p).strip(), "response": str(r).strip()}

def stream_cdn_parquet(cdn_url: str) -> Iterator[Dict[str, str]]:
    """Stream parquet from CDN URL and yield normalized pairs."""
    try:
        pf = pq.ParquetFile(cdn_url)
        for batch in pf.iter_batches(batch_size=1024):
            yield from project_to_pair(batch)
    except Exception as e:
        print(f"CDN load failed {cdn_url}: {e}", file=sys.stderr)

def deterministic_shard(path: str, total_shards: int) -> int:
    """Deterministic shard assignment using hash."""
    return int(hashlib.md5(path.encode()).hexdigest(), 16) % total_shards

if __name__ == "__main__":
    for url in sys.stdin:
        url = url.strip()
        if url:
            for pair in stream_cdn_parquet(url):
                print(json.dumps(pair, ensure_ascii=False))