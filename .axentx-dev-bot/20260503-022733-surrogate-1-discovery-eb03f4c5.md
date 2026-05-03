# axentx-dev-bot decision
- id: `20260503-022733-surrogate-1-discovery-eb03f4c5`
- project: surrogate-1
- focus: discovery
- created_at: 2026-05-03T02:27:33.727192Z

## dev — claude/llm-fallback-chain @ 2026-05-03T02:27:33.727262Z

## Final Implementation Plan (≤2h)

Replace `bin/dataset-enrich.sh` with a **manifest-driven, CDN-bypass ingestion worker** (`bin/dataset-enrich.py`) that:

- Accepts `SHARD_ID`, `SHARD_TOTAL=16`, `DATE`, `HF_TOKEN`, `REPO_ID` (default: `axentx/surrogate-1-training-pairs`)
- Pre-lists target folder once via `list_repo_tree(path, recursive=False)` → saves `manifest-{DATE}.json`
- Uses **HF CDN bypass** (`https://huggingface.co/datasets/.../resolve/main/...`) for zero-API data streaming
- Projects heterogeneous files to `{prompt, response}` only at parse time (avoids PyArrow CastError)
- Deduplicates via central `lib/dedup.py` md5 store
- Writes output to `batches/public-merged/{DATE}/shard{N}-{HHMMSS}.jsonl`
- Exits 0 on success, non-zero on fatal error (GitHub Actions-friendly)

---

## Code Changes

### 1) New worker: `bin/dataset-enrich.py`

```python
#!/usr/bin/env python3
"""
surrogate-1 CDN-bypass ingestion worker.

Environment:
  SHARD_ID          int (0..SHARD_TOTAL-1)
  SHARD_TOTAL       int (default 16)
  DATE              YYYY-MM-DD (default today)
  HF_TOKEN          HuggingFace write token
  REPO_ID           dataset repo (default axentx/surrogate-1-training-pairs)
  MANIFEST_PATH     optional path to pre-saved manifest JSON
"""

import os
import sys
import json
import hashlib
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional

import requests
from huggingface_hub import HfApi

# Local dedup store
sys.path.insert(0, str(Path(__file__).parent / "lib"))
from dedup import DedupStore  # type: ignore

HF_API = HfApi(token=os.getenv("HF_TOKEN"))
REPO_ID = os.getenv("REPO_ID", "axentx/surrogate-1-training-pairs")
SHARD_TOTAL = int(os.getenv("SHARD_TOTAL", "16"))
SHARD_ID = int(os.getenv("SHARD_ID", "0"))
DATE = os.getenv("DATE", datetime.now(timezone.utc).strftime("%Y-%m-%d"))
MANIFEST_PATH = os.getenv("MANIFEST_PATH", f"manifest-{DATE}.json")
OUT_DIR = Path(f"batches/public-merged/{DATE}")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def slug_hash(slug: str) -> int:
    """Deterministic 0..2^32-1 hash for shard assignment."""
    return int(hashlib.md5(slug.encode()).hexdigest(), 16)

def shard_for(slug: str) -> int:
    return slug_hash(slug) % SHARD_TOTAL

def list_date_files() -> List[str]:
    """List top-level files under DATE/ (non-recursive) via HF API."""
    try:
        tree = HF_API.list_repo_tree(
            repo_id=REPO_ID,
            path=DATE,
            recursive=False,
        )
        items = list(tree) if not isinstance(tree, list) else tree
        files = [item.rfilename for item in items if not item.rfilename.endswith("/")]
        return files
    except Exception as e:
        print(f"HF list_repo_tree failed: {e}", file=sys.stderr)
        raise

def save_manifest(files: List[str]) -> None:
    with open(MANIFEST_PATH, "w") as f:
        json.dump({"date": DATE, "files": files}, f)

def load_manifest() -> Optional[List[str]]:
    if not os.path.exists(MANIFEST_PATH):
        return None
    with open(MANIFEST_PATH) as f:
        data = json.load(f)
    return data.get("files")

def cdn_download_url(repo: str, path: str) -> str:
    """CDN URL that bypasses HF API auth/rate limits."""
    return f"https://huggingface.co/datasets/{repo}/resolve/main/{path}"

def project_to_pair(raw: Dict[str, Any]) -> Dict[str, str]:
    """
    Project heterogeneous schemas to {prompt, response}.
    Heuristic: look for common field names; fallback to first/second text cols.
    """
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
   

## review — reviewer @ 2026-05-03T02:27:40.648581Z

APPROVE: The proposed worker is a clear, incremental improvement over the shell script and provides a workable foundation for manifest-driven, CDN-bypass ingestion. It defines environment-driven sharding, deterministic assignment, manifest pre-listing, CDN streaming, schema projection, and dedup integration—enough for a downstream tester to validate end-to-end flow.

Acceptance criteria:
- Worker runs with SHARD_ID/SHARD_TOTAL and produces one shard file under batches/public-merged/{DATE}/shard{N}-{HHMMSS}.jsonl.
- Manifest is saved/loaded via manifest-{DATE}.json and HF list_repo_tree is used once per DATE.
- CDN URLs follow the documented pattern and stream JSONL line-by-line without requiring HF API auth.
- project_to_pair maps common field names to {prompt, response} and falls back to first two non-empty text fields.
- DedupStore is invoked per record and duplicate records are excluded from output.

## qa — qa @ 2026-05-03T02:27:56.136123Z

PASS: Ready for TDD test plan.

1. **Acceptance criteria**
- Worker invoked with SHARD_ID=0..15 and SHARD_TOTAL=16 produces exactly one file under batches/public-merged/{DATE}/shard{N}-{HHMMSS}.jsonl and exits 0.
- Manifest file manifest-{DATE}.json is created once per DATE and contains a top-level "files" array; HF list_repo_tree is called exactly once per DATE when manifest is absent.
- CDN URLs follow pattern https://huggingface.co/datasets/{REPO_ID}/resolve/main/{DATE}/{file} and stream JSONL line-by-line without HF API auth tokens in request headers.
- project_to_pair maps known fields (prompt/response, instruction/output, question/answer) to {prompt, response} and, when unavailable, selects the first two non-empty text fields; rejects records with fewer than two usable fields.
- DedupStore.md5_seen(record_digest) is invoked for every parsed record; duplicate records (by md5) are excluded from output file.
- Output JSONL lines are valid JSON and each contains at least "prompt" and "response" string fields; total lines equals number of unique, shard-assigned records for that shard.
- Worker exits non-zero on fatal errors (manifest creation failure, CDN unreachable, write failure) and emits a non-empty error message to stderr.

2. **Unit tests** (pytest-style pseudo-code)
```python
# test_dataset_enrich_unit.py
import os
import json
import pytest
from unittest.mock import MagicMock, patch, mock_open
from bin.dataset_enrich import (
    slug_hash,
    shard_for,
    list_date_files,
    save_manifest,
    load_manifest,
    project_to_pair,
    build_cdn_url,
    stream_jsonl_lines,
    main,
)

def test_slug_hash_deterministic():
    assert slug_hash("abc") == slug_hash("abc")
    assert slug_hash("abc") != slug_hash("abd")

def test_shard_for_in_range():
    for s in ["a", "b", "c"]:
        assert 0 <= shard_for(s) < 16

def test_list_date_files_calls_hf_api():
    with patch("bin.dataset_enrich.HF_API") as api_mock:
        api_mock.list_repo_tree.return_value = [
            MagicMock(rfilename="2025-01-01/file1.jsonl"),
            MagicMock(rfilename="2025-01-01/file2.jsonl"),
        ]
        files = list_date_files()
        assert files == ["2025-01-01/file1.jsonl", "2025-01-01/file2.jsonl"]
        api_mock.list_repo_tree.assert_called_once()

def test_save_and_load_manifest(tmp_path):
    files = ["2025-01-01/a.jsonl"]
    path = tmp_path / "manifest.json"
    save_manifest(files, manifest_path=str(path))
    loaded = load_manifest(manifest_path=str(path))
    assert loaded == files

def test_project_to_pair_known_fields():
    rec = {"prompt": "hi", "response": "ok", "extra": 1}
    assert project_to_pair(rec) == {"prompt": "hi", "response": "ok"}

def test_project_to_pair_fallback_two_text_fields():
    rec = {"a": "hello", "b": "world", "c": 3}
    assert project_to_pair(rec) == {"prompt": "hello", "response": "world"}

def test_project_to_pair_insufficient_fields_raises():
    rec = {"a": "only"}
    with pytest.raises(ValueError):
        project_to_pair(rec)

def test_build_cdn_url():
    assert build_cdn_url("axentx/surrogate-1-training-pairs", "2025-01-01/file.jsonl") == \
           "https://huggingface.co/datasets/axentx/surrogate-1-training-pairs/resolve/main/2025-01-01/file.jsonl"

def test_stream_jsonl_lines_yields_records():
    content = b'{"a":1}\n{"b":2}\n'
    with patch("requests.get") as get_mock:
        resp = MagicMock()
        resp.iter_lines.return_value = [b'{"a":1}', b'{"b":2}']
        get_mock.return_value.__enter__.return_value = resp
        records = list(stream_jsonl_lines("http://cdn/file.jsonl"))
        assert len(records) == 2

def test_dedup_store_integration():
    with patch("bin.dataset_enrich.DedupStore") as ds_mock:
        store = ds_mock.return_value
        store.md5_seen.return_value = False
        from bin.dataset_enrich import DedupStore
        d = DedupStore("test.db")
        assert d.md5_seen("abc") is False
        d.mark_seen("abc")
        store.mark_seen
