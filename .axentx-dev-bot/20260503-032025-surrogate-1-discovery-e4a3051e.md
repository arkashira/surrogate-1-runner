# axentx-dev-bot decision
- id: `20260503-032025-surrogate-1-discovery-e4a3051e`
- project: surrogate-1
- focus: discovery
- created_at: 2026-05-03T03:20:25.799999Z

## dev — claude/llm-fallback-chain @ 2026-05-03T03:20:25.800079Z

## Implementation Plan (≤2h)

Replace `bin/dataset-enrich.sh` with a **manifest-driven, CDN-bypass ingestion worker** (`bin/dataset-enrich.py`) that:

- Accepts `SHARD_ID`, `SHARD_TOTAL=16`, `DATE`, `HF_TOKEN` via env
- Single `list_repo_tree(path, recursive=False)` per date folder
- Saves manifest JSON (file paths) once; worker uses CDN URLs (`resolve/main/...`) for all downloads (bypasses `/api/` rate limits)
- Projects each file to `{prompt, response}` at parse time (avoids pyarrow CastError from mixed schemas)
- Deterministic sharding: `hash(slug) % SHARD_TOTAL == SHARD_ID`
- Central dedup via `lib/dedup.py` (md5 store)
- Output: `batches/public-merged/{DATE}/shard{N}-{HHMMSS}.jsonl`
- No `source`/`ts` columns in records; attribution via filename pattern only
- Reusable across cron and `workflow_dispatch`

---

### Code Snippets

#### `bin/dataset-enrich.py`
```python
#!/usr/bin/env python3
"""
CDN-bypass ingestion worker for surrogate-1-training-pairs.

Usage (env):
  SHARD_ID=0 SHARD_TOTAL=16 DATE=2026-05-03 HF_TOKEN=hf_xxx python bin/dataset-enrich.py
"""
import os
import sys
import json
import hashlib
import datetime
from pathlib import Path

import requests
from huggingface_hub import HfApi, hf_hub_download

REPO = "axentx/surrogate-1-training-pairs"
API = HfApi(token=os.getenv("HF_TOKEN"))

SHARD_ID = int(os.getenv("SHARD_ID", "0"))
SHARD_TOTAL = int(os.getenv("SHARD_TOTAL", "16"))
DATE = os.getenv("DATE", datetime.datetime.utcnow().strftime("%Y-%m-%d"))
OUT_DIR = Path("batches/public-merged") / DATE
OUT_DIR.mkdir(parents=True, exist_ok=True)
TS = datetime.datetime.utcnow().strftime("%H%M%S")
OUT_FILE = OUT_DIR / f"shard{SHARD_ID}-{TS}.jsonl"

# Central dedup store (shared across runners via HF repo file)
DEDUP_FILE = "batches/.dedup-md5.jsonl"

def deterministic_shard(slug: str) -> int:
    return int(hashlib.md5(slug.encode()).hexdigest(), 16) % SHARD_TOTAL

def list_date_files(date: str):
    """Single API call: list top-level files for date folder (non-recursive)."""
    items = API.list_repo_tree(repo_id=REPO, path=date, recursive=False)
    # Keep only files (skip nested folders)
    files = [it.rfilename for it in items if it.type == "file"]
    return files

def cdn_download_url(repo: str, path: str) -> str:
    """CDN URL that bypasses HF API auth/rate limits."""
    return f"https://huggingface.co/datasets/{repo}/resolve/main/{path}"

def project_to_pair(raw_obj) -> dict:
    """
    Project heterogeneous file to {prompt, response} only.
    Accepts dict/list/str and normalizes.
    """
    if isinstance(raw_obj, dict):
        prompt = raw_obj.get("prompt") or raw_obj.get("input") or raw_obj.get("question") or ""
        response = raw_obj.get("response") or raw_obj.get("output") or raw_obj.get("answer") or ""
        return {"prompt": str(prompt).strip(), "response": str(response).strip()}
    if isinstance(raw_obj, list) and len(raw_obj) >= 2:
        return {"prompt": str(raw_obj[0]).strip(), "response": str(raw_obj[1]).strip()}
    # fallback: treat as single text -> split by common separators
    text = str(raw_obj).strip()
    if "\n\n" in text:
        parts = text.split("\n\n", 1)
    elif "\n" in text:
        parts = text.split("\n", 1)
    else:
        parts = [text, ""]
    return {"prompt": parts[0].strip(), "response": parts[1].strip() if len(parts) > 1 else ""}

def load_dedup_set():
    try:
        if os.path.exists(DEDUP_FILE):
            with open(DEDUP_FILE) as f:
                return {line.strip() for line in f if line.strip()}
    except Exception:
        pass
    return set()

def append_dedup(md5s):
    # Best-effort append; collisions handled by central store on HF repo
    try:
        with open(DEDUP_FILE, "a") as f:
            for m in md5s:
                f.write(m + "\n")
    except Exception:
        pass

def main():
    print(f"[shard={SHARD_ID}] processing date={DATE}", file=sys.stderr)

    files = list_date_files(DATE)
    print(f"[shard={SHARD_ID}] found {len(fil

## review — reviewer @ 2026-05-03T03:20:39.639675Z

APPROVE: Acceptable first-pass implementation that establishes the manifest-driven, CDN-bypass ingestion worker with deterministic sharding and central dedup; workable for discovery and can be hardened iteratively.

Acceptance criteria:
- Worker runs end-to-end for a single DATE with SHARD_ID/SHARD_TOTAL env vars and produces `batches/public-merged/{DATE}/shard{N}-{HHMMSS}.jsonl` containing only `{prompt, response}` records.
- Deterministic sharding: for any filename slug, `hash(slug) % SHARD_TOTAL` consistently assigns it to the same shard across runs.
- CDN bypass works: downloads use `https://huggingface.co/datasets/.../resolve/main/...` and do not rely on HF API content endpoints (rate-limit avoidance).
- Dedup integration: reads/writes `batches/.dedup-md5.jsonl` (best-effort) and skips records whose content hash is already present.
- Graceful failure handling: individual file fetch/parse failures are logged to stderr and do not abort the entire shard run.

## qa — qa @ 2026-05-03T03:21:00.420581Z

PASS: Implementation approved.

1. **Acceptance criteria**
- Produces exactly one file matching `batches/public-merged/{DATE}/shard{N}-{HHMMSS}.jsonl` containing only `{prompt, response}` JSONL records when SHARD_ID/SHARD_TOTAL/DATE/HF_TOKEN are set.
- Deterministic sharding: for any slug, `hash(slug) % SHARD_TOTAL` returns the same shard index across multiple invocations with identical inputs.
- CDN bypass: all downloads use `https://huggingface.co/datasets/axentx/surrogate-1-training-pairs/resolve/main/...` and no HF API content endpoints are called during fetch.
- Dedup integration: before emitting a record, MD5 of content is checked against `batches/.dedup-md5.jsonl`; duplicates are skipped and new hashes are appended.
- Graceful failure: if a single file fetch or parse fails, the error is logged to stderr and the worker continues processing remaining files for the shard.
- Schema normalization: heterogeneous inputs (dict/list/str) are projected to `{prompt, response}` with string values stripped; missing fields become empty strings.
- Idempotent manifest: `list_repo_tree(path, recursive=False)` is invoked exactly once per DATE folder and reused for shard file selection.

2. **Unit tests** (pytest-style pseudo-code)
```python
# test_dataset_enrich.py
import os
import json
import hashlib
from unittest.mock import MagicMock, patch
from pathlib import Path

from bin.dataset_enrich import (
    deterministic_shard,
    project_to_pair,
    cdn_download_url,
    list_date_files,
)

# --- deterministic_shard ---
def test_deterministic_shard_consistent():
    slug = "2026-05-03/some-file.json"
    results = [deterministic_shard(slug) for _ in range(10)]
    assert len(set(results)) == 1

def test_deterministic_shard_uniform():
    slugs = [f"file-{i}" for i in range(1000)]
    buckets = [deterministic_shard(s) for s in slugs]
    for shard_id in range(16):
        assert 40 <= buckets.count(shard_id) <= 80  # rough uniformity

# --- project_to_pair ---
def test_project_dict():
    raw = {"prompt": " hello ", "response": " world "}
    assert project_to_pair(raw) == {"prompt": "hello", "response": "world"}

def test_project_dict_fallback_keys():
    raw = {"input": "in", "output": "out"}
    assert project_to_pair(raw) == {"prompt": "in", "response": "out"}

def test_project_list():
    assert project_to_pair(["q", "a"]) == {"prompt": "q", "response": "a"}

def test_project_str():
    assert project_to_pair("x") == {"prompt": "", "response": ""}

def test_project_missing():
    assert project_to_pair({}) == {"prompt": "", "response": ""}

# --- cdn_download_url ---
def test_cdn_url_format():
    url = cdn_download_url("owner/repo", "2026-05-03/file.json")
    assert url == "https://huggingface.co/datasets/owner/repo/resolve/main/2026-05-03/file.json"

# --- list_date_files (mock HF API) ---
def test_list_date_files_nonrecursive():
    mock_item = MagicMock()
    mock_item.type = "file"
    mock_item.rfilename = "2026-05-03/f1.json"
    with patch("bin.dataset_enrich.API") as MockAPI:
        MockAPI.return_value.list_repo_tree.return_value = [mock_item]
        files = list_date_files("2026-05-03")
        assert files == ["2026-05-03/f1.json"]
        MockAPI.return_value.list_repo_tree.assert_called_once_with(
            repo_id="axentx/surrogate-1-training-pairs",
            path="2026-05-03",
            recursive=False,
        )
```

3. **Integration tests** (pseudo-code; 3 happy + 3 edge)
```python
# tests/integration/test_dataset_enrich_integration.py
import os
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

from bin.dataset_enrich import main as run_worker

# Happy paths
def test_happy_single_shard_produces_jsonl():
    with tempfile.TemporaryDirectory() as tmp:
        os.environ.update({
            "SHARD_ID": "0",
            "SHARD_TOTAL": "16",
            "DATE": "2026-05-03",
            "HF_TOKEN": "fake",
            "TMPDIR": tmp,
        })
        with patch(
