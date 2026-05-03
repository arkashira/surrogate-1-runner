import json, requests, pyarrow.parquet as pq, time
from torch.utils.data import IterableDataset

class CDNParquetDataset(IterableDataset):
    def __init__(self, filelist_path, repo="axentx/surrogate-1-training-pairs"):
        with open(filelist_path) as f:
            self.files = json.load(f)["files"]
        self.repo = repo
        self.base = f"https://huggingface.co/datasets/{repo}/resolve/main"

    def _download_with_retry(self, url, max_retries=3, backoff=1.0):
        for attempt in range(max_retries):
            try:
                with requests.get(url, stream=True, timeout=30) as r:
                    r.raise_for_status()
                    with open("/tmp/current.parquet", "wb") as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                return
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                sleep = backoff * (2 ** attempt)
                print(f"CDN download failed (attempt {attempt+1}): {e}. Retrying in {sleep}s...")
                time.sleep(sleep)

    def __iter__(self):
        for path in self.files:
            url = f"{self.base}/{path}"
            self._download_with_retry(url)
            table = pq.read_table("/tmp/current.parquet", columns=["prompt", "response"])
            for row in table.to_pylist():
                yield row