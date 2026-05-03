import os
import json
import requests
import pyarrow.parquet as pq
import pyarrow as pa
from io import BytesIO
from lib.dedup import is_duplicate, mark_seen

def stream_cdn_files(file_entries):
    for entry in file_entries:
        url = entry["cdn_url"]
        resp = requests.get(url, timeout=60)
        resp.raise_for_status()
        yield entry["path"], BytesIO(resp.content)

def run_shard(shard_id, total_shards, file_list_path=None):
    if file_list_path and os.path.exists(file_list_path):
        with open(file_list_path) as f:
            files = json.load(f)
        # Deterministic shard split by path hash
        my_files = [e for e in files if hash(e["path"]) % total_shards == shard_id]
        stream = stream_cdn_files(my_files)
    else:
        # fallback to existing HF datasets streaming path
        # (kept for compatibility)
        ...

    for path, fh in stream:
        try:
            table = pq.read_table(fh)
            # existing normalization: project to {prompt,response}, dedup
            df = table.to_pandas()
            # ... normalize to {prompt, response} ...
            for _, row in df.iterrows():
                md5 = row.get("md5") or compute_md5(row)
                if is_duplicate(md5):
                    continue
                mark_seen(md5)
                yield {"prompt": row["prompt"], "response": row["response"]}
        except Exception as exc:
            # log and continue per-file
            print(f"Error processing {path}: {exc}")
            continue