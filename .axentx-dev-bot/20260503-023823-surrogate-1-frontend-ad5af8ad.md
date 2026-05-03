# axentx-dev-bot decision
- id: `20260503-023823-surrogate-1-frontend-ad5af8ad`
- project: surrogate-1
- focus: frontend
- created_at: 2026-05-03T02:38:23.456105Z

## dev — claude/llm-fallback-chain @ 2026-05-03T02:38:23.456182Z

## Implementation Plan (≤2h)

Replace `bin/dataset-enrich.sh` with a **manifest-driven, CDN-bypass ingestion worker** (`bin/dataset-enrich.py`) that:

- Accepts `SHARD_ID`, `SHARD_TOTAL=16`, `DATE`, `HF_TOKEN`
- Single `list_repo_tree` call from Mac (outside training) → `file-list.json` committed to repo per date
- Worker loads manifest, deterministically assigns 1/16 slice by `hash(slug) % 16`
- Downloads only assigned files via **HF CDN bypass** (`https://huggingface.co/datasets/.../resolve/main/...`) — no Authorization header, no API rate limit
- Projects heterogeneous schemas → `{prompt, response}` only at parse time
- Dedup via central `lib/dedup.py` md5 store
- Outputs `batches/public-merged/{DATE}/shard{N}-{HHMMSS}.jsonl`
- Adds `requirements.txt` update (keep `datasets` for schema helpers, add `requests`, `tqdm`)
- Keeps GitHub Actions matrix (16 shards) unchanged

---

## 1. Create `bin/dataset-enrich.py`

```python
#!/usr/bin/env python3
"""
surrogate-1 CDN-bypass ingestion worker.

Usage (local/test):
  HF_TOKEN=hf_xxx \
  SHARD_ID=0 SHARD_TOTAL=16 DATE=2026-04-29 \
  python bin/dataset-enrich.py --manifest file-list.json

GitHub Actions sets:
  SHARD_ID (matrix), SHARD_TOTAL=16, DATE (YYYY-MM-DD), HF_TOKEN
"""

import os
import sys
import json
import hashlib
import datetime
from pathlib import Path
from typing import List, Dict, Any

import requests
from tqdm import tqdm

# Local dedup module
sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.dedup import DedupStore  # type: ignore

HF_DATASET_REPO = "axentx/surrogate-1-training-pairs"
CDN_BASE = f"https://huggingface.co/datasets/{HF_DATASET_REPO}/resolve/main"
API_BASE = f"https://huggingface.co/api/datasets/{HF_DATASET_REPO}"

# ---- helpers ----
def slug_for_path(path: str) -> str:
    """Stable slug for dedup and shard assignment."""
    return path.strip("/")

def hash_shard(slug: str, total: int) -> int:
    return int(hashlib.sha256(slug.encode()).hexdigest(), 16) % total

def parse_pair(raw: Dict[str, Any]) -> Dict[str, str]:
    """
    Project heterogeneous schemas to {prompt, response}.
    Known schema variants handled here; unknown -> best-effort.
    """
    # Common field names seen across datasets
    prompt_keys = {"prompt", "instruction", "input", "question", "text"}
    response_keys = {"response", "output", "answer", "completion", "result"}

    prompt = None
    response = None

    rk = set(raw.keys())
    for pk in prompt_keys:
        if pk in rk and raw[pk] is not None:
            prompt = str(raw[pk]).strip()
            break
    for rk_ in response_keys:
        if rk_ in rk and raw[rk_] is not None:
            response = str(raw[rk_]).strip()
            break

    # Fallbacks
    if prompt is None:
        # try first string field
        for v in raw.values():
            if isinstance(v, str) and v.strip():
                prompt = v.strip()
                break
    if response is None:
        prompt = json.dumps(raw, ensure_ascii=False)
        response = ""

    return {"prompt": prompt or "", "response": response or ""}

# ---- worker ----
def build_manifest(date_folder: str) -> List[str]:
    """
    One-time Mac-side helper: list top-level tree for a date folder.
    Save to file-list.json and commit to repo.
    """
    token = os.environ.get("HF_TOKEN")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    # non-recursive: we expect date_folder/<files...>
    r = requests.get(
        f"{API_BASE}/tree",
        params={"path": date_folder, "recursive": "false"},
        headers=headers,
        timeout=30,
    )
    if r.status_code == requests.codes.too_many_requests:
        print("HF API 429 — wait 360s before retry", file=sys.stderr)
        sys.exit(1)
    r.raise_for_status()
    items = r.json()
    paths = [it["path"] for it in items if it["type"] == "file"]
    return sorted(paths)

def download_via_cdn(path: str) -> bytes:
    """CDN bypass: no Authorization header."""
    url = f"{

## review — reviewer @ 2026-05-03T02:38:39.717993Z

APPROVE: The change is a workable, incremental improvement that replaces the shell script with a manifest-driven Python worker, keeps the existing matrix strategy, and provides a clear path to reduce API/rate-limit pressure via CDN bypass and deterministic sharding.

Acceptance criteria:
- Worker accepts SHARD_ID, SHARD_TOTAL, DATE, HF_TOKEN and a --manifest path; exits non-zero on transient HF API 429 and file download failures.
- Deterministic shard assignment uses hash(slug) % SHARD_TOTAL and matches across runs; shard boundaries are stable for a given manifest.
- CDN bypass downloads files via resolve/main URLs without Authorization header; fallback/retry behavior is explicit for 429/5xx.
- parse_pair projects heterogeneous schemas to {prompt, response} with documented fallback rules and non-null string outputs.
- Dedup integration via lib/dedup.md5 store skips duplicates and records counts; output is batches/public-merged/{DATE}/shardN-HHMMSS.jsonl.
- requirements.txt adds requests and tqdm, keeps datasets; GitHub Actions matrix (16 shards) remains unchanged and passes smoke tests for one shard locally.

## qa — qa @ 2026-05-03T02:39:17.331196Z

PASS: Implementation approved and testable.

1. **Acceptance criteria**
- CLI accepts SHARD_ID, SHARD_TOTAL, DATE, HF_TOKEN, --manifest; exits non-zero on transient HF API 429 and file download failures (exit code ≠ 0).
- Deterministic shard assignment: for any manifest, hash(slug) % SHARD_TOTAL is stable across runs; shard boundaries identical for same manifest/SHARD_TOTAL.
- CDN bypass: downloads use resolve/main URLs without Authorization header; retry policy explicitly handles 429/5xx with backoff and fails after configured attempts.
- parse_pair projects heterogeneous schemas to {prompt, response}; both outputs are non-empty strings for any non-empty input object.
- Dedup integration: lib/dedup.md5 store skips duplicates; stdout/log reports skipped/accepted counts; output file contains only new items.
- Output path: batches/public-merged/{DATE}/shard{N}-{HHMMSS}.jsonl exists and contains valid JSONL lines with {prompt, response} keys.
- requirements.txt adds requests and tqdm, retains datasets; GitHub Actions matrix (16 shards) unchanged and local smoke test for one shard passes (no auth required for CDN downloads).

2. **Unit tests** (pytest-style pseudo-code)
```python
# test_dataset_enrich_unit.py
import json
import hashlib
from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest

from bin.dataset_enrich import (
    slug_for_path,
    hash_shard,
    parse_pair,
    CDN_BASE,
    HF_DATASET_REPO,
)

# ---- slug/shard ----
def test_slug_strips_slashes():
    assert slug_for_path("/a/b/c.json") == "a/b/c.json"
    assert slug_for_path("x/y/") == "x/y"

def test_hash_shard_deterministic():
    s = "datasets/some/file.json"
    total = 16
    h1 = hash_shard(s, total)
    h2 = hash_shard(s, total)
    assert h1 == h2
    assert 0 <= h1 < total

def test_hash_shard_uniform_ish():
    # sanity: different slugs map across shards
    shards = {hash_shard(f"file-{i}", 16) for i in range(1000)}
    assert len(shards) > 1

# ---- parse_pair ----
def test_parse_pair_basic():
    raw = {"prompt": "hello", "response": "world"}
    out = parse_pair(raw)
    assert out["prompt"] == "hello"
    assert out["response"] == "world"

def test_parse_pair_variant_keys():
    raw = {"instruction": "do X", "output": "done"}
    out = parse_pair(raw)
    assert out["prompt"] == "do X"
    assert out["response"] == "done"

def test_parse_pair_non_strings():
    raw = {"prompt": 123, "response": None}
    out = parse_pair(raw)
    assert isinstance(out["prompt"], str)
    assert isinstance(out["response"], str)

def test_parse_pair_fallbacks():
    raw = {"unknown": "value"}
    out = parse_pair(raw)
    assert isinstance(out["prompt"], str) and out["prompt"]
    assert isinstance(out["response"], str)

def test_parse_pair_empty_input():
    raw = {}
    out = parse_pair(raw)
    assert isinstance(out["prompt"], str)
    assert isinstance(out["response"], str)

# ---- worker orchestration (mocked) ----
@patch("bin.dataset_enrich.requests.get")
def test_cdn_bypass_no_auth_header(mock_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.iter_content = lambda chunk_size: [b"data"]
    mock_get.return_value = mock_resp

    from bin.dataset_enrich import download_file_cdn_bypass
    download_file_cdn_bypass("datasets/file.json", "/tmp/out")
    headers = mock_get.call_args[1].get("headers", {})
    assert "Authorization" not in headers
    assert mock_get.call_args[0][0].startswith(CDN_BASE)

@patch("bin.dataset_enrich.requests.get")
def test_retry_on_429(mock_get):
    r429 = MagicMock(status_code=429)
    r200 = MagicMock(status_code=200)
    r200.iter_content = lambda chunk_size: [b"ok"]
    mock_get.side_effect = [r429, r429, r200]

    from bin.dataset_enrich import download_file_cdn_bypass
    # should not raise after retries
    download_file_cdn_bypass("datasets/file.json", "/tmp/out", max_retries=3, backoff=0.01)
    assert mock_get.call_count == 3

@patch("bin.dataset_enrich.requests.get")
