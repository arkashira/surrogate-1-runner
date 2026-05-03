from pathlib import Path
import json, hashlib, requests, pyarrow.csv as pc, pyarrow.parquet as pq
from torch.utils.data import IterableDataset

CDN = "https://huggingface.co/datasets"

class CdnDataset(IterableDataset):
    def __init__(self, manifest_path, shard_id=0, num_shards=1):
        manifest = json.loads(Path(manifest_path).read_text())
        self.folder = manifest["folder"]
        # deterministic sharding by filename
        files = sorted(manifest["files"])
        self.files = [
            f for f in files
            if hashlib.md5(f.encode()).digest()[0] % num_shards == shard_id
        ]
        self.shard_id = shard_id
        self.num_shards = num_shards

    def __iter__(self):
        for fname in self.files:
            url = f"{CDN}/{self.folder}/{fname}"
            try:
                with requests.get(url, stream=True) as r:
                    r.raise_for_status()
                    if fname.endswith(".parquet"):
                        table = pq.read_table(pq.ParquetFile(r.raw))
                    else:
                        # project only prompt/response to avoid CastError
                        table = pc.read_csv(
                            r.raw,
                            read_options=pc.ReadOptions(column_names=["prompt", "response"]),
                            parse_options=pc.ParseOptions(delimiter="\t"),
                        )
                    for batch in table.to_batches(max_chunksize=1024):
                        cols = batch.to_pydict()
                        for p, r_ in zip(cols.get("prompt", []), cols.get("response", [])):
                            if p and r_:
                                yield {"prompt": p, "response": r_}
            except Exception as exc:
                print(f"Skipping {url}: {exc}")
                continue