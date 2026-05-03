import json
import logging
from pathlib import Path
from typing import Dict, Iterator, Any

import pyarrow as pa
import pyarrow.parquet as pq
import requests

log = logging.getLogger(__name__)

def load_jsonl_cdn(url: str, max_lines: int | None = None) -> Iterator[Dict[str, Any]]:
    """Stream JSONL from CDN URL."""
    with requests.get(url, stream=True, timeout=30) as r:
        r.raise_for_status()
        for i, line in enumerate(r.iter_lines(decode_unicode=True)):
            if max_lines is not None and i >= max_lines:
                break
            if line:
                yield json.loads(line)

def load_parquet_cdn(url: str, columns=("prompt", "response")) -> Iterator[Dict[str, Any]]:
    """Download Parquet once from CDN and stream rows."""
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    table = pq.read_table(pa.BufferReader(resp.content), columns=columns)
    for batch in table.to_batches(max_chunksize=1024):
        rows = batch.to_pydict()
        n = len(batch)
        for k in columns:
            if len(rows[k]) != n:
                log.warning("Column length mismatch in %s", url)
        for i in range(n):
            yield {k: rows[k][i] for k in columns}

def iter_manifest_records(
    manifest_path: Path,
    max_files: int | None = None,
    max_lines_per_jsonl: int | None = None,
) -> Iterator[Dict[str, Any]]:
    """
    Yield records from manifest files via CDN.
    Skips unreadable files instead of failing the epoch.
    """
    manifest = json.loads(manifest_path.read_text())
    for i, item in enumerate(manifest["files"]):
        if max_files is not None and i >= max_files:
            break
        url = item["cdn_url"]
        try:
            if url.endswith(".jsonl"):
                yield from load_jsonl_cdn(url, max_lines=max_lines_per_jsonl)
            elif url.endswith(".parquet"):
                yield from load_parquet_cdn(url)
            else:
                log.warning("Unsupported file: %s", url)
                continue
        except Exception as exc:
            log.exception("Skipping %s: %s", url, exc)
            continue