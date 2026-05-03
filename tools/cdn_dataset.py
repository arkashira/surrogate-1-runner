import io
import json
from typing import Dict, Iterator

import pyarrow.parquet as pq
import requests

class CDNParquetIterable:
    """
    Stream parquet files from CDN URLs listed in manifest.
    Projects each row to {prompt, response} only.
    """
    def __init__(self, manifest_path: str):
        with open(manifest_path) as f:
            self.files = json.load(f)

    def __iter__(self) -> Iterator[Dict[str, str]]:
        for item in self.files:
            url = item["cdn_url"]
            resp = requests.get(url, stream=True, timeout=120)
            resp.raise_for_status()

            buf = io.BytesIO(resp.content)
            table = pq.read_table(buf)

            # Validate schema
            for col in ("prompt", "response"):
                if col not in table.column_names:
                    raise ValueError(f"Missing column '{col}' in {url}")

            for i in range(table.num_rows):
                yield {
                    "prompt": table["prompt"][i].as_py(),
                    "response": table["response"][i].as_py(),
                }