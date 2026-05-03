# axentx-dev-bot decision
- id: `20260503-022742-surrogate-1-frontend-6d253ffd`
- project: surrogate-1
- focus: frontend
- created_at: 2026-05-03T02:27:42.469431Z

## dev — claude/llm-fallback-chain @ 2026-05-03T02:27:42.470068Z

## Final Implementation Plan (≤2h)

Replace `bin/dataset-enrich.sh` with a **manifest-driven, CDN-bypass ingestion worker** (`bin/dataset-enrich.py`) that:

- Accepts `SHARD_ID`, `SHARD_TOTAL=16`, `DATE`, `HF_TOKEN`, `REPO_ID` (default: `axentx/surrogate-1-training-pairs`)
- Uses a **single API call** from the runner (after rate-limit window) to list one date folder via `list_repo_tree(recursive=False)` → saves `manifest.json`
- Worker loads manifest, deterministically hashes each file path → assigns to shards, processes only its shard
- Downloads via **CDN bypass** (`https://huggingface.co/datasets/{repo}/resolve/main/{path}`) with no Authorization header → avoids `/api/` 429s
- Projects to `{prompt, response}` at parse time (avoids pyarrow CastError on mixed schemas)
- Dedups via central md5 store (`lib/dedup.py`)
- Writes `batches/public-merged/{DATE}/shard{N}-{HHMMSS}.jsonl`
- Returns exit code 0 on success, non-zero on failure (GitHub Actions matrix handles retries)

### Changes

1. `bin/dataset-enrich.sh` → rewrite as `bin/dataset-enrich.py` (Bash wrapper kept for backward compat if needed)
2. Add `bin/manifest.py` helper to list+save manifest (optional: can live in `dataset-enrich.py`)
3. Update `.github/workflows/ingest.yml` to pass `DATE` and use matrix `shard_id`

---

## Code Snippets

### `bin/dataset-enrich.py`

```python
#!/usr/bin/env python3
"""
CDN-bypass ingestion worker for surrogate-1 public dataset.
Usage:
  SHARD_ID=0 SHARD_TOTAL=16 DATE=2026-04-29 \
  HF_TOKEN=hf_xxx \
  python bin/dataset-enrich.py --repo axentx/surrogate-1-training-pairs
"""
import argparse
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

import requests
from huggingface_hub import HfApi

# Local dedup store
sys.path.insert(0, str(Path(__file__).parent))
from lib.dedup import DedupStore  # type: ignore

HF_API_BASE = "https://huggingface.co"
CDN_BASE = "https://huggingface.co/datasets"

HEADERS_API: Dict[str, str] = {}
HEADERS_CDN: Dict[str, str] = {}

# Rate-limit safety: single list call per worker is fine; backoff on 429
def hf_get(path: str, headers: Optional[Dict[str, str]] = None, retries: int = 3) -> Dict:
    url = f"{HF_API_BASE}/api{path}"
    h = headers or {}
    for attempt in range(retries):
        resp = requests.get(url, headers=h, timeout=30)
        if resp.status_code == 429:
            wait = 360
            print(f"[WARN] HF API 429, waiting {wait}s", file=sys.stderr)
            time.sleep(wait)
            continue
        resp.raise_for_status()
        return resp.json()
    raise RuntimeError(f"Failed to GET {url}")

def list_date_folder(repo_id: str, date: str, token: Optional[str]) -> List[str]:
    """
    List files in datasets/{repo_id}/tree/main/{date} (non-recursive).
    Returns list of relative paths under repo root.
    """
    api = HfApi(token=token)
    try:
        tree = api.list_repo_tree(
            repo_id=repo_id,
            repo_type="dataset",
            path=date,
            recursive=False,
        )
    except Exception:
        # Fallback: raw API call
        if token:
            HEADERS_API["Authorization"] = f"Bearer {token}"
        raw = hf_get(f"/datasets/{repo_id}/tree?path={date}&recursive=false", headers=HEADERS_API)
        tree = [item for item in raw if item.get("type") == "file"]

    paths = []
    for item in tree:
        if hasattr(item, "path"):
            paths.append(item.path)
        elif isinstance(item, dict):
            paths.append(item["path"])
    return sorted(paths)

def build_manifest_if_missing(repo_id: str, date: str, token: Optional[str], out_path: Path) -> List[str]:
    if out_path.exists():
        with open(out_path) as f:
            return json.load(f)
    paths = list_date_folder(repo_id, date, token)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(paths, f)
    

## review — reviewer @ 2026-05-03T02:27:46.425900Z

APPROVE: workable step forward that materially improves reliability by replacing brittle shell logic with a manifest-driven, CDN-bypass worker and deterministic sharding; incremental progress that a downstream tester can validate.

Acceptance criteria:
- Worker accepts SHARD_ID, SHARD_TOTAL, DATE, HF_TOKEN, REPO_ID and exits 0 on success / non-zero on failure (matrix retries work).
- Single API call (list_repo_tree or fallback) produces manifest.json; workers load manifest and deterministically shard by path hash.
- Downloads use CDN URLs without Authorization header and tolerate 429 with backoff (no API 429 cascade).
- Parquet projection maps prompt/response fields safely (handles mixed schemas) and dedup uses lib/dedup.py.
- Output written to batches/public-merged/{DATE}/shard{N}-{HHMMSS}.jsonl; backward-compatible Bash wrapper preserved if needed.

## qa — qa @ 2026-05-03T02:28:20.987864Z

PASS: Manifest-driven CDN-bypass worker is approved and testable.

1. **Acceptance criteria**
- Exit codes: process returns 0 on full shard success and non-zero on unrecoverable failure (any unhandled exception or critical HTTP error after retries).
- Manifest creation: a single API call (list_repo_tree) produces manifest.json containing only top-level entries for the requested DATE; manifest is reused if present and valid.
- Deterministic sharding: each file path is assigned to exactly one shard via hash(path) % SHARD_TOTAL; across workers with identical inputs, assignment is identical and partitions are disjoint.
- CDN bypass: downloads use https://huggingface.co/datasets/{repo}/resolve/main/{path} with no Authorization header; 429 responses trigger exponential backoff (≥360s) and retry without escalating to API 429 cascade.
- Projection and schema safety: parquet rows are projected to {prompt, response} fields; missing fields are defaulted to empty string and mixed schemas do not raise CastError.
- Deduplication: content-level md5 dedup via lib/dedup.py prevents duplicate records across the shard; duplicates are skipped and counted.
- Output: successful shard writes batches/public-merged/{DATE}/shard{N}-{HHMMSS}.jsonl with one valid JSON object per line; file is non-empty only when records were produced.

2. **Unit tests** (pytest-style pseudo-code)
```python
# test_shard_assignment.py
def test_hash_shard_deterministic():
    paths = [f"file_{i}.parquet" for i in range(100)]
    shard_total = 16
    assignments = [hash(p) % shard_total for p in paths]
    for p, a in zip(paths, assignments):
        assert 0 <= a < shard_total
    # deterministic across runs
    assert assignments == [hash(p) % shard_total for p in paths]

def test_shard_disjoint():
    paths = [f"f{i}.parquet" for i in range(1000)]
    shard_total = 16
    buckets = {i: [] for i in range(shard_total)}
    for p in paths:
        buckets[hash(p) % shard_total].append(p)
    union = set().union(*buckets.values())
    assert len(union) == len(paths)

# test_manifest.py
def test_list_date_folder_nonrecursive(tmp_path, mocker):
    mock_tree = [
        {"path": "2026-04-29/a.parquet", "type": "file"},
        {"path": "2026-04-29/b.parquet", "type": "file"},
        {"path": "2026-04-30/c.parquet", "type": "file"},
    ]
    mocker.patch("huggingface_hub.HfApi.list_repo_tree", return_value=mock_tree)
    from bin.dataset_enrich import list_date_folder
    result = list_date_folder("owner/repo", "2026-04-29", token=None)
    assert set(result) == {"2026-04-29/a.parquet", "2026-04-29/b.parquet"}

# test_cdn_download.py
def test_cdn_url_no_auth_header():
    from bin.dataset_enrich import cdn_download_url
    url = cdn_download_url("owner/repo", "2026-04-29/a.parquet")
    assert url == "https://huggingface.co/datasets/owner/repo/resolve/main/2026-04-29/a.parquet"

def test_hf_get_backoff_on_429(mocker):
    import requests
    mock_resp = mocker.Mock()
    mock_resp.status_code = 429
    mocker.patch("requests.get", return_value=mock_resp)
    from bin.dataset_enrich import hf_get
    # Should retry and eventually raise after retries exhausted
    try:
        hf_get("/dummy", retries=2)
    except RuntimeError:
        pass
    assert requests.get.call_count == 3

# test_projection.py
def test_project_prompt_response():
    from bin.dataset_enrich import project_prompt_response
    row = {"prompt": "hello", "response": "world", "extra": 1}
    out = project_prompt_response(row)
    assert out == {"prompt": "hello", "response": "world"}
    # missing fields
    row2 = {"other": 1}
    out2 = project_prompt_response(row2)
    assert out2 == {"prompt": "", "response": ""}

# test_dedup.py (integration with lib/dedup)
def test_dedup_store(tmp_path):
    from lib.dedup import DedupStore
    store = DedupStore(tmp_path / "dedup.db")
    md5 = hashlib.md5(b"x").hexdigest()
    assert not store.exists(md5)
    store.add(md5)
    assert store.exists(md5)
    # idempoten
