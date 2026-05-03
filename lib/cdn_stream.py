#!/usr/bin/env python3
"""
CDN-only data loader for surrogate-1.

Usage:
  from lib.cdn_stream import CDNParquetDataset
  dataset = CDNParquetDataset("file-list.json", shard_id=0, num_shards=16)
  for row in dataset:
      print(row)
"""

import io
import json
from pathlib import Path
from typing import Dict, Iterator, Optional

import pyarrow as pa
import pyarrow.parquet as pq
import requests

HF_REPO = "axentx/surrogate-1-training-pairs"  # override via env if needed

def normalize_record(obj: Dict) -> Dict:
    """Project to {prompt, response} only; keep attribution in filename pattern."""
    prompt = obj.get("prompt") or obj.get("input") or obj.get("text") or ""
    response = obj.get("response") or obj.get("output") or obj.get("completion") or ""
    return {"prompt": str(prompt), "response": str(response)}

class CDNParquetDataset:
    def __init__(
        self,
        file_list_path: str,
        shard_id: Optional[int] = None,
        num_shards: Optional[int] = None,
        repo: Optional[str] = None,
    ):
        self.repo = repo or HF_REPO
        with open(file_list_path) as f:
            self.files = [json.loads(ln)["path"] for ln in f if ln.strip()]

        if shard_id is not None and num_shards is not None:
            self.files = [p for i, p in enumerate(self.files) if i % num_shards == shard_id]

    def _stream_file(self, path: str) -> Iterator[Dict]:
        url = f"https://huggingface.co/datasets/{self.repo}/resolve/main/{path}"
        resp = requests.get(url, timeout=60)
        resp.raise_for_status()
        content = resp.content

        try:
            table = pq.read_table(io.BytesIO(content))
            for row in table.to_pylist():
                nr = normalize_record(row)
                if nr["prompt"] and nr["response"]:
                    yield nr
        except Exception:
            # Fallback: line-delimited JSON
            for line in content.decode("utf-8", errors="ignore").strip().splitlines():
                if not line.strip():
                    continue
                try:
                    row = json.loads(line)
                    nr = normalize_record(row)
                    if nr["prompt"] and nr["response"]:
                        yield nr
                except Exception:
                    continue

    def __iter__(self) -> Iterator[Dict]:
        for path in self.files:
            yield from self._stream_file(path)