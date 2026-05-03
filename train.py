import json
import os
from pathlib import Path
from typing import List, Dict

import pyarrow as pa
import pyarrow.parquet as pq
import requests
from torch.utils.data import IterableDataset

class CDNParquetDataset(IterableDataset):
    """
    Zero-HF-API dataset loader.
    Reads file_manifest.json and streams parquet files via CDN URLs.
    """

    def __init__(self, manifest_path: str, columns=("prompt", "response")):
        super().__init__()
        with open(manifest_path) as f:
            self.manifest = json.load(f)
        self.files: List[Dict] = self.manifest["files"]
        self.columns = columns

    def _stream_parquet(self, cdn_url: str):
        # Stream parquet from CDN without auth/API
        with requests.get(cdn_url, stream=True, timeout=60) as r:
            r.raise_for_status()
            # Write to temp buffer (or memory-map if small)
            data = r.content
            table = pq.read_table(pa.BufferReader(data), columns=self.columns)
            yield from table.to_pylist()

    def __iter__(self):
        for entry in self.files:
            yield from self._stream_parquet(entry["cdn_url"])

# Lightning DataModule usage
# class SurrogateDataModule(L.LightningDataModule):
#     def __init__(self, manifest_path="file_manifest.json"):
#         super().__init__()
#         self.manifest_path = manifest_path
#
#     def train_dataloader(self):
#         dataset = CDNParquetDataset(self.manifest_path)
#         return DataLoader(dataset, batch_size=...)