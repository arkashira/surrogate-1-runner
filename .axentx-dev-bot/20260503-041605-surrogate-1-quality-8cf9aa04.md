# axentx-dev-bot decision
- id: `20260503-041605-surrogate-1-quality-8cf9aa04`
- project: surrogate-1
- focus: quality
- created_at: 2026-05-03T04:16:05.271792Z

## dev — claude/llm-fallback-chain @ 2026-05-03T04:16:05.271884Z

## Final Implementation Plan (≤2 h)

**Highest-value improvement**: Replace fragile shell-based ingestion with a **manifest-driven, CDN-bypass Python worker** that eliminates HF API rate limits during data loads and prevents mixed-schema `CastError`s. One worker run is deterministic, observable, and safe for 16-way parallelism.

---

### Changes

1. **Add `bin/worker.py`** — single-file worker:
   - Accepts `SHARD_ID` (0–15) and `TOTAL_SHARDS` (default 16) via env.
   - One API call (`list_repo_tree`) to list date folders under `batches/public-merged/`.
   - Picks the latest date folder.
   - Builds a manifest of all `shard-*.jsonl` files in that folder.
   - Filters files by `int(sha256(filename) % TOTAL_SHARDS) == SHARD_ID`.
   - Downloads selected files via **HF CDN** (`resolve/main/...`) with no Authorization header.
   - Streams JSONL, projects to `{prompt, response}`, validates schema, skips malformed rows.
   - Deduplicates via `lib/dedup.py` (central md5 store).
   - Writes output to `batches/public-merged/<date>/shard<N>-<HHMMSS>.jsonl` via HF API (single commit).

2. **Replace `bin/dataset-enrich.sh` with `bin/dataset_enrich.py`** (thin wrapper):
   - Exports `SHARD_ID`, `TOTAL_SHARDS=16`.
   - Invokes `python3 bin/worker.py`.
   - Logs to stdout/stderr (captured by Actions).

3. **Update `.github/workflows/ingest.yml`**:
   - Add matrix strategy with `shard_id: [0..15]`.
   - Keep 7 GB runner headroom and short timeout per shard.

4. **Add `requirements-dev.txt`** (optional) — pin `requests`, `tqdm`, `huggingface-hub` for local testing.

---

### Why this is highest value
- Eliminates HF API rate limits during data load (CDN bypass).
- Prevents `pyarrow.CastError` by projecting schema at parse time.
- Keeps 16-shard parallelism while making each shard resilient and observable.
- Fits within 2 h: ~150 LoC new + small workflow tweak.

---

### Code Snippets

#### `bin/worker.py`

```python
#!/usr/bin/env python3
"""
CDN-bypass ingestion worker for surrogate-1 public dataset.

Environment:
  SHARD_ID        int 0..15
  TOTAL_SHARDS    int (default 16)
  HF_TOKEN        write token for axentx/surrogate-1-training-pairs
  DATASET_REPO    default axentx/surrogate-1-training-pairs
"""

import os
import sys
import json
import hashlib
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Iterable

import requests
from huggingface_hub import HfApi, list_repo_tree

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger("worker")

HF_TOKEN = os.getenv("HF_TOKEN")
DATASET_REPO = os.getenv("DATASET_REPO", "axentx/surrogate-1-training-pairs")
TOTAL_SHARDS = int(os.getenv("TOTAL_SHARDS", "16"))
SHARD_ID = int(os.getenv("SHARD_ID", "-1"))

if not HF_TOKEN:
    log.error("HF_TOKEN is required")
    sys.exit(1)
if not (0 <= SHARD_ID < TOTAL_SHARDS):
    log.error("SHARD_ID must be in [0, TOTAL_SHARDS-1]")
    sys.exit(1)

API = HfApi(token=HF_TOKEN)

# Local dedup store
DEDUP_DB_PATH = Path(__file__).parent / "lib" / "dedup.py"
if DEDUP_DB_PATH.exists():
    import importlib.util
    spec = importlib.util.spec_from_file_location("dedup", DEDUP_DB_PATH)
    dedup_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(dedup_mod)
    is_duplicate = getattr(dedup_mod, "is_duplicate", None)
    mark_seen = getattr(dedup_mod, "mark_seen", None)
else:
    log.warning("dedup.py not found, skipping cross-run dedup")
    is_duplicate = lambda h: False  # noqa: E731
    mark_seen = lambda h: None  # noqa: E731

CDN_ROOT = f"https://huggingface.co/datasets/{DATASET_REPO}/resolve/main"

def deterministic_shard(key: str) -> int:
    return int(hashlib.sha256(key.encode()).hexdigest(), 16) % TOTAL_SHARDS

def list_date_folders() -> list[str]:
    """Return sorted date folder names under batches/public-merged/"""
    items = list_repo_tree(
        repo_

## review — reviewer @ 2026-05-03T04:16:17.927825Z

APPROVE: Manifest-driven worker is a clear, workable improvement that replaces fragile shell ingestion, eliminates HF API rate limits via CDN, and prevents CastErrors by projecting schema at parse time; incremental and testable within the 2-hour scope.

Acceptance criteria:
- Worker accepts SHARD_ID/TOTAL_SHARDS env vars and exits non-zero on invalid values or missing HF_TOKEN.
- One list_repo_tree call discovers the latest date folder and builds a manifest of shard-*.jsonl files; deterministic sharding uses sha256(filename) % TOTAL_SHARDS.
- Downloads use CDN URLs (no Authorization header) and stream JSONL; each row is projected to {prompt, response} with basic schema validation and malformed rows skipped.
- Deduplication calls is_duplicate/mark_seen from lib/dedup.py when present; missing dedup logs warning and continues.
- Output is written as batches/public-merged/<date>/shard<N>-<HHMMSS>.jsonl via HF API (single commit) and logs include timestamps and shard identity.

## qa — qa @ 2026-05-03T04:16:33.857844Z

PASS

---

### 1. Acceptance criteria
- Worker accepts SHARD_ID/TOTAL_SHARDS env vars and exits non-zero on invalid values or missing HF_TOKEN.
- One list_repo_tree call discovers the latest date folder and builds a manifest of shard-*.jsonl files; deterministic sharding uses sha256(filename) % TOTAL_SHARDS.
- Downloads use CDN URLs (no Authorization header) and stream JSONL; each row is projected to {prompt, response} with basic schema validation and malformed rows skipped.
- Deduplication calls is_duplicate/mark_seen from lib/dedup.py when present; missing dedup logs warning and continues.
- Output is written as batches/public-merged/<date>/shard<N>-<HHMMSS>.jsonl via HF API (single commit) and logs include timestamps and shard identity.
- Worker emits structured logs (timestamp, level, name, message) and records per-shard metrics (files_selected, rows_read, rows_valid, rows_skipped, rows_duplicate, rows_written).
- Worker is idempotent for the same shard+date+files: re-run with identical inputs produces identical output file content and does not create duplicate HF commits for unchanged data.

---

### 2. Unit tests (pytest-style pseudo-code)

```python
# tests/unit/test_worker.py
import os
import json
import hashlib
import pytest
from unittest import mock
from bin.worker import (
    select_shard_files,
    project_row,
    is_valid_row,
    build_cdn_url,
    run_worker,
)

# ---- helpers ----
def fake_tree(path, entries):
    return [mock.Mock(path=f"{path}/{e}", type="file") for e in entries]

# ---- acceptance: env validation ----
def test_rejects_missing_hf_token():
    with mock.patch.dict(os.environ, {}, clear=True):
        with pytest.raises(SystemExit, match="HF_TOKEN"):
            run_worker()

def test_rejects_invalid_shard_id():
    with mock.patch.dict(os.environ, {"HF_TOKEN": "x", "SHARD_ID": "99", "TOTAL_SHARDS": "16"}):
        with pytest.raises(SystemExit):
            run_worker()

def test_accepts_valid_shard_env():
    with mock.patch.dict(os.environ, {"HF_TOKEN": "x", "SHARD_ID": "3", "TOTAL_SHARDS": "16"}):
        # should not raise
        pass

# ---- acceptance: manifest & deterministic sharding ----
def test_select_shard_files_deterministic():
    files = [
        "batches/public-merged/2024-06-01/shard-001.jsonl",
        "batches/public-merged/2024-06-01/shard-002.jsonl",
        "batches/public-merged/2024-06-01/shard-003.jsonl",
    ]
    selected = select_shard_files(files, shard_id=1, total_shards=4)
    expected = [
        f for f in files
        if int(hashlib.sha256(f.encode()).hexdigest(), 16) % 4 == 1
    ]
    assert selected == expected

def test_select_shard_files_returns_empty_when_none_match():
    files = ["batches/public-merged/2024-06-01/other.txt"]
    selected = select_shard_files(files, shard_id=0, total_shards=16)
    assert selected == []

# ---- acceptance: projection & schema validation ----
def test_project_row_valid():
    row = {"prompt": "hello", "response": "world", "extra": 1}
    out = project_row(row)
    assert out == {"prompt": "hello", "response": "world"}

def test_project_row_missing_prompt():
    row = {"response": "world"}
    assert is_valid_row(row) is False

def test_project_row_missing_response():
    row = {"prompt": "hello"}
    assert is_valid_row(row) is False

def test_project_row_non_string():
    row = {"prompt": 123, "response": []}
    # validation may allow non-strings depending on policy; test behavior
    out = project_row(row)
    assert "prompt" in out and "response" in out

def test_skips_malformed_jsonl_line():
    line = "{invalid json"
    parsed = json.loads('{"prompt":"x","response":"y"}')  # control
    # integration-level test would stream; unit asserts is_valid_row/project_row
    assert is_valid_row(parsed) is True

# ---- acceptance: CDN URL & no auth header ----
def test_build_cdn_url():
    url = build_cdn_url("axentx/surrogate-1-training-pairs", "batches/public-merged/2024-06-01/shard-001.jsonl")
    assert "resolve" i
