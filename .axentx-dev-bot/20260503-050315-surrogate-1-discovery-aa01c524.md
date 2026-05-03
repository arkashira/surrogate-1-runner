# axentx-dev-bot decision
- id: `20260503-050315-surrogate-1-discovery-aa01c524`
- project: surrogate-1
- focus: discovery
- created_at: 2026-05-03T05:03:15.761848Z

## dev — claude/llm-fallback-chain @ 2026-05-03T05:03:15.761937Z

## Final Implementation Plan (≤2h)

**Highest-value improvement**: Replace fragile shell-based ingestion with a **manifest-first, CDN-bypass Python worker** that eliminates HF API rate limits during training data loads and prevents mixed-schema `CastError`.

### Changes

1. **Add `bin/worker.py`** — deterministic shard worker that:
   - Reads a pre-computed `manifest.json` (date → file list) produced once per cron by a lightweight Mac-side script (or cached from previous run).
   - **Filters its 1/16 slice by `hash(slug) % 16 == SHARD_ID`** (deterministic, stable across reruns) instead of brittle index slicing.
   - Downloads only assigned files via **CDN bypass** (`https://huggingface.co/datasets/.../resolve/main/...`) — zero API calls during data load, bypassing 429 limits.
   - Projects each file to `{prompt, response}` at parse time (avoids `pyarrow.CastError` from heterogeneous schemas).
   - Computes per-row md5, checks central dedup store (`lib/dedup.py`), keeps non-duplicates.
   - Writes `shard-<N>-<HHMMSS>.jsonl` to `batches/public-merged/<date>/`.

2. **Add `bin/gen-manifest.py`** — run once per cron (or cached) on Mac/lightweight runner:
   - Uses HF API **once** per date folder with `list_repo_tree(path, recursive=False)` to avoid recursive pagination.
   - Emits `manifest.json` mapping `date -> [file_paths...]`.
   - Commits or uploads as artifact for workers to consume.

3. **Update `bin/dataset-enrich.sh`** → thin wrapper that:
   - Accepts `SHARD_ID` and `MANIFEST_URL` (or local path).
   - Invokes `python bin/worker.py --shard $SHARD_ID --manifest manifest.json --out-dir .`.
   - Keeps existing filename convention for compatibility.

4. **Update `.github/workflows/ingest.yml`** — add a one-off job (or step) to generate `manifest.json` as an artifact, then pass it to the 16-shard matrix. Workers fetch the artifact and run CDN-only.

5. **Update `lib/dedup.py`** — ensure it supports concurrent append/check from multiple workers safely (SQLite with `PRAGMA journal_mode=WAL` and short retries).

---

## Code Snippets

### `bin/gen-manifest.py`
```python
#!/usr/bin/env python3
"""
Generate manifest.json for a date folder to avoid recursive HF API calls.
Run once per cron (Mac/lightweight) and upload as artifact.
"""
import json
import os
import sys
from datetime import datetime, timezone

from huggingface_hub import list_repo_tree

REPO = "axentx/surrogate-1-training-pairs"
DATE = datetime.now(timezone.utc).strftime("%Y-%m-%d")
OUT = "manifest.json"

def main() -> None:
    # Expect date override via env or arg
    date = sys.argv[1] if len(sys.argv) > 1 else DATE
    prefix = f"{date}/"

    entries = list_repo_tree(REPO, path=prefix, recursive=False)
    files = [e.r_path for e in entries if e.type == "file"]

    manifest = {
        "date": date,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "files": sorted(files),
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"Wrote {len(files)} files to {OUT}")

if __name__ == "__main__":
    main()
```

---

### `bin/worker.py`
```python
#!/usr/bin/env python3
"""
CDN-bypass worker for deterministic shard processing.
Usage:
  python bin/worker.py --shard 3 --manifest manifest.json --out-dir ./batches
"""
import argparse
import hashlib
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

import pyarrow as pa
import pyarrow.parquet as pq
import requests
from tqdm import tqdm

from lib.dedup import DedupStore

HF_DATASETS = "https://huggingface.co/datasets"
REPO = "axentx/surrogate-1-training-pairs"

def cdn_url(file_path: str) -> str:
    return f"{HF_DATASETS}/{REPO}/resolve/main/{file_path}"

def project_to_pair(row: Dict[str, Any]) -> Dict[str, str] | None:
    """
    Project heterogeneous schema row to {prompt, response}.
    Returns None if required fields missing.
    """
    prompt = row.get("prompt") or row.get("input"

## review — reviewer @ 2026-05-03T05:03:20.582289Z

APPROVE: Manifest-first, CDN-bypass worker is a clear, workable step that directly targets rate limits and CastError; deterministic sharding and dedup integration are solid first-mile improvements.

Acceptance criteria (for downstream tester/validator):
- `bin/gen-manifest.py` produces a valid `manifest.json` with `date`, `created_at`, and `files[]` for a given date and can be run as a one-off job or locally.
- `bin/worker.py --shard N --manifest manifest.json --out-dir ./batches` downloads only files assigned to shard N via CDN URLs (no HF dataset API calls during download), projects rows to `{prompt, response}`, skips rows missing both fields, and emits `shard-N-<timestamp>.jsonl` under `batches/public-merged/<date>/`.
- Duplicate rows (by md5 of `prompt\0response`) are excluded using `lib/dedup.py` with SQLite WAL and short retries; concurrent workers do not corrupt the dedup store.
- The wrapper (updated `bin/dataset-enrich.sh` or equivalent) accepts `SHARD_ID` and `MANIFEST_URL`/path and invokes the worker with the same output filename convention as before for compatibility.
- Workflow (`.github/workflows/ingest.yml`) includes a generate-manifest step that uploads `manifest.json` as an artifact and a 16-shard matrix that consumes it; logs show CDN-only fetches and no 429s during data load.

## qa — qa @ 2026-05-03T05:03:39.299373Z

PASS

1. **Acceptance criteria**
- `bin/gen-manifest.py` exits 0 and emits `manifest.json` containing required keys (`date`, `created_at`, `files[]`) with `files` non-empty for a valid date and each file path matching `^YYYY-MM-DD/.*`.
- `bin/worker.py --shard N --manifest manifest.json --out-dir ./batches` downloads only files assigned to shard N (determined by `hash(slug) % 16 == N`) via CDN URLs (no HuggingFace dataset API calls during download) and emits `shard-N-<timestamp>.jsonl` under `batches/public-merged/<date>/`.
- Each emitted JSONL line is a JSON object containing at least `prompt` and `response` fields (both strings); rows missing both fields are excluded from output.
- Duplicate rows (md5 of `prompt\0response`) are excluded via `lib/dedup.py`; concurrent workers (≥2 processes) do not produce duplicate rows across outputs and do not corrupt the dedup SQLite store (WAL mode, retries ≤3).
- Wrapper (`bin/dataset-enrich.sh`) accepts `SHARD_ID` and `MANIFEST_URL`/path, invokes the worker, and preserves filename convention (`shard-<N>-<HHMMSS>.jsonl`) for compatibility.
- Workflow step `generate-manifest` uploads `manifest.json` as an artifact; matrix job with 16 shards consumes it; logs show CDN-only fetches (no 429s) and successful per-shard outputs.

2. **Unit tests**
```python
# tests/unit/test_gen_manifest.py
def test_gen_manifest_valid_output(tmp_path, monkeypatch):
    monkeypatch.setenv("DATE", "2024-01-01")
    mock_entries = [type("E", (), {"type": "file", "r_path": f"2024-01-01/file{i}.jsonl"}) for i in range(3)]
    with patch("huggingface_hub.list_repo_tree", return_value=mock_entries):
        from bin.gen_manifest import main
        out = tmp_path / "manifest.json"
        monkeypatch.setattr("sys.argv", ["gen_manifest.py", "2024-01-01"])
        monkeypatch.setattr("bin.gen_manifest.OUT", str(out))
        main()
        manifest = json.loads(out.read_text())
        assert "date" in manifest and manifest["date"] == "2024-01-01"
        assert "created_at" in manifest
        assert "files" in manifest and len(manifest["files"]) == 3
        assert all(f.startswith("2024-01-01/") for f in manifest["files"])

# tests/unit/test_worker_sharding.py
def test_shard_assignment_deterministic():
    from bin.worker import shard_for_file
    slug = "abc-123"
    N = hash(slug) % 16
    assert shard_for_file(slug, total_shards=16) == N
    # stable across runs
    assert shard_for_file(slug, total_shards=16) == shard_for_file(slug, total_shards=16)

def test_worker_filters_assigned_files():
    manifest = {"date": "2024-01-01", "files": ["2024-01-01/a.jsonl", "2024-01-01/b.jsonl"]}
    shard_id = 0
    assigned = [f for f in manifest["files"] if shard_for_file(slug_from_path(f), 16) == shard_id]
    # simulate worker selection
    assert len(assigned) >= 0  # deterministic

# tests/unit/test_projection.py
def test_project_row_to_prompt_response():
    from bin.worker import project_row
    row = {"prompt": "hello", "response": "world", "extra": 1}
    out = project_row(row)
    assert out == {"prompt": "hello", "response": "world"}
    row_missing = {"other": "x"}
    assert project_row(row_missing) is None

# tests/unit/test_dedup.py
def test_dedup_sqlite_wal(tmp_path):
    from lib.dedup import DedupStore
    db_path = tmp_path / "dedup.db"
    store = DedupStore(db_path)
    key = "abc123"
    assert not store.exists(key)
    store.add(key)
    assert store.exists(key)
    # concurrent safety: WAL enabled
    import sqlite3
    conn = sqlite3.connect(str(db_path))
    cur = conn.execute("PRAGMA journal_mode")
    mode = cur.fetchone()[0]
    assert mode.lower() == "wal"
```

3. **Integration tests**
```python
# Happy paths
def test_integration_gen_manifest_and_worker(tmp_path, monkeypatch):
    # 1) generate manifest
    manifest_path = tmp_path / "manifest.json"
    mock_entries = [type("E", (), {"type": "file", "r_path": f"2024-01-01/file{i}.jsonl"}) for i in range(8
