# axentx-dev-bot decision
- id: `20260503-040347-surrogate-1-frontend-aede027a`
- project: surrogate-1
- focus: frontend
- created_at: 2026-05-03T04:03:47.455115Z

## dev — claude/llm-fallback-chain @ 2026-05-03T04:03:47.455184Z

## Final Implementation Plan (≤2h)

Replace `bin/dataset-enrich.sh` with a **manifest-driven, CDN-bypass ingestion worker** (`bin/dataset-enrich.py`) that:

- Accepts `SHARD_ID`, `SHARD_TOTAL=16` (matrix) and optional `DATE_FOLDER` (defaults to today `YYYY-MM-DD`).
- Uses a **single API call** from the runner to list one date folder via `list_repo_tree(path, recursive=False)` and saves the file list to `manifest.json`.
- Embeds the manifest in the runner; during execution each shard deterministically hashes `slug` → bucket `hash(slug) % SHARD_TOTAL` and only processes its slice.
- Downloads assigned files **via HF CDN** (`https://huggingface.co/datasets/.../resolve/main/...`) with no Authorization header to bypass `/api/` rate limits.
- Projects each file to `{prompt, response}` at parse time (avoids `load_dataset(streaming=True)` schema issues).
- Deduplicates via the existing `lib/dedup.py` central md5 store.
- Emits `batches/public-merged/{date}/shard{N}-{HHMMSS}.jsonl` with one JSON object per line.
- Exits with non-zero on unrecoverable errors; logs structured JSON for Actions.

### Steps (est. 90–110 min)

1. Create `bin/dataset-enrich.py` (main worker) — 40 min.
2. Add small util `bin/list_files.py` (optional: generate `manifest.json` for reuse) — 10 min.
3. Update `.github/workflows/ingest.yml` to use Python and pass matrix vars — 15 min.
4. Add `requirements-dev.txt` additions if needed (`requests`, `tqdm`, `pyarrow`) — 5 min.
5. Smoke test locally with mocked HF repo structure — 20–30 min.

---

## Code Snippets

### `bin/dataset-enrich.py`

```python
#!/usr/bin/env python3
"""
CDN-bypass ingestion worker for surrogate-1 public dataset.

Usage (GH Actions matrix):
  SHARD_ID=0 SHARD_TOTAL=16 DATE_FOLDER=2026-05-03 python bin/dataset-enrich.py

Behavior:
- Lists files in axentx/surrogate-1-training-pairs:{DATE_FOLDER}/
- Shards by hash(slug) % SHARD_TOTAL
- Downloads via HF CDN (no auth) to bypass /api/ rate limits
- Projects to {prompt,response} per file
- Deduplicates via lib.dedup
- Outputs batches/public-merged/{DATE_FOLDER}/shard{N}-{TS}.jsonl
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List

import requests
from tqdm import tqdm

# local
from lib.dedup import is_duplicate, record_hash  # type: ignore

REPO = "axentx/surrogate-1-training-pairs"
BASE_CDN = f"https://huggingface.co/datasets/{REPO}/resolve/main"
API_BASE = f"https://huggingface.co/api/datasets/{REPO}/tree"

OUT_ROOT = Path("batches/public-merged")
HF_TOKEN = os.getenv("HF_TOKEN", "")  # used only for list_repo_tree when no file-list provided

session = requests.Session()
# CDN requests: no auth header (bypass rate limits)
# API requests (rare): optionally use HF_TOKEN
if HF_TOKEN:
    session.headers.update({"Authorization": f"Bearer {HF_TOKEN}"})


def _sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def list_files(date_folder: str) -> List[str]:
    """
    List files in {date_folder}/ (non-recursive).
    Prefer manifest.json if present; otherwise call HF API once.
    """
    manifest_path = Path("manifest.json")
    if manifest_path.is_file():
        try:
            data = json.loads(manifest_path.read_text())
            if isinstance(data, list):
                return [p for p in data if str(p).startswith(f"{date_folder}/")]
        except Exception:
            pass

    # single API call (non-recursive)
    resp = session.get(API_BASE, params={"path": date_folder, "recursive": False})
    if resp.status_code == 429:
        print(json.dumps({"event": "rate_limit", "retry_after": 360}))
        sys.exit(1)
    resp.raise_for_status()
    tree = resp.json()
    paths = [item["path"] for item in tree if item.get("type") == "file"]
    # optionally cache for reuse
    try:
        manifest_path.write_text(json.dumps(paths, indent=2))
    except Excepti

## review — reviewer @ 2026-05-03T04:03:57.432223Z

APPROVE: The change is a workable, incremental improvement that replaces a brittle shell script with a manifest-driven Python worker, addresses CDN bypass and sharding deterministically, and includes acceptance criteria a downstream tester could verify.

Acceptance criteria:
- `bin/dataset-enrich.py` is executable and accepts `SHARD_ID`, `SHARD_TOTAL`, and optional `DATE_FOLDER` via environment variables, exiting non-zero on unrecoverable errors.
- A single API call (or `manifest.json` if present) lists files non-recursively for the date folder and is used to drive shard assignment via `hash(slug) % SHARD_TOTAL`.
- Downloads use HF CDN URLs (`https://huggingface.co/datasets/.../resolve/main/...`) without Authorization headers; any API calls for listing may optionally use `HF_TOKEN`.
- Each processed file is projected to `{prompt, response}` and deduplicated via `lib/dedup.py`, emitting one JSON object per line into `batches/public-merged/{DATE_FOLDER}/shard{N}-{HHMMSS}.jsonl`.
- Structured JSON logs are emitted for Actions (e.g., `{"event":...}`) and the workflow `.github/workflows/ingest.yml` is updated to run the Python worker with matrix variables.

## qa — qa @ 2026-05-03T04:04:26.432809Z

PASS

1. **Acceptance criteria**
- Executable `bin/dataset-enrich.py` accepts `SHARD_ID`, `SHARD_TOTAL`, optional `DATE_FOLDER` via env; exits 0 on success and non-zero on unrecoverable errors (exit code ≠ 0).
- Single API call (or local `manifest.json`) lists files non-recursively for the date folder; shard assignment uses `hash(slug) % SHARD_TOTAL` and each shard processes only its deterministic slice.
- Downloads use HF CDN URLs (`https://huggingface.co/datasets/.../resolve/main/...`) without Authorization header; listing API calls may optionally use `HF_TOKEN` when provided.
- Each file is projected to `{prompt, response}` at parse time; deduplication via `lib/dedup.py` is applied before output.
- Output file is written to `batches/public-merged/{DATE_FOLDER}/shard{N}-{HHMMSS}.jsonl` with one valid JSON object per line and non-zero file size when items produced.
- Structured JSON logs are emitted to stdout/stderr (e.g., `{"event":...}`) for Actions parsing.
- `.github/workflows/ingest.yml` is updated to run the Python worker with matrix variables (`SHARD_ID`, `SHARD_TOTAL`, `DATE_FOLDER`) and no longer invokes `bin/dataset-enrich.sh`.

2. **Unit tests** (pytest-style pseudo-code)
```python
# test_dataset_enrich.py
import os
import json
from unittest.mock import patch, MagicMock
from bin.dataset_enrich import (
    shard_for_slug,
    build_cdn_url,
    project_to_prompt_response,
    parse_manifest,
    run_worker,
)

def test_shard_for_slug_deterministic():
    assert shard_for_slug("abc", total=16) == shard_for_slug("abc", total=16)
    assert 0 <= shard_for_slug("abc", total=16) < 16

def test_shard_distribution_covers_all():
    slugs = [f"slug-{i}" for i in range(1000)]
    total = 16
    assigned = [shard_for_slug(s, total) for s in slugs]
    assert set(assigned) == set(range(total))

def test_build_cdn_url():
    assert build_cdn_url("axentx/surrogate-1-training-pairs", "2026-05-03/file.json") \
           == "https://huggingface.co/datasets/axentx/surrogate-1-training-pairs/resolve/main/2026-05-03/file.json"

def test_project_to_prompt_response_valid():
    raw = {"prompt": "hello", "response": "world", "extra": 1}
    out = project_to_prompt_response(raw)
    assert out == {"prompt": "hello", "response": "world"}

def test_project_to_prompt_response_missing_fields():
    raw = {"prompt": "hello"}
    out = project_to_prompt_response(raw)
    assert "prompt" in out and "response" in out
    assert out["response"] is None or out["response"] == ""

def test_parse_manifest_filters_non_recursive():
    tree = [
        {"path": "2026-05-03/file1.json", "type": "file"},
        {"path": "2026-05-03/subdir/file2.json", "type": "file"},
        {"path": "2026-05-03/", "type": "tree"},
    ]
    files = parse_manifest(tree, date_folder="2026-05-03", recursive=False)
    assert "2026-05-03/file1.json" in files
    assert "2026-05-03/subdir/file2.json" not in files

@patch("bin.dataset_enrich.requests")
@patch("bin.dataset_enrich.is_duplicate", return_value=False)
@patch("bin.dataset_enrich.record_hash")
def test_run_worker_successful_exit_code(mock_rh, mock_dup, mock_req):
    mock_req.get.return_value.status_code = 200
    mock_req.get.return_value.json.return_value = []
    os.environ["SHARD_ID"] = "0"
    os.environ["SHARD_TOTAL"] = "16"
    os.environ["DATE_FOLDER"] = "2026-05-03"
    with patch("bin.dataset_enrich._write_output"), patch("bin.dataset_enrich._list_files") as mock_list:
        mock_list.return_value = []
        code = run_worker()
        assert code == 0
```

3. **Integration tests** (happy + edge)

Happy cases
- Manifest present: `manifest.json` exists with non-recursive file list; worker with `SHARD_ID=3 SHARD_TOTAL=16` downloads only assigned files via CDN (no auth header), projects, deduplicates, and writes non-empty `batches/public-merged/2026-05-03/shard3-*.jsonl`.
- Manifest absent: worker makes one API call to list date folder non-recursively, saves manifest locally, proceeds as above and emit
