import json
import os
import pyarrow.parquet as pq
import pyarrow as pa
import requests
from typing import Iterator, Dict, Any, List

def read_manifest(manifest_path: str) -> List[Dict[str, Any]]:
    with open(manifest_path) as f:
        return json.load(f)["files"]

def cdn_lines(url: str) -> Iterator[str]:
    with requests.get(url, stream=True, timeout=60) as r:
        r.raise_for_status()
        for line in r.iter_lines(decode_unicode=True):
            if line:
                yield line

def project_to_pair(obj: Dict[str, Any]) -> Dict[str, str]:
    return {
        "prompt": str(obj.get("prompt", "")),
        "response": str(obj.get("response", "")),
    }

def stream_jsonl_cdn(files: List[Dict[str, Any]], shard_id: int = 0, n_shards: int = 1) -> Iterator[Dict[str, str]]:
    for idx, entry in enumerate(files):
        if idx % n_shards != shard_id:
            continue
        url = entry["cdn_url"]
        if url.endswith(".jsonl"):
            for line in cdn_lines(url):
                try:
                    obj = json.loads(line)
                    yield project_to_pair(obj)
                except Exception:
                    continue
        elif url.endswith(".parquet"):
            resp = requests.get(url, timeout=120)
            resp.raise_for_status()
            table = pq.read_table(pa.BufferReader(resp.content))
            df = table.to_pandas()
            for _, row in df.iterrows():
                yield project_to_pair(row.to_dict())

def make_cdn_dataset(manifest_path: str, shard_id: int = 0, n_shards: int = 1):
    files = read_manifest(manifest_path)
    return stream_jsonl_cdn(files, shard_id=shard_id, n_shards=n_shards)