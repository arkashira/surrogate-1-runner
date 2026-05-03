import json
import os
from pathlib import Path
from typing import Dict, Iterator

import pyarrow.parquet as pq
import requests
from torch.utils.data import IterableDataset

MANIFEST_PATH = os.getenv("FILE_MANIFEST", "file_manifest.json")

class CDNParquetIterable(IterableDataset):
    """Stream parquet files from CDN using manifest (zero HF API calls)."""

    def __init__(self, manifest_path: str = MANIFEST_PATH, columns=None):
        super().__init__()
        self.manifest_path = manifest_path
        self.columns = columns

    def _iter_files(self) -> Iterator[Dict]:
        with open(self.manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for meta in data["files"]:
            yield meta

    def _stream_parquet(self, cdn_url: str):
        resp = requests.get(cdn_url, stream=True, timeout=60)
        resp.raise_for_status()
        import io
        buf = io.BytesIO()
        for chunk in resp.iter_content(chunk_size=8192):
            buf.write(chunk)
        buf.seek(0)
        table = pq.read_table(buf, columns=self.columns)
        yield from table.to_pylist()

    def __iter__(self):
        for meta in self._iter_files():
            try:
                yield from self._stream_parquet(meta["cdn_url"])
            except Exception as exc:
                print(f"Skipping {meta['path']}: {exc}")
                continue