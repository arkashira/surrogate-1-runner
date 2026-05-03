import json, io, time, requests
from typing import List, Dict, Iterator
import pyarrow.parquet as pq

def _backoff(attempt: int, base: float = 1.0, cap: float = 60.0) -> float:
    return min(cap, base * (2 ** attempt))

def load_from_snapshot(manifest_path: str, columns: List[str] = ("prompt", "response")) -> Iterator[Dict]:
    with open(manifest_path) as f:
        manifest = json.load(f)

    files = manifest.get("files", [])
    if not files:
        return

    for item in files:
        url = item.get("cdn_url") or item.get("path")
        if not url:
            continue
        if not url.startswith("http"):
            # fallback to CDN construction
            repo = manifest.get("repo", "")
            url = f"https://huggingface.co/datasets/{repo}/resolve/main/{item['path']}"

        for attempt in range(5):
            try:
                resp = requests.get(url, stream=True, timeout=30)
                resp.raise_for_status()
                break
            except Exception as e:
                wait = _backoff(attempt)
                print(f"WARN: attempt {attempt+1}/5 failed for {url}: {e}; retry in {wait:.1f}s")
                time.sleep(wait)
        else:
            print(f"WARN: failed to fetch {url} after 5 attempts")
            continue

        data = resp.content
        try:
            if url.endswith(".parquet"):
                table = pq.read_table(io.BytesIO(data), columns=columns)
                for batch in table.to_batches(max_chunksize=1000):
                    cols = {c: batch.column(c) for c in columns}
                    for i in range(batch.num_rows):
                        yield {c: cols[c][i].as_py() for c in columns}
            elif url.endswith(".jsonl"):
                for line in data.splitlines():
                    if not line.strip():
                        continue
                    try:
                        row = json.loads(line)
                        yield {c: row.get(c) for c in columns}
                    except Exception:
                        continue
            else:
                print(f"WARN: unsupported file {url}")
        except Exception as e:
            print(f"WARN: failed to decode {url}: {e}")
            continue