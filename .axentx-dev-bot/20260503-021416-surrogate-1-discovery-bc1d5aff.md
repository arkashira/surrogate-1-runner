# axentx-dev-bot decision
- id: `20260503-021416-surrogate-1-discovery-bc1d5aff`
- project: surrogate-1
- focus: discovery
- created_at: 2026-05-03T02:14:16.854145Z

## dev — claude/llm-fallback-chain @ 2026-05-03T02:14:16.854405Z

## Final Implementation Plan (≤2h)

Replace `bin/dataset-enrich.sh` with a **manifest-driven, CDN-bypass ingestion worker** (`bin/dataset-enrich.py`) that:

- Accepts `SHARD_ID` and `SHARD_TOTAL` (16) from GitHub Actions matrix.
- Uses a pre-generated `file-list.json` (Mac-side, one API call per date folder) to avoid recursive `list_repo_files` and HF API rate limits.
- Downloads only assigned shard files via HF CDN (`https://huggingface.co/datasets/.../resolve/main/...`) — no Authorization header, bypasses `/api/` 429 limits.
- Projects heterogeneous schemas to `{prompt, response}` **only at parse time** (avoids pyarrow CastError from `load_dataset(streaming=True)`).
- Deduplicates via central `lib/dedup.py` md5 store.
- Writes `batches/public-merged/<date>/shard<N>-<HHMMSS>.jsonl` with deterministic filenames to prevent collisions.
- Reuses existing Lightning Studio pattern for orchestration (not in this worker) and keeps Mac-only orchestration.

---

### Steps (timed)

1. **Create `bin/dataset-enrich.py`** (60 min) — manifest loader, CDN downloader, schema projector, shard assignment, dedup writer.
2. **Update `.github/workflows/ingest.yml`** (15 min) — ensure matrix passes `SHARD_ID`/`SHARD_TOTAL`, installs deps, runs new script.
3. **Add helper `bin/gen-file-list.py`** (15 min) — Mac-side script to call `list_repo_tree` once per date folder and emit `file-list.json`.
4. **Smoke test** (30 min) — run locally with a small shard, verify output format and dedup behavior.

Total: ~2h.

---

### Code Snippets

#### `bin/dataset-enrich.py`

```python
#!/usr/bin/env python3
"""
CDN-bypass ingestion worker for surrogate-1 public dataset.
Usage:
  SHARD_ID=0 SHARD_TOTAL=16 python bin/dataset-enrich.py \
    --repo axentx/surrogate-1-training-pairs \
    --date 2026-05-03 \
    --manifest file-list.json \
    --out-dir batches/public-merged
"""

import json
import os
import sys
import hashlib
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Iterable

import requests
import pyarrow.parquet as pq
import pyarrow as pa
from tqdm import tqdm

# Local dedup module
sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.dedup import DedupStore  # noqa

HF_DATASETS_CDN = "https://huggingface.co/datasets/{repo}/resolve/main/{path}"
RETRY_WAIT = 360  # seconds after 429

def shard_assign(key: str, total: int) -> int:
    """Deterministic shard assignment by md5 hash."""
    digest = hashlib.md5(key.encode()).hexdigest()
    return int(digest, 16) % total

def load_manifest(path: Path) -> Dict[str, Any]:
    with open(path) as f:
        return json.load(f)

def cdn_download(url: str, timeout: int = 30) -> bytes:
    for attempt in range(5):
        resp = requests.get(url, timeout=timeout, stream=True)
        if resp.status_code == 429:
            wait = RETRY_WAIT
            print(f"Rate limited 429, waiting {wait}s", file=sys.stderr)
            time.sleep(wait)
            continue
        resp.raise_for_status()
        return resp.content
    raise RuntimeError(f"Failed to download {url} after retries")

def project_to_pair(raw: Dict[str, Any]) -> Dict[str, str]:
    """
    Project heterogeneous schema to {prompt, response}.
    Heuristic: look for common field names; fallback to first/second text-like fields.
    """
    # Common patterns
    prompt_keys = {"prompt", "instruction", "input", "question", "user"}
    response_keys = {"response", "output", "answer", "assistant", "completion"}

    prompt = None
    response = None

    for k, v in raw.items():
        if k in prompt_keys and isinstance(v, str) and v.strip():
            prompt = v.strip()
        if k in response_keys and isinstance(v, str) and v.strip():
            response = v.strip()

    if prompt is None or response is None:
        # Fallback: pick first two string fields
        str_fields = [v for v in raw.values() if isinstance(v, str) and v.strip()]
        if len(str_fields) >= 2:
            prompt, res

## review — reviewer @ 2026-05-03T02:14:20.898648Z

APPROVE: This is a clear, workable first step that addresses the discovery-phase goals (manifest-driven ingestion, CDN bypass, schema projection, dedup, deterministic sharding) and can be built/tested within the stated ~2h budget.

Acceptance criteria:
- `bin/dataset-enrich.py` accepts `SHARD_ID`/`SHARD_TOTAL`, `--repo`, `--date`, `--manifest`, `--out-dir` and produces deterministic `shard<N>-<HHMMSS>.jsonl` files under `batches/public-merged/<date>/`.
- CDN downloads use `https://huggingface.co/datasets/{repo}/resolve/main/{path}` with retry/backoff on 429 and no Authorization header.
- `project_to_pair` maps heterogeneous source rows to `{prompt, response}` and discards rows where either field is missing/empty after projection.
- Deduplication via `lib/dedup.py` (md5 store) prevents duplicate pairs across runs; manifest-based file list avoids recursive repo API calls.
- `.github/workflows/ingest.yml` passes matrix `SHARD_ID`/`SHARD_TOTAL` (16) and runs the new worker; `bin/gen-file-list.py` emits `file-list.json` for a given date folder.

## qa — qa @ 2026-05-03T02:14:39.903529Z

PASS

1. **Acceptance criteria**
- CLI accepts `SHARD_ID`, `SHARD_TOTAL`, `--repo`, `--date`, `--manifest`, `--out-dir` and exits 0 with valid inputs; exits non-zero on missing required args.
- CDN downloads use `https://huggingface.co/datasets/{repo}/resolve/main/{path}` with no Authorization header; on HTTP 429 retries with ≥360s backoff and succeeds within 5 attempts.
- `project_to_pair` returns `{prompt: str, response: str}` for valid rows and discards rows where either field is missing/empty/whitespace after projection.
- Deterministic shard assignment: for any file key and fixed `SHARD_TOTAL=16`, `shard_assign(key, 16)` always returns the same integer in [0,15].
- Deduplication: running ingestion twice with the same inputs produces identical output content (no duplicate pairs) via `lib/dedup.py` md5 store.
- Output filenames are deterministic and collision-free: `batches/public-merged/<date>/shard<N>-<HHMMSS>.jsonl` where N equals `SHARD_ID` and timestamp is consistent within the run.
- Workflow integration: `.github/workflows/ingest.yml` passes matrix `SHARD_ID`/`SHARD_TOTAL` (16) to the worker and `bin/gen-file-list.py` emits valid `file-list.json` for a given date folder.

2. **Unit tests**
```python
# test_dataset_enrich.py
import json
import hashlib
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

from bin.dataset_enrich import (
    shard_assign,
    load_manifest,
    project_to_pair,
    cdn_download,
)

def test_shard_assign_deterministic():
    key = "some/file.parquet"
    total = 16
    result = shard_assign(key, total)
    assert 0 <= result < total
    assert shard_assign(key, total) == result  # stable

def test_load_manifest(tmp_path):
    manifest = {"date": "2026-05-03", "files": ["a.parquet", "b.parquet"]}
    p = tmp_path / "file-list.json"
    p.write_text(json.dumps(manifest))
    assert load_manifest(p) == manifest

def test_project_to_pair_valid():
    row = {"prompt": "hello", "response": "world", "extra": 1}
    assert project_to_pair(row) == {"prompt": "hello", "response": "world"}

def test_project_to_pair_missing_prompt():
    row = {"response": "world"}
    assert project_to_pair(row) is None

def test_project_to_pair_missing_response():
    row = {"prompt": "hello"}
    assert project_to_pair(row) is None

def test_project_to_pair_empty_after_strip():
    row = {"prompt": "  ", "response": "ok"}
    assert project_to_pair(row) is None

@patch("bin.dataset_enrich.requests.get")
def test_cdn_download_429_retry(mock_get):
    mock_resp_ok = MagicMock()
    mock_resp_ok.status_code = 200
    mock_resp_ok.iter_content.return_value = [b"data"]

    mock_resp_429 = MagicMock()
    mock_resp_429.status_code = 429

    mock_get.side_effect = [mock_resp_429, mock_resp_ok]

    with patch("bin.dataset_enrich.time.sleep") as mock_sleep:
        result = cdn_download("https://huggingface.co/datasets/repo/resolve/main/file", timeout=1)
        assert result == b"data"
        assert mock_sleep.call_count >= 1

@patch("bin.dataset_enrich.requests.get")
def test_cdn_download_no_auth_header(mock_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.iter_content.return_value = [b"data"]
    mock_get.return_value = mock_resp

    cdn_download("https://huggingface.co/datasets/repo/resolve/main/file")
    call_kwargs = mock_get.call_args.kwargs
    assert "Authorization" not in call_kwargs.get("headers", {})
```

3. **Integration tests**
- Happy path: run `bin/dataset-enrich.py` with a small `file-list.json` containing 4 files, `SHARD_ID=3`, `SHARD_TOTAL=16`, valid repo/date; verify that only shard-assigned files are downloaded, projected, deduplicated, and written to `batches/public-merged/<date>/shard3-<HHMMSS>.jsonl` with valid JSONL lines containing `{prompt,response}`.
- Happy path: run twice with identical inputs; second run produces byte-for-byte identical output (dedup prevents duplicates) and does not re-download files unnecessarily (mock CDN 
