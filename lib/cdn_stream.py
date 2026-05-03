import json
import pyarrow.parquet as pq
import pyarrow as pa
import requests
import time
import tempfile
import os
from typing import Iterator, Dict, Any, Optional


def cdn_download(repo: str, path: str, out_path: str, max_retries: int = 3) -> None:
    url = f"https://huggingface.co/datasets/{repo}/resolve/main/{path}"
    for attempt in range(1, max_retries + 1):
        try:
            with requests.get(url, stream=True, timeout=30) as r:
                r.raise_for_status()
                with open(out_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            return
        except Exception as exc:
            if attempt == max_retries:
                raise
            sleep = 2 ** attempt
            time.sleep(sleep)


def project_to_prompt_response(path: str, tmp_path: str) -> Iterator[Dict[str, Any]]:
    """Yield {prompt, response} records from JSONL or Parquet."""
    try:
        if path.endswith(".parquet"):
            tbl = pq.read_table(tmp_path, columns=["prompt", "response"])
            for i in range(tbl.num_rows):
                rec = {k: tbl[k][i].as_py() for k in ["prompt", "response"]}
                yield rec
        else:
            with open(tmp_path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    rec = json.loads(line)
                    yield {k: rec.get(k) for k in ["prompt", "response"]}
    except Exception as exc:
        # skip malformed; log and continue
        import sys
        sys.stderr.write(f"parse error {path}: {exc}\n")


def stream_shard(
    repo: str,
    file_list: list,
    shard_id: int,
    total_shards: int,
) -> Iterator[Dict[str, Any]]:
    """
    Deterministic shard assignment by slug (filename without extension).
    Downloads via CDN and projects to {prompt, response}.
    """
    def shard_for(slug: str) -> int:
        import hashlib
        h = int(hashlib.sha256(slug.encode()).hexdigest(), 16)
        return h % total_shards

    for item in file_list:
        relpath = item["path"]
        slug = os.path.splitext(os.path.basename(relpath))[0]
        if shard_for(slug) != shard_id:
            continue

        with tempfile.NamedTemporaryFile(delete=False) as tf:
            tmp_path = tf.name
        try:
            cdn_download(repo, relpath, tmp_path)
            yield from project_to_prompt_response(relpath, tmp_path)
        finally:
            try:
                os.unlink(tmp_path)
            except Exception:
                pass