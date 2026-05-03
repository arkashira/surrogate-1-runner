import requests, pyarrow.parquet as pq, io, json
from typing import Iterator, Dict

CDN_ROOT = "https://huggingface.co/datasets"

def cdn_url(repo: str, path: str) -> str:
    return f"{CDN_ROOT}/{repo}/resolve/main/{path}"

def project_record(raw: Dict) -> Dict:
    # Strict projection to avoid mixed schemas / CastError
    return {
        "prompt": str(raw.get("prompt") or raw.get("input") or ""),
        "response": str(raw.get("response") or raw.get("output") or "")
    }

def stream_cdn_files(manifest_path: str) -> Iterator[Dict]:
    with open(manifest_path) as f:
        manifest = json.load(f)

    repo = manifest["repo"]
    for rel_path in manifest["files"]:
        url = cdn_url(repo, rel_path)
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()

        if rel_path.endswith(".parquet"):
            table = pq.read_table(io.BytesIO(resp.content))
            for batch in table.to_batches(max_chunksize=1000):
                for row in batch.to_pylist():
                    yield project_record(row)
        elif rel_path.endswith(".jsonl"):
            for line in resp.iter_lines(decode_unicode=True):
                if not line:
                    continue
                row = json.loads(line)
                yield project_record(row)
        else:
            continue