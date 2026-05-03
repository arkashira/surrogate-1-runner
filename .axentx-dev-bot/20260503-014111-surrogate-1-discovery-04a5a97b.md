# axentx-dev-bot decision
- id: `20260503-014111-surrogate-1-discovery-04a5a97b`
- project: surrogate-1
- focus: discovery
- created_at: 2026-05-03T01:41:11.634841Z

## dev — claude/llm-fallback-chain @ 2026-05-03T01:41:11.635005Z

## Implementation Plan — Manifest-Driven CDN-Bypass Ingestion Pipeline

**Goal**: Replace `bin/dataset-enrich.sh` with a manifest-driven, CDN-bypass ingestion pipeline that eliminates HF API rate limits (429) and mixed-schema `pyarrow` errors, and produces clean `{prompt,response}` pairs into `batches/public-merged/<date>/shard<N>-<HHMMSS>.jsonl`.

**Scope**: Single high-value change that can ship in <2h and unblocks stable, scalable ingestion for surrogate-1.

---

### 1) High-level flow (what changes)

1. **Mac orchestrator** (run manually or via cron):
   - Calls HF API **once** per date folder with `list_repo_tree(path, recursive=False)` (non-recursive to avoid pagination explosion).
   - Saves file list + metadata to `manifests/<date>/file-list.json`.
   - Commits/pushes manifest (optional) or passes to Actions via `workflow_dispatch` input.

2. **GitHub Actions matrix (16 shards)**:
   - Each runner receives:
     - `DATE` (e.g., `2026-05-03`)
     - `SHARD_ID` (0–15)
     - `FILE_LIST` path or inline JSON
   - Runner **does not call HF API** during ingestion. It only uses **CDN URLs**:
     - `https://huggingface.co/datasets/axentx/surrogate-1-training-pairs/resolve/main/<path>`
   - Per file:
     - Download via CDN (no auth, bypasses `/api/` rate limits).
     - Parse safely:
       - If parquet: read with `pyarrow` and project only `{prompt, response}` at parse time; ignore extra columns.
       - If JSON/JSONL: stream and extract `{prompt, response}`.
       - If schema is missing/heterogeneous: skip malformed rows and log.
     - Compute deterministic `md5` over normalized content for dedup (central SQLite store on HF Space remains source of truth; local dedup is best-effort per-run).
   - Output: `batches/public-merged/<date>/shard<N>-<HHMMSS>.jsonl` (one line per `{prompt, response}`).
   - Push to HF dataset repo using `huggingface_hub` with `HF_TOKEN`.

3. **Deterministic shard assignment**:
   - `shard_id = hash(slug) % 16`
   - Ensures same file always maps to same shard across runs → no cross-shard collisions.

4. **Idempotency & collision avoidance**:
   - Filename includes `shard<N>-<HHMMSS>` → unique per run.
   - Central dedup store on HF Space prevents duplicates across runs (best-effort; wasted bandwidth acceptable per trade-offs).

---

### 2) Concrete file changes

#### New: `bin/build-manifest.py`
```python
#!/usr/bin/env python3
"""
Usage: python bin/build-manifest.py --date 2026-05-03 --out manifests/2026-05-03/file-list.json
"""
import argparse
import json
import os
from huggingface_hub import HfApi

API = HfApi()
REPO = "datasets/axentx/surrogate-1-training-pairs"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True, help="Date folder in repo (e.g. 2026-05-03)")
    parser.add_argument("--out", required=True, help="Output JSON path")
    args = parser.parse_args()

    # Non-recursive to avoid pagination explosion
    entries = API.list_repo_tree(REPO, path=args.date, recursive=False)
    files = [e.path for e in entries if e.type == "file"]

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w") as f:
        json.dump({"date": args.date, "files": files}, f, indent=2)

    print(f"Wrote {len(files)} files to {args.out}")

if __name__ == "__main__":
    main()
```
- Make executable: `chmod +x bin/build-manifest.py`.

---

#### Replace: `bin/dataset-enrich.sh` → `bin/dataset-enrich.py`

Rationale: Bash is fragile for JSON, retries, and per-row schema projection. Python gives safe, readable, and maintainable parsing with CDN bypass.

```python
#!/usr/bin/env python3
"""
Per-shard CDN-bypass ingestion worker.

Environment:
  DATE=2026-05-03
  SHARD_ID=0..15
  FILE_LIST=manifests/2026-05-03/file-list.json  (or inline JSON)
  HF_TOKEN=...
  OUTPUT_DIR=batches/public-merged
"""
import json
import os
import sys
import hashlib
import time
import logging
from pathlib import Path
from datetime import datetime

import pyarrow.pa

## review — reviewer @ 2026-05-03T01:41:28.607005Z

APPROVE: Proposes a clear, incremental step forward that replaces fragile bash with a manifest-driven, CDN-bypass ingestion pipeline; addresses HF API rate limits and schema heterogeneity; has testable outputs and deterministic shard assignment.

Acceptance criteria (for downstream tester):
- `bin/build-manifest.py --date 2026-05-03 --out manifests/2026-05-03/file-list.json` produces valid JSON with a `files` list and non-recursive HF tree listing.
- `bin/dataset-enrich.py` (when provided DATE, SHARD_ID, FILE_LIST, HF_TOKEN) downloads files via CDN URLs (`https://huggingface.co/datasets/.../resolve/main/...`) without calling HF `/api/` endpoints.
- Per-file parsing projects only `{prompt, response}` (accepting alternate keys) and emits one line per normalized pair into `batches/public-merged/<date>/shard<N>-<HHMMSS>.jsonl`.
- Deterministic shard assignment: `shard_id = hash(slug) % 16` yields the same shard for the same file across runs.
- Output files are valid JSONL and pushed to the HF dataset repo using `huggingface_hub` with the provided HF_TOKEN.

## qa — qa @ 2026-05-03T01:42:26.037833Z

PASS: proposal is clear, incremental, and testable.

1) **Acceptance criteria**
- `bin/build-manifest.py --date 2026-05-03 --out manifests/2026-05-03/file-list.json` exits 0 and produces valid JSON containing a top-level `files` list with non-recursive entries (no nested trees) and non-empty `path` fields.
- `bin/dataset-enrich.py` (with DATE, SHARD_ID, FILE_LIST, HF_TOKEN) performs zero HTTP requests to `*/api/*` endpoints during ingestion (only CDN `resolve/main/` URLs).
- Per-file parsing emits one JSONL line per normalized `{prompt, response}` pair; lines are valid JSON and contain exactly those two keys (string values).
- Deterministic shard assignment: for any file slug, `shard_id = hash(slug) % 16` returns the same integer in [0,15] across multiple runs.
- Output file path matches pattern `batches/public-merged/<date>/shard<N>-<HHMMSS>.jsonl` where N ∈ [0,15] and HHMMSS is a valid timestamp; file is valid JSONL and is pushed to the HF dataset repo using `huggingface_hub` with provided HF_TOKEN.

2) **Unit tests** (pytest-style pseudo-code)
```python
# test_build_manifest.py
def test_build_manifest_valid_json(tmp_path, mock_hf_api):
    out = tmp_path / "file-list.json"
    mock_hf_api.list_repo_tree.return_value = [
        {"path": "2026-05-03/a.parquet", "type": "file", "size": 1024},
        {"path": "2026-05-03/b.jsonl", "type": "file", "size": 2048},
    ]
    run_build_manifest(date="2026-05-03", out=out)
    data = json.loads(out.read_text())
    assert "files" in data
    assert len(data["files"]) == 2
    assert all("path" in f and isinstance(f["path"], str) for f in data["files"])
    # non-recursive: no nested tree objects
    assert all(f.get("type") != "tree" for f in data["files"])

def test_build_manifest_non_recursive(mock_hf_api):
    run_build_manifest(date="2026-05-03", out=Path("x.json"))
    mock_hf_api.list_repo_tree.assert_called_with(
        "datasets/axentx/surrogate-1-training-pairs",
        path="2026-05-03",
        recursive=False
    )

# test_dataset_enrich.py
def test_no_api_calls_during_ingest(mock_requests, tmp_path):
    file_list = tmp_path / "files.json"
    file_list.write_text(json.dumps({
        "files": [{"path": "2026-05-03/a.parquet", "type": "file"}]
    }))
    mock_requests.get.side_effect = lambda url, **kw: MockResponse(
        url=url,
        content=make_parquet_bytes(rows=[{"prompt": "p", "response": "r"}])
    )
    run_dataset_enrich(
        date="2026-05-03",
        shard_id=3,
        file_list=file_list,
        hf_token="x",
        out_dir=tmp_path
    )
    api_calls = [c for c in mock_requests.get.call_args_list if "/api/" in c[0][0]]
    assert len(api_calls) == 0

def test_projects_prompt_response_only(tmp_path):
    file_list = tmp_path / "files.json"
    file_list.write_text(json.dumps({
        "files": [{"path": "2026-05-03/a.jsonl", "type": "file"}]
    }))
    lines = [
        {"prompt": "hello", "response": "world", "extra": "x"},
        {"prompt": "foo", "response": "bar"},
    ]
    mock_download_and_parse.return_value = lines
    out = run_dataset_enrich(
        date="2026-05-03",
        shard_id=0,
        file_list=file_list,
        hf_token="x",
        out_dir=tmp_path
    )
    emitted = [json.loads(l) for l in out.read_text().strip().splitlines()]
    assert len(emitted) == 2
    for e in emitted:
        assert set(e.keys()) == {"prompt", "response"}
        assert isinstance(e["prompt"], str)
        assert isinstance(e["response"], str)

def test_shard_assignment_deterministic():
    slug = "2026-05-03/a.parquet"
    ids = [shard_id(slug) for _ in range(10)]
    assert len(set(ids)) == 1
    assert 0 <= ids[0] <= 15

def test_output_path_pattern(tmp_path):
    out = output_path(date="2026-05-03
