import json
import sys
import os
import pyarrow.parquet as pq
import requests
from surrogate_1.lib.snapshot import load_snapshot, iter_cdn_urls

def stream_cdn_file(url, project_keys=("prompt", "response")):
    # Simple retry/backoff
    for attempt in range(3):
        try:
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            break
        except Exception as e:
            if attempt == 2:
                raise
            continue

    # Determine format by extension or content
    if url.endswith(".parquet"):
        # Stream parquet by row groups; read only needed columns
        pf = pq.ParquetFile(resp.content)
        for rg_i in range(pf.metadata.num_row_groups):
            table = pf.read_row_group(rg_i, columns=project_keys)
            for row in table.to_pylist():
                yield {k: row.get(k) for k in project_keys}
    elif url.endswith(".jsonl"):
        for line in resp.iter_lines(decode_unicode=True):
            if not line:
                continue
            obj = json.loads(line)
            yield {k: obj.get(k) for k in project_keys}
    elif url.endswith(".json"):
        obj = resp.json()
        if isinstance(obj, list):
            for item in obj:
                yield {k: item.get(k) for k in project_keys}
        else:
            yield {k: obj.get(k) for k in project_keys}
    else:
        raise ValueError(f"Unsupported file format: {url}")

def main(snapshot_path, out_path):
    manifest = load_snapshot(snapshot_path)
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as out_f:
        for cdn_url, _, _ in iter_cdn_urls(manifest):
            for record in stream_cdn_file(cdn_url):
                out_f.write(json.dumps(record, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python -m surrogate_1.ingest_cdn <snapshot.json> <out.jsonl>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])