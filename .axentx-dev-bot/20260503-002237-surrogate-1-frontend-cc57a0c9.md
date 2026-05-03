# axentx-dev-bot decision
- id: `20260503-002237-surrogate-1-frontend-cc57a0c9`
- project: surrogate-1
- focus: frontend
- created_at: 2026-05-03T00:22:37.297262Z

## dev — claude/llm-fallback-chain @ 2026-05-03T00:22:37.297360Z

**Final consolidated implementation plan**  
(Strongest parts from both proposals, contradictions resolved for correctness + concrete actionability)

---

## Core idea (highest-value, ≤2h)

Add a **deterministic snapshot generator** (`bin/snapshot.sh`) that lists one date folder via HF tree API and emits `snapshots/<date>/files.json` with CDN URLs.  
Make **ingestion** and **training** accept that snapshot and stream exclusively via CDN — zero HF API calls during heavy data movement.  
Keep Mac as orchestrator only; reuse running Lightning Studio; preserve 16-shard parallelism.

---

## Why this wins

- Removes recursive `list_repo_files`/`list_repo_tree` during training → eliminates 429s.  
- CDN downloads do not count against HF API limits.  
- Deterministic manifests enable reproducible sharding across workers.  
- Minimal footprint: one new script, small patches to ingestion and training, no schema changes.

---

## File layout (final)

```
/opt/axentx/surrogate-1/
├── bin/
│   ├── snapshot.sh              # new: manifest generator
│   └── dataset-enrich.sh        # patch: accept SNAPSHOT_FILE
├── surrogate_1/
│   ├── __init__.py
│   ├── ingest_cdn.py            # new: CDN-only ingestion worker
│   ├── data.py                  # patch: CdnDataset + helpers
│   └── lib/
│       └── snapshot.py          # new: load snapshot + build URLs
├── train.py                     # patch: accept --snapshot; use CdnDataset
└── requirements.txt             # ensure requests, pyarrow, datasets, lightning
```

---

## 1) Snapshot generator — `bin/snapshot.sh` (new)

- Single `list_repo_tree(..., recursive=false)` per date folder.  
- Deterministic sort → stable manifest.  
- Output: `snapshots/<date>/files.json` with CDN URLs and basenames.

```bash
#!/usr/bin/env bash
# bin/snapshot.sh
# Usage: HF_TOKEN=... ./bin/snapshot.sh axentx/surrogate-1-training-pairs 2026-05-03
set -euo pipefail

REPO="${1:?repo required}"
DATE="${2:?date required (YYYY-MM-DD)}"
OUTDIR="snapshots/${DATE}"
OUTFILE="${OUTDIR}/files.json"

mkdir -p "${OUTDIR}"

# One HF tree API call per date folder (non-recursive).
# Rate-note: this is the only HF API call; CDN downloads do NOT count against limits.
echo "Listing ${REPO} tree for ${DATE}..."
TREE_JSON=$(curl -s \
  -H "Authorization: Bearer ${HF_TOKEN:-}" \
  -H "Content-Type: application/json" \
  "https://huggingface.co/api/datasets/${REPO}/tree?path=${DATE}&recursive=false")

# Extract filenames, sort for determinism, build CDN URLs.
echo "${TREE_JSON}" \
  | python3 -c "
import sys, json, os
tree = json.load(sys.stdin)
items = sorted([item for item in tree if item.get('type') == 'file'], key=lambda x: x['path'])
base = 'https://huggingface.co/datasets/${REPO}/resolve/main'
out = []
for it in items:
    p = it['path']
    out.append({
        'path': p,
        'basename': os.path.basename(p),
        'cdn_url': f'{base}/{p}'
    })
print(json.dumps({'date': '${DATE}', 'repo': '${REPO}', 'files': out}, indent=2))
" > "${OUTFILE}"

echo "Snapshot written to ${OUTFILE}"
```

Make executable:

```bash
chmod +x bin/snapshot.sh
```

---

## 2) Snapshot loader — `surrogate_1/lib/snapshot.py` (new)

```python
import json
import os
from typing import List, Dict

def load_snapshot(snapshot_path: str) -> Dict:
    with open(snapshot_path) as f:
        data = json.load(f)
    return data

def iter_cdn_urls(manifest: Dict):
    for item in manifest.get("files", []):
        yield item["cdn_url"], item["basename"], item["path"]
```

---

## 3) Ingestion worker — `surrogate_1/ingest_cdn.py` (new)

- Streams each CDN URL.  
- Detects format (jsonl/parquet/json) and projects only `{prompt,response}`.  
- Writes line-delimited JSON for downstream training.

```python
import json
import sys
import os
import pyarrow.parquet as pq
import requests
from surrogate_1.lib.snapshot import load_snapshot, iter_cdn_urls

def stream_cdn_file(url, project_keys=("prompt", "response")):
    # Simple retry/backoff
    for attempt in range(3):
  

## review — reviewer @ 2026-05-03T00:22:43.939381Z

APPROVE: Deterministic snapshot + CDN-only ingestion is a clear, workable step that directly addresses HF API limits and enables reproducible sharding; patches are minimal and testable.

Acceptance criteria (downstream tester can check):
- `bin/snapshot.sh` runs with a valid HF_TOKEN and produces `snapshots/<date>/files.json` containing sorted entries with `cdn_url`, `basename`, and `path` for every file in that date folder (non-recursive).  
- `surrogate_1/lib/snapshot.py` loads the produced JSON and `iter_cdn_urls` yields tuples `(cdn_url, basename, path)` for every file entry.  
- `surrogate_1/ingest_cdn.py` can stream a sample CDN URL (parquet/jsonl/json) and emit `{prompt, response}` records without calling HF API endpoints (verify via network logs or mock).  
- `train.py` accepts `--snapshot <path>` and uses `CdnDataset` (or equivalent) to iterate training examples exclusively from CDN URLs listed in the snapshot.  
- The 16-shard parallelism (existing) can consume the snapshot manifest and each shard processes a deterministic subset of files (e.g., shard_id modulo assignment) without overlap or missing files.

## qa — qa @ 2026-05-03T00:23:06.464367Z

PASS: deterministic snapshot + CDN-only ingestion is clear, workable, and directly addresses HF API limits.

---

## 1) Acceptance criteria

- `bin/snapshot.sh` with valid `HF_TOKEN` produces `snapshots/<date>/files.json` containing sorted entries; each entry has `cdn_url`, `basename`, and `path` for every file in that date folder (non-recursive).  
- `surrogate_1/lib/snapshot.py` loads the produced JSON and `iter_cdn_urls()` yields `(cdn_url, basename, path)` for every file entry in manifest order.  
- `surrogate_1/ingest_cdn.py` streams a sample CDN URL (parquet/jsonl/json) and emits `{prompt, response}` records without calling any HF API endpoints (verifiable via network logs or mocks).  
- `train.py` accepts `--snapshot <path>` and uses `CdnDataset` (or equivalent) to iterate training examples exclusively from CDN URLs listed in the snapshot.  
- The 16-shard parallelism consumes the snapshot manifest and each shard processes a deterministic subset of files (shard_id modulo assignment) with zero overlap and no missing files.  
- Snapshot generation uses exactly one HF tree API call per date folder (non-recursive) and emits deterministic output for identical repo/date inputs.  
- All new/modified components have unit tests and integration tests that pass in CI.

---

## 2) Unit tests (pseudo-code, pytest style)

```python
# surrogate_1/lib/test_snapshot.py
import json
from surrogate_1.lib.snapshot import load_snapshot, iter_cdn_urls

def test_load_snapshot(tmp_path):
    manifest = {
        "date": "2026-05-03",
        "repo": "axentx/surrogate-1-training-pairs",
        "files": [
            {"path": "2026-05-03/a.parquet", "basename": "a.parquet", "cdn_url": "https://huggingface.co/datasets/axentx/surrogate-1-training-pairs/resolve/main/2026-05-03/a.parquet"},
            {"path": "2026-05-03/b.parquet", "basename": "b.parquet", "cdn_url": "https://huggingface.co/datasets/axentx/surrogate-1-training-pairs/resolve/main/2026-05-03/b.parquet"},
        ]
    }
    p = tmp_path / "files.json"
    p.write_text(json.dumps(manifest))
    loaded = load_snapshot(str(p))
    assert loaded["date"] == "2026-05-03"
    assert len(loaded["files"]) == 2

def test_iter_cdn_urls_order():
    manifest = {
        "files": [
            {"path": "2026-05-03/a.parquet", "basename": "a.parquet", "cdn_url": "cdn/a"},
            {"path": "2026-05-03/b.parquet", "basename": "b.parquet", "cdn_url": "cdn/b"},
        ]
    }
    out = list(iter_cdn_urls(manifest))
    assert out == [("cdn/a", "a.parquet", "2026-05-03/a.parquet"), ("cdn/b", "b.parquet", "2026-05-03/b.parquet")]

# surrogate_1/test_ingest_cdn.py
from surrogate_1.ingest_cdn import stream_cdn_file
import pytest

def test_stream_cdn_parquet_no_hf_api_calls(requests_mock):
    # block any real HF API calls
    requests_mock.get("https://huggingface.co/api/", status_code=404)
    requests_mock.get("https://huggingface.co/datasets/repo/resolve/main/sample.parquet", content=create_sample_parquet_bytes())
    rows = list(stream_cdn_file("https://huggingface.co/datasets/repo/resolve/main/sample.parquet"))
    assert all("prompt" in r and "response" in r for r in rows)
    assert all(not req.path.startswith("/api/") for req in requests_mock.request_history)

# surrogate_1/test_data.py
from surrogate_1.data import CdnDataset

def test_cdn_dataset_uses_only_cdn_urls():
    manifest = {"files": [{"cdn_url": "https://cdn/file1.parquet", "basename": "file1.parquet", "path": "2026-05-03/file1.parquet"}]}
    ds = CdnDataset(manifest, shard_id=0, num_shards=1)
    # internal check: no HF API endpoints in requested URLs
    urls = [u for u in ds._urls if "huggingface.co/api" in u]
    assert len(urls) == 0

# train/test_cli.py
from click.testing import CliRunner
from train import cli

def test_train_accepts_snapshot():
    runner = CliRunner()
    result = runner.invoke(cli, ["--snapshot", "snapshots/2026-05-03/files.json", "--dry-run"])
    assert result.exit_code == 0
   
