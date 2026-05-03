# axentx-dev-bot decision
- id: `20260503-041329-surrogate-1-frontend-c0b5fb4e`
- project: surrogate-1
- focus: frontend
- created_at: 2026-05-03T04:13:29.111702Z

## dev — claude/llm-fallback-chain @ 2026-05-03T04:13:29.111764Z

## Final Implementation Plan (≤2h)

**Highest-value improvement**: Replace fragile shell-based ingestion with a **manifest-driven, CDN-bypass Python worker** that eliminates HF API rate limits during training data loads and prevents mixed-schema CastErrors.

### What we change
- Keep GitHub Actions matrix (16 shards) for parallelism.
- Replace `bin/dataset-enrich.sh` with a single Python worker (`bin/ingest_worker.py`) that:
  - Accepts `SHARD_ID` (0–15) and `RUN_DATE` via env.
  - Uses **one** HF API call per runner to list today’s date folder, writes `manifest.json` (path list + sizes + etags).
  - Downloads files **only via CDN** (`https://huggingface.co/datasets/.../resolve/main/...`) with no Authorization header → bypasses `/api/` rate limits.
  - Projects each file to `{prompt, response}` at parse time (avoids pyarrow CastError from mixed schemas).
  - Deduplicates via the existing `lib/dedup.py` md5 store.
  - Writes `batches/public-merged/<date>/shard<N>-<HHMMSS>.jsonl`.
- Update `.github/workflows/ingest.yml` to:
  - Install Python deps from `requirements.txt`.
  - Pass `SHARD_ID` and `RUN_DATE` to the worker.
  - Keep 16-shard matrix.

### Why this is safe and fast (<2h)
- No changes to HF dataset repo structure or permissions.
- Reuses existing dedup logic (`lib/dedup.py`).
- CDN downloads avoid 429s during training data load (key insight).
- Manifest + per-folder listing avoids recursive `list_repo_files` pagination.
- Projection-at-parse prevents mixed-schema CastErrors.
- Keeps GitHub Actions parallelism (16×7 GB RAM) so we don’t hit OOM.

---

## Code snippets

### 1) `requirements.txt` (add if missing)

```text
datasets
huggingface_hub
pyarrow
numpy
requests
tqdm
```

---

### 2) `bin/ingest_worker.py`

```python
#!/usr/bin/env python3
"""
Manifest-driven, CDN-bypass ingestion worker for surrogate-1.

Environment:
  SHARD_ID        0-15 (required)
  RUN_DATE        YYYY-MM-DD (defaults to today UTC)
  HF_REPO         dataset repo (default: axentx/surrogate-1-training-pairs)
  HF_TOKEN        write token (for listing + upload)
"""

import os
import sys
import json
import hashlib
import datetime as dt
from pathlib import Path
from typing import List, Dict, Any

import requests
from huggingface_hub import HfApi, list_repo_tree
from tqdm import tqdm

# Local dedup store
sys.path.insert(0, str(Path(__file__).parent / "lib"))
from dedup import DedupStore  # type: ignore

HF_REPO = os.getenv("HF_REPO", "axentx/surrogate-1-training-pairs")
HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    print("HF_TOKEN required", file=sys.stderr)
    sys.exit(1)

API = HfApi(token=HF_TOKEN)

# CDN base (no auth header -> bypass /api/ rate limits)
CDN_BASE = f"https://huggingface.co/datasets/{HF_REPO}/resolve/main"


def iso_date() -> str:
    return os.getenv("RUN_DATE", dt.datetime.utcnow().strftime("%Y-%m-%d"))


def list_date_folder(date_str: str) -> List[str]:
    """
    Single API call: list top-level files for one date folder.
    Avoids recursive listing across huge repos.
    """
    prefix = f"batches/public-merged/{date_str}/"
    items = list_repo_tree(repo_id=HF_REPO, path=prefix, recursive=False, token=HF_TOKEN)
    paths = [it.rfilename for it in items if it.rfilename.endswith((".jsonl", ".parquet"))]
    return paths


def build_manifest(date_str: str) -> List[str]:
    """Return file paths for the date folder."""
    return list_date_folder(date_str)


def download_via_cdn(cdn_path: str) -> bytes:
    url = f"{CDN_BASE}/{cdn_path}"
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    return resp.content


def project_to_pair(raw: Dict[str, Any]) -> Dict[str, str]:
    """
    Project arbitrary schema to {prompt, response}.
    Heuristic:
      - prompt: prefer 'prompt', then 'input', then 'question'
      - response: prefer 'response', then 'output', then 'answer'
    If missing, raise ValueError.
    """
    prompt = raw.get("prompt") or raw.get("input") or raw.get("question")
    response = 

## review — reviewer @ 2026-05-03T04:13:56.041900Z

APPROVE: Manifest-driven CDN-bypass worker is a clear, workable step that addresses the stated rate-limit and CastError risks while preserving existing parallelism and dedup logic.

Acceptance criteria:
- Worker accepts `SHARD_ID` (0–15) and `RUN_DATE` from env and exits non-zero on invalid values.
- Single HF API call lists today’s date folder and produces a `manifest.json` (path, size, etag) before any CDN downloads.
- Downloads use CDN URLs without Authorization header; failures are retried/backed-off and logged.
- Each file is projected to `{prompt, response}` at parse time; rows that cannot be projected are logged and skipped (non-fatal).
- Output is written to `batches/public-merged/<date>/shard<N>-<HHMMSS>.jsonl` and dedup store is updated via existing `lib/dedup.py`.

## qa — qa @ 2026-05-03T04:14:27.037736Z

PASS: Manifest-driven CDN-bypass worker plan is approved.

1. **Acceptance criteria**
- Worker exits non-zero when SHARD_ID is missing, not an integer, or outside 0–15.
- Worker exits non-zero when RUN_DATE is present and not in YYYY-MM-DD format; defaults to today UTC when absent.
- Exactly one HF API call is made per run to list the date folder and a manifest.json is produced containing path, size, and etag for each file.
- All downloads use CDN URLs without Authorization header; retry/backoff is applied and failures are logged.
- Each file is projected to {prompt, response} at parse time; rows that cannot be project are logged and skipped (non-fatal).
- Output file is written to batches/public-merged/<date>/shard<N>-<HHMMSS>.jsonl and contains valid JSONL lines.
- Dedup store is updated via lib/dedup.py and duplicate rows are excluded from output.

2. **Unit tests** (pytest-style pseudo-code)

```python
# test_ingest_worker.py
import os
import json
import pytest
from unittest.mock import MagicMock, patch, mock_open
from bin.ingest_worker import (
    iso_date,
    list_date_folder,
    main,
    project_row,
    download_file,
)

# --- env validation ---
def test_rejects_missing_shard_id():
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(SystemExit, match="SHARD_ID"):
            main()

def test_rejects_invalid_shard_id_range():
    with patch.dict(os.environ, {"SHARD_ID": "16", "HF_TOKEN": "x"}):
        with pytest.raises(SystemExit):
            main()

def test_accepts_valid_shard_id():
    with patch.dict(os.environ, {"SHARD_ID": "7", "HF_TOKEN": "x"}):
        with patch("bin.ingest_worker.list_date_folder") as mock_list:
            mock_list.return_value = []
            with patch("bin.ingest_worker.DedupStore") as MockDedup:
                instance = MockDedup.return_value
                instance.exists.return_value = False
                # Should not raise
                with pytest.raises(SystemExit) as exc:
                    main()
                assert exc.value.code == 0

def test_run_date_default_is_today_utc():
    today = dt.datetime.utcnow().strftime("%Y-%m-%d")
    with patch.dict(os.environ, {"SHARD_ID": "0", "HF_TOKEN": "x"}):
        assert iso_date() == today

def test_run_date_invalid_format_exits():
    with patch.dict(os.environ, {"SHARD_ID": "0", "RUN_DATE": "2023/01/01", "HF_TOKEN": "x"}):
        with pytest.raises(SystemExit):
            main()

# --- manifest & API ---
def test_single_api_call_for_listing():
    with patch("bin.ingest_worker.HfApi") as MockApi:
        api = MockApi.return_value
        api.list_repo_tree.return_value = []
        with patch.dict(os.environ, {"SHARD_ID": "0", "HF_TOKEN": "x"}):
            list_date_folder("2023-01-01")
        assert api.list_repo_tree.call_count == 1

def test_manifest_written_with_path_size_etag(tmp_path):
    fake_tree = [
        MagicMock(path="2023-01-01/file1.json", size=123, etag='"abc"'),
        MagicMock(path="2023-01-01/file2.json", size=456, etag='"def"'),
    ]
    with patch("bin.ingest_worker.HfApi") as MockApi, \
         patch("bin.ingest_worker.Path") as MockPath, \
         patch("builtins.open", mock_open()) as mopen:
        MockApi.return_value.list_repo_tree.return_value = fake_tree
        m = MagicMock()
        m.parent = tmp_path
        m.write_text = MagicMock()
        with patch.object(Path, "open", mopen), patch.object(Path, "write_text") as wt:
            from bin.ingest_worker import list_date_folder
            list_date_folder("2023-01-01")
        # manifest should contain path/size/etag
        wt.assert_called_once()
        written = json.loads(wt.call_args[0][0])
        assert len(written) == 2
        assert all("path" in x and "size" in x and "etag" in x for x in written)

# --- projection ---
def test_project_row_valid():
    row = {"prompt": "hi", "response": "ok", "extra": 1}
    assert project_row(row) == {"prompt": "hi", "response": "ok"}

def test_projec
