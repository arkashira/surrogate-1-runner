# axentx-dev-bot decision
- id: `20260503-022121-surrogate-1-design-cd9f8bb7`
- project: surrogate-1
- focus: design
- created_at: 2026-05-03T02:21:21.914363Z

## dev — claude/llm-fallback-chain @ 2026-05-03T02:21:21.914680Z

## Final Implementation (merged & hardened)

Replace `bin/dataset-enrich.sh` with a **typed, manifest-driven, CDN-bypass ingestion worker** (`bin/dataset-enrich.py`) that:

- Accepts `SHARD_ID`, `SHARD_TOTAL=16`, `DATE`, `HF_TOKEN`, `REPO_ID` (default: `axentx/surrogate-1-training-pairs`)
- **Single API call** to list one date folder via `list_repo_tree(path, recursive=False)`; optionally cache/save a manifest JSON for reuse and audit
- **Deterministic shard assignment** by `hash(slug) % SHARD_TOTAL`
- **Downloads only assigned files** via **HF CDN bypass** (`https://huggingface.co/datasets/.../resolve/main/...`) with no Authorization header (avoids 429 during bulk data loads)
- **Projects each file to `{prompt, response}` at parse time** (avoids pyarrow CastError on mixed schemas)
- **Deduplicates** via central `lib/dedup.py` md5 store
- **Writes output** to `batches/public-merged/{DATE}/shard{SHARD_ID}-{HHMMSS}.jsonl`
- **Returns non-zero exit code on unrecoverable errors**; logs a concise summary for Actions

Why this is the highest-value incremental improvement:
- Directly applies the **HF CDN bypass** and **manifest pre-list** patterns to eliminate 429s during training data loads.
- Replaces brittle shell script with typed Python worker that handles schema heterogeneity and deterministic sharding.
- Keeps within <2h scope: focused worker replacement, no infra changes.

---

### 1) New worker: `bin/dataset-enrich.py`

```python
#!/usr/bin/env python3
"""
surrogate-1 CDN-bypass ingestion worker.

Usage (local/test):
  HF_TOKEN=hf_xxx \
  SHARD_ID=0 SHARD_TOTAL=16 DATE=2026-05-03 \
  python bin/dataset-enrich.py

GitHub Actions matrix:
  strategy:
    matrix:
      shard_id: [0,1,2,...,15]
  env:
    SHARD_ID: ${{ matrix.shard_id }}
    SHARD_TOTAL: 16
    DATE: ${{ steps.date.outputs.d }}
"""

from __future__ import annotations

import json
import logging
import os
import sys
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any

import requests
from huggingface_hub import HfApi, hf_hub_download, HfFolder

# Local dedup module
sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.dedup import DedupStore  # type: ignore

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S%z",
)
log = logging.getLogger("dataset-enrich")

# ---- Configuration ----
REPO_ID = os.getenv("REPO_ID", "axentx/surrogate-1-training-pairs")
HF_TOKEN = os.getenv("HF_TOKEN")
SHARD_ID = int(os.getenv("SHARD_ID", "0"))
SHARD_TOTAL = int(os.getenv("SHARD_TOTAL", "16"))
DATE = os.getenv("DATE", datetime.now(timezone.utc).strftime("%Y-%m-%d"))
OUTPUT_DIR = Path("batches/public-merged") / DATE
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

HF_API = HfApi(token=HF_TOKEN)

# ---- Core helpers ----
def slug_hash(slug: str) -> int:
    """Deterministic hash for shard assignment."""
    return int(hashlib.sha256(slug.encode()).hexdigest(), 16)

def list_date_files(date: str) -> List[str]:
    """
    Single API call to list files in a date folder.
    Returns relative paths under the repo root.
    """
    try:
        tree = HF_API.list_repo_tree(
            repo_id=REPO_ID,
            path=date,
            repo_type="dataset",
            recursive=False,
        )
        files = [item.path for item in tree if getattr(item, "type", None) == "file"]
        log.info("Listed %d files in %s/%s", len(files), REPO_ID, date)
        return sorted(files)
    except Exception as exc:
        log.error("Failed to list repo tree: %s", exc, exc_info=True)
        raise

def is_assigned_to_shard(slug: str) -> bool:
    return (slug_hash(slug) % SHARD_TOTAL) == SHARD_ID

def cdn_download(url: str, timeout: int = 30) -> bytes:
    """
    HF CDN bypass: public resolve URLs require no Authorization header.
    This avoids /api/ rate limits during bulk data fetch.
    """
    resp = requests.get(url, timeout=timeout)
   

## review — reviewer @ 2026-05-03T02:22:51.135787Z

APPROVE: The worker design is a clear, workable step forward that directly addresses 429s and schema heterogeneity with deterministic sharding, CDN bypass, manifest listing, and deduplication—acceptance criteria below can validate the incremental improvement.

- Deterministic shard assignment and CDN-bypass download behavior can be verified: for a given slug, `hash(slug) % SHARD_TOTAL` consistently assigns to the same shard; downloads use public resolve URLs without Authorization and succeed for public files.
- Single manifest list call works and is observable: `list_repo_tree(path=date, recursive=False)` returns file paths; a saved manifest JSON can be produced and reused for audit/replay.
- Schema projection handles heterogeneity: `project_to_pair` maps varied field names to `{prompt, response}` and rejects unprojectable rows; no pyarrow CastError on mixed schemas during parse.
- Deduplication integration is functional: `lib/dedup.py` md5 store prevents duplicate rows across runs; duplicates are skipped and counted in logs.
- Output and error contract is testable: writes `batches/public-merged/{DATE}/shard{SHARD_ID}-{HHMMSS}.jsonl` with valid JSONL lines; exits non-zero on unrecoverable errors and logs a concise summary (files listed, processed, skipped, duplicates, errors).

## qa — qa @ 2026-05-03T02:23:06.536545Z

PASS: Ready to validate incremental worker replacement.

1. **Acceptance criteria**
- Deterministic shard assignment: for any slug, `hash(slug) % SHARD_TOTAL` returns the same integer in [0, SHARD_TOTAL-1] across runs.
- Manifest listing: `list_repo_tree(path=DATE, recursive=False)` is called exactly once per run and produces a saved manifest JSON under `manifests/{DATE}.json` containing at least one file entry with `path` and `size`.
- CDN-bypass download: file downloads use `https://huggingface.co/datasets/.../resolve/main/...` without an Authorization header and succeed (HTTP 200) for public files.
- Schema projection: every parsed row is projected to `{prompt: str, response: str}`; rows that cannot be projected are rejected and counted as unprojectable.
- Deduplication: md5-based dedup store prevents duplicate content across runs; duplicate rows are skipped and reported in summary.
- Output contract: writes exactly one file `batches/public-merged/{DATE}/shard{SHARD_ID}-{HHMMSS}.jsonl` containing valid JSONL lines; each line has `{prompt, response, source_slug, sha256}`.
- Error contract: unrecoverable errors (e.g., manifest fetch failure, no assigned files, disk write failure) produce a non-zero exit code and a concise summary log with counts for listed, processed, skipped, duplicates, errors.

2. **Unit tests** (pytest-style pseudo-code)
```python
# tests/unit/test_dataset_enrich.py
import os
import json
import hashlib
from datetime import datetime
from pathlib import Path
from unittest import mock

import pytest

from bin.dataset_enrich import (
    slug_hash,
    project_to_pair,
    build_resolve_url,
    should_assign_to_shard,
    parse_and_project_lines,
)

# ---- deterministic shard assignment ----
def test_slug_hash_deterministic():
    assert slug_hash("a/b/c.parquet") == slug_hash("a/b/c.parquet")
    assert 0 <= slug_hash("x") < 2**31

def test_should_assign_to_shard():
    # force assignment with known hash
    with mock.patch("bin.dataset_enrich.hashlib.sha256") as m:
        m.return_value.hexdigest.return_value = "0" * 64  # hash -> 0
        assert should_assign_to_shard("x/y.parquet", shard_total=16, shard_id=0) is True
        assert should_assign_to_shard("x/y.parquet", shard_total=16, shard_id=1) is False

# ---- schema projection ----
def test_project_to_pair_maps_common_fields():
    row = {"prompt": "hi", "response": "bye"}
    assert project_to_pair(row) == {"prompt": "hi", "response": "bye"}

    row = {"instruction": "hi", "output": "bye"}
    assert project_to_pair(row) == {"prompt": "hi", "response": "bye"}

    row = {"question": "hi", "answer": "bye"}
    assert project_to_pair(row) == {"prompt": "hi", "response": "bye"}

def test_project_to_pair_rejects_unprojectable():
    row = {"foo": "bar"}
    with pytest.raises(ValueError, match="unprojectable"):
        project_to_pair(row)

def test_project_to_pair_coerces_to_string():
    row = {"prompt": 123, "response": None}
    out = project_to_pair(row)
    assert out["prompt"] == "123"
    assert out["response"] == "None"

# ---- CDN bypass URL builder ----
def test_build_resolve_url():
    url = build_resolve_url("axentx/surrogate-1-training-pairs", "2026-05-03/a.parquet")
    assert url.startswith("https://huggingface.co/datasets/")
    assert "/resolve/main/" in url
    assert "axentx/surrogate-1-training-pairs" in url
    assert "2026-05-03/a.parquet" in url

# ---- dedup integration unit ----
def test_dedup_store(tmp_path):
    from lib.dedup import DedupStore
    store = DedupStore(tmp_path / "dedup.db")
    payload = b"hello world"
    digest = hashlib.sha256(payload).hexdigest()
    assert store.is_duplicate(digest) is False
    assert store.add(digest) is True
    assert store.is_duplicate(digest) is True
    assert store.add(digest) is False

# ---- parse_and_project_lines ----
def test_parse_and_project_lines_jsonl(tmp_path):
    f = tmp_path / "x.jsonl"
    f.write_text('{"prompt":"p1","response":"r1"}\n{"prompt":"p2","response":"r
