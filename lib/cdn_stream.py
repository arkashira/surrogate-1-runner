"""
lib/cdn_stream.py

Usage:
  from lib.cdn_stream import iter_cdn_parquet
  for item in iter_cdn_parquet(file_list, max_retries=5):
      ...
"""

import json
import time
from pathlib import Path
from typing import Iterable, Dict, Any

import pyarrow.parquet as pq
import requests

CDN_TIMEOUT = 30

def _download(url: str, out_path: Path, max_retries: int = 5) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(1, max_retries + 1):
        try:
            with requests.get(url, stream=True, timeout=CDN_TIMEOUT) as r:
                r.raise_for_status()
                with open(out_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            return
        except Exception as exc:
            wait = 2 ** attempt
            print(f"CDN download attempt {attempt}/{max_retries} failed: {exc}. Retrying in {wait}s...")
            time.sleep(wait)
    raise RuntimeError(f"Failed to download {url} after {max_retries} attempts")

def iter_cdn_parquet(
    file_list_path: str,
    work_dir: str = ".cdn_cache",
    max_retries: int = 5,
    fields=("prompt", "response"),
) -> Iterable[Dict[str, Any]]:
    """
    Given file-list.json, download each parquet via CDN and yield projected rows.
    """
    with open(file_list_path, encoding="utf-8") as f:
        manifest = json.load(f)

    work_dir = Path(work_dir)
    for item in manifest["files"]:
        if not item["path"].lower().endswith(".parquet"):
            continue
        local_path = work_dir / item["path"]
        if not local_path.exists():
            _download(item["cdn_url"], local_path, max_retries=max_retries)

        table = pq.read_table(local_path, columns=fields)
        for batch in table.to_batches():
            cols = {name: batch.column(name).to_pylist() for name in fields}
            for i in range(batch.num_rows):
                yield {k: cols[k][i] for k in fields}