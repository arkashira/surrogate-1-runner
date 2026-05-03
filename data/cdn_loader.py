import json, io, pyarrow as pa, pyarrow.parquet as pq, requests
from torch.utils.data import IterableDataset

class CDNParquetPairs(IterableDataset):
    def __init__(self, manifest_path, columns=("prompt", "response")):
        with open(manifest_path) as f:
            self.manifest = json.load(f)
        self.columns = columns

    def _stream_file(self, cdn_url):
        # CDN fetch — no Authorization header, bypasses HF API rate limits
        resp = requests.get(cdn_url, timeout=60)
        resp.raise_for_status()
        return io.BytesIO(resp.content)

    def __iter__(self):
        for f in self.manifest["files"]:
            try:
                buf = self._stream_file(f["cdn_url"])
                table = pq.read_table(buf, columns=self.columns)
                for row in table.to_pylist():
                    yield row
            except Exception as exc:
                # Log and skip bad files; don't crash entire epoch
                print(f"Skipping {f['path']}: {exc}")
                continue