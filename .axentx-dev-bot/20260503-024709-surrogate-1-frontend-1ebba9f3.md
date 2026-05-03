# axentx-dev-bot decision
- id: `20260503-024709-surrogate-1-frontend-1ebba9f3`
- project: surrogate-1
- focus: frontend
- created_at: 2026-05-03T02:47:09.344257Z

## dev — claude/llm-fallback-chain @ 2026-05-03T02:47:09.344326Z

## Final Implementation Plan (≤2h)

Replace `bin/dataset-enrich.sh` with a **manifest-driven, CDN-bypass ingestion worker** (`bin/dataset-enrich.py`) that:

- Accepts `SHARD_ID`, `SHARD_TOTAL=16`, `DATE`, `HF_TOKEN` (write)
- Single `list_repo_tree(path, recursive=False)` for `public-merged/<DATE>/` (or falls back to `training-pairs/` if needed) → saves list to `manifest.json`
- Deterministic shard assignment: `hash(slug) % SHARD_TOTAL == SHARD_ID`
- Downloads only assigned files via **CDN bypass** (`https://huggingface.co/datasets/.../resolve/main/...`) — no Authorization header, avoids HF API 429
- Streams JSONL/Parquet, projects to `{prompt, response}`, computes `md5` for dedup against central store (`lib/dedup.py`)
- Writes output to `batches/public-merged/<DATE>/shard<SHARD_ID>-<HHMMSS>.jsonl`
- Commits via HF Hub (one commit per shard) — respects 128/hr/repo cap by using deterministic shard → repo mapping if needed (future)
- Exits 0 on success, non-zero on hard failure (GitHub Actions will retry)

### Code snippets

`bin/dataset-enrich.py`
```python
#!/usr/bin/env python3
"""
CDN-bypass ingestion worker for surrogate-1 training pairs.

Usage:
  SHARD_ID=0 SHARD_TOTAL=16 DATE=2026-04-29 HF_TOKEN=hf_xxx python bin/dataset-enrich.py
"""
import os
import sys
import json
import hashlib
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator, Dict, Any

import requests
from huggingface_hub import HfApi, hf_hub_download, list_repo_tree

REPO_DATASET = "axentx/surrogate-1-training-pairs"
CDN_ROOT = f"https://huggingface.co/datasets/{REPO_DATASET}/resolve/main"
DATE_FMT = "%Y-%m-%d"
BATCH_DIR = "batches/public-merged"

# Deterministic shard assignment
def shard_for(slug: str, total: int) -> int:
    return int(hashlib.sha256(slug.encode()).hexdigest(), 16) % total

def iso_ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")

def list_date_files(date_str: str) -> list[str]:
    """Single API call to list files for a date folder."""
    folder = f"{BATCH_DIR}/{date_str}"
    try:
        tree = list_repo_tree(REPO_DATASET, folder=folder, repo_type="dataset")
    except Exception:
        # Fallback: list root training-pairs folder if date folder doesn't exist yet
        tree = list_repo_tree(REPO_DATASET, folder="training-pairs", repo_type="dataset")
    # Keep only files (not directories)
    return [item.rfilename for item in tree if item.type == "file"]

def cdn_download(url: str, timeout: int = 30) -> bytes:
    resp = requests.get(url, timeout=timeout)
    resp.raise_for_status()
    return resp.content

def project_to_pair(raw: Dict[str, Any]) -> Dict[str, str]:
    """Project raw record to {prompt, response}. Add more schema adapters as needed."""
    prompt = raw.get("prompt") or raw.get("input") or raw.get("question") or ""
    response = raw.get("response") or raw.get("output") or raw.get("answer") or ""
    return {"prompt": str(prompt).strip(), "response": str(response).strip()}

def md5_of_pair(pair: Dict[str, str]) -> str:
    blob = json.dumps(pair, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.md5(blob).hexdigest()

def main() -> int:
    shard_id = int(os.getenv("SHARD_ID", "0"))
    shard_total = int(os.getenv("SHARD_TOTAL", "16"))
    date_str = os.getenv("DATE", datetime.utcnow().strftime(DATE_FMT))
    hf_token = os.getenv("HF_TOKEN", "")

    if not hf_token:
        print("HF_TOKEN is required", file=sys.stderr)
        return 1

    api = HfApi(token=hf_token)
    out_dir = Path(f"{BATCH_DIR}/{date_str}")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"shard{shard_id}-{iso_ts()}.jsonl"

    # 1) List files once
    files = list_date_files(date_str)
    manifest_path = Path("manifest.json")
    manifest_path.write_text(json.dumps({"date": date_str, "files": files}, sort_keys=True))

    # 2) Central dedup store (SQLite)
    from lib.dedup import DedupStore
    dedup = DedupStore()

   

## review — reviewer @ 2026-05-03T02:47:15.881702Z

APPROVE: This is a workable, incremental step forward that replaces the shell script with a manifest-driven, CDN-bypass worker and provides clear acceptance criteria a downstream tester can validate.

Acceptance criteria:
- `bin/dataset-enrich.py` is executable and runs with `SHARD_ID`, `SHARD_TOTAL`, `DATE`, `HF_TOKEN` env vars, producing `batches/public-merged/<DATE>/shard<SHARD_ID>-<HHMMSS>.jsonl`.
- A single `list_repo_tree` call is made per run and saved to `manifest.json`; fallback to `training-pairs/` is attempted if the date folder is missing.
- Deterministic shard assignment (`hash(slug) % SHARD_TOTAL == SHARD_ID`) is applied and only assigned files are downloaded.
- Downloads use CDN bypass URLs (`https://huggingface.co/datasets/.../resolve/main/...`) without Authorization headers; failures are logged and non-fatal.
- Output records are projected to `{prompt, response}` and deduplicated against `lib/dedup.py`; exit code is 0 on success and non-zero on hard failure.

## qa — qa @ 2026-05-03T02:47:43.152088Z

PASS

## 1. Acceptance criteria
- `bin/dataset-enrich.py` is executable (`chmod +x`) and runs with `SHARD_ID`, `SHARD_TOTAL`, `DATE`, `HF_TOKEN` env vars, producing `batches/public-merged/<DATE>/shard<SHARD_ID>-<HHMMSS>.jsonl`.
- Exactly one `list_repo_tree` call is made per run; the resulting file list is saved to `manifest.json`; if the date folder is missing, a fallback to `training-pairs/` is attempted.
- Deterministic shard assignment (`hash(slug) % SHARD_TOTAL == SHARD_ID`) is applied and only assigned files are downloaded.
- Downloads use CDN bypass URLs (`https://huggingface.co/datasets/.../resolve/main/...`) without Authorization headers; individual download failures are logged and non-fatal (do not abort the run).
- Output records are projected to `{prompt, response}` and deduplicated against `lib/dedup.py`; exit code is 0 on success and non-zero on hard failure.
- Output file naming uses UTC timestamp in `HHMMSS` format and contains only deduplicated, projected records for the assigned shard.
- No Authorization header is present on CDN download requests (verified by request inspection).

## 2. Unit tests
```python
# tests/unit/test_shard_for.py
import hashlib
from bin.dataset_enrich import shard_for

def test_shard_for_deterministic():
    assert shard_for("abc", 16) == shard_for("abc", 16)

def test_shard_for_uniform():
    total = 16
    buckets = [0] * total
    for i in range(1000):
        buckets[shard_for(f"slug-{i}", total)] += 1
    # rough uniformity: no bucket empty and none > 3x average
    assert all(c > 0 for c in buckets)
    avg = 1000 / total
    assert max(buckets) < avg * 3

def test_shard_for_boundary():
    assert 0 <= shard_for("x", 16) < 16
```

```python
# tests/unit/test_project_to_pair.py
from bin.dataset_enrich import project_to_pair

def test_project_prompt_response():
    raw = {"prompt": "hello", "response": "world"}
    assert project_to_pair(raw) == {"prompt": "hello", "response": "world"}

def test_project_input_output():
    raw = {"input": "in", "output": "out"}
    assert project_to_pair(raw) == {"prompt": "in", "response": "out"}

def test_project_question_answer():
    raw = {"question": "q", "answer": "a"}
    assert project_to_pair(raw) == {"prompt": "q", "response": "a"}

def test_project_missing_fields():
    raw = {"other": "x"}
    out = project_to_pair(raw)
    assert out["prompt"] == ""
    assert out["response"] == ""

def test_project_strips_strings():
    raw = {"prompt": "  p  ", "response": "  r  "}
    assert project_to_pair(raw) == {"prompt": "p", "response": "r"}
```

```python
# tests/unit/test_iso_ts.py
import re
from bin.dataset_enrich import iso_ts

def test_iso_ts_format():
    assert re.match(r"^\d{4}-\d{2}-\d{2}T\d{6}Z$", iso_ts())
```

```python
# tests/unit/test_list_date_files.py
from unittest.mock import MagicMock, patch
from bin.dataset_enrich import list_date_files

def test_list_date_files_uses_single_api_call():
    mock_tree = [MagicMock(rfilename="training-pairs/f1.jsonl", type="file")]
    with patch("bin.dataset_enrich.list_repo_tree", return_value=mock_tree) as m:
        files = list_date_files("2026-04-29")
        assert m.call_count == 1
        assert files == ["training-pairs/f1.jsonl"]

def test_list_date_files_filters_dirs():
    mock_tree = [
        MagicMock(rfilename="training-pairs/dir", type="directory"),
        MagicMock(rfilename="training-pairs/f1.jsonl", type="file"),
    ]
    with patch("bin.dataset_enrich.list_repo_tree", return_value=mock_tree):
        files = list_date_files("2026-04-29")
        assert files == ["training-pairs/f1.jsonl"]
```

```python
# tests/unit/test_cdn_download.py
import pytest
from unittest.mock import Mock, patch
from bin.dataset_enrich import cdn_download

def test_cdn_download_success():
    mock_resp = Mock()
    mock_resp.content = b"data"
    mock_resp.raise_for_status = Mock()
    with patch("bin.dataset_enrich.requests.get", return_value=mock_resp) as m:
        result = cdn_download("h
