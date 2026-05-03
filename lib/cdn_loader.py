import json, hashlib, pyarrow.parquet as pq, pyarrow as pa, io, requests, time
from typing import List, Dict, Iterator

CDN_TIMEOUT = 30
MAX_RETRIES = 5

def load_manifest(path: str) -> List[Dict]:
    with open(path) as f:
        return json.load(f)["files"]

def shard_files(files: List[Dict], shard_id: int, total_shards: int = 16) -> List[Dict]:
    return [f for i, f in enumerate(files) if i % total_shards == shard_id]

def stream_cdn_parquet(url: str) -> Iterator[pa.Table]:
    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.get(url, timeout=CDN_TIMEOUT, stream=True)
            resp.raise_for_status()
            buf = io.BytesIO(resp.content)
            yield pq.read_table(buf, columns=["prompt", "response"])
            break
        except Exception as e:
            if attempt == MAX_RETRIES - 1:
                raise
            time.sleep(2 ** attempt)

def normalize_table(t: pa.Table) -> Iterator[Dict]:
    df = t.to_pandas()
    for _, row in df.iterrows():
        prompt = str(row.get("prompt", ""))
        response = str(row.get("response", ""))
        if prompt.strip() and response.strip():
            yield {"prompt": prompt.strip(), "response": response.strip()}

def process_shard(manifest_path: str, shard_id: int) -> Iterator[Dict]:
    files = load_manifest(manifest_path)
    for f in shard_files(files, shard_id):
        try:
            for tbl in stream_cdn_parquet(f["cdn_url"]):
                yield from normalize_table(tbl)
        except Exception as e:
            print(f"Failed to process {f['path']}: {e}")