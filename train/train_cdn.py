#!/usr/bin/env python3
"""
CDN-only training data loader.
Zero HF API calls during training — avoids rate limits and CastErrors.
"""
import json
import pyarrow.parquet as pq
import pyarrow.compute as pc
from pathlib import Path
from typing import Iterator, Dict, Any
import requests
from torch.utils.data import IterableDataset

BASE = "https://huggingface.co/datasets/axentx/surrogate-1-training-pairs/resolve/main"
MANIFEST = Path(__file__).parent / "manifest.json"

class CDNPairDataset(IterableDataset):
    def __init__(self, date: str = None):
        manifest = json.loads(MANIFEST.read_text())
        files = manifest["shards"]
        if date:
            files = {date: files[date]} if date in files else {}
        self.urls = [
            f"{BASE}/batches/public-merged/{f}"
            for fs in files.values() for f in fs
        ]

    def _stream_file(self, url: str) -> Iterator[Dict[str, Any]]:
        # Stream download + column projection to avoid full-schema decode
        with requests.get(url, stream=True, timeout=60) as r:
            r.raise_for_status()
            with open("/tmp/temp.parquet", "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        pf = pq.ParquetFile("/tmp/temp.parquet")
        # Project only prompt/response; ignore extra cols to prevent CastError
        cols = {"prompt", "response"}
        available = set(pf.schema.names)
        proj = list(cols & available)
        if not proj:
            return

        for batch in pf.iter_batches(batch_size=512, columns=proj):
            df = batch.to_pydict()
            for i in range(len(df["prompt"])):
                yield {"prompt": df["prompt"][i], "response": df["response"][i]}

    def __iter__(self):
        for url in self.urls:
            yield from self._stream_file(url)

# Example usage in Lightning
if __name__ == "__main__":
    from torch.utils.data import DataLoader
    ds = CDNPairDataset()
    dl = DataLoader(ds, batch_size=8)
    for batch in dl:
        print(batch)
        break