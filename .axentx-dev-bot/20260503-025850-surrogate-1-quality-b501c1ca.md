# axentx-dev-bot decision
- id: `20260503-025850-surrogate-1-quality-b501c1ca`
- project: surrogate-1
- focus: quality
- created_at: 2026-05-03T02:58:50.348746Z

## dev — claude/llm-fallback-chain @ 2026-05-03T02:58:50.348818Z

## Final Implementation Plan (≤2h)

Replace `bin/dataset-enrich.sh` with a **manifest-driven, CDN-bypass ingestion worker** (`bin/dataset-enrich.py`) that:

- Accepts `SHARD_ID`, `SHARD_TOTAL=16`, `DATE`, `HF_TOKEN`
- Single `list_repo_tree(path=DATE, recursive=False)` → deterministic file list
- Deterministic shard assignment: `hash(slug) % SHARD_TOTAL == SHARD_ID`
- Downloads only assigned files via **HF CDN bypass** (`resolve/main/...`, no Authorization header)
- Projects each file to `{prompt, response}` at parse time (no schema assumptions)
- Deduplicates via central `lib/dedup.py` md5 store
- Writes `batches/public-merged/{DATE}/shard{N}-{HHMMSS}.jsonl`
- Exits 0 on success; logs counts + skipped dupes

### Why this is the highest-value incremental improvement
- Fixes the **HF API 429/rate-limit** and **pyarrow CastError** patterns from the playbook
- Eliminates `load_dataset(streaming=True)` on heterogeneous repos
- Cuts API calls during training (manifest is pre-computed)
- Keeps ingestion parallel, deterministic, and OOM-safe
- Reuses existing dedup store and output convention

---

## Code Changes

### 1) New worker: `bin/dataset-enrich.py`

```python
#!/usr/bin/env python3
"""
surrogate-1 CDN-bypass ingestion worker.

Usage (GH Actions matrix):
  SHARD_ID=0 SHARD_TOTAL=16 DATE=2026-05-03 \
  HF_TOKEN=hf_xxx \
  python bin/dataset-enrich.py

Environment:
  SHARD_ID          - worker index [0..SHARD_TOTAL-1]
  SHARD_TOTAL       - total parallel workers (default 16)
  DATE              - folder in axentx/surrogate-1-training-pairs to ingest
  HF_TOKEN          - HF write token (for dedup store + upload)
  DRY_RUN           - if set, skip upload
"""
import os
import sys
import json
import hashlib
import datetime
import logging
from pathlib import Path
from typing import Dict, Any, List

import requests
import pyarrow.parquet as pq
from huggingface_hub import HfApi

# Project-local dedup store
sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.dedup import DedupStore  # type: ignore

REPO_ID = "axentx/surrogate-1-training-pairs"
CHUNK_SIZE = 8 * 1024 * 1024  # 8 MB

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S%z",
)
log = logging.getLogger("dataset-enrich")

def shard_of(slug: str, total: int) -> int:
    return int(hashlib.md5(slug.encode()).hexdigest(), 16) % total

def list_date_files(date: str) -> List[str]:
    """Single API call: list top-level files in DATE/ folder."""
    api = HfApi(token=os.getenv("HF_TOKEN"))
    items = api.list_repo_tree(repo_id=REPO_ID, path=date, recursive=False)
    files = [it.rfilename for it in items if it.type == "file"]
    log.info("listed %d files in %s/", len(files), date)
    return files

def cdn_download(repo_id: str, path_in_repo: str, out_path: str) -> None:
    """Download via HF CDN (no Authorization header)."""
    url = f"https://huggingface.co/datasets/{repo_id}/resolve/main/{path_in_repo}"
    with requests.get(url, stream=True, timeout=60) as r:
        r.raise_for_status()
        with open(out_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=CHUNK_SIZE):
                f.write(chunk)

def project_to_pair(obj: Dict[str, Any]) -> Dict[str, str]:
    """
    Best-effort projection to {prompt, response}.
    Supports common field names seen in surrogate-1 sources.
    """
    prompt_keys = {"prompt", "instruction", "input", "question", "user"}
    response_keys = {"response", "completion", "output", "answer", "assistant"}

    prompt = None
    response = None

    for k, v in obj.items():
        nk = k.strip().lower()
        if nk in prompt_keys and prompt is None:
            prompt = str(v) if v is not None else ""
        elif nk in response_keys and response is None:
            response = str(v) if v is not None else ""

    # Fallback: if only one text column exists, treat as prompt and empty response
    text_cols = [k for k, v in obj.items() if i

## review — reviewer @ 2026-05-03T02:58:59.634027Z

APPROVE: workable incremental step that addresses HF rate-limits and deterministic sharding; code is mostly complete and the intent is clear, with a few small gaps that can be tightened during implementation.

Acceptance criteria (for downstream tester / implementer):
- Worker accepts SHARD_ID, SHARD_TOTAL, DATE, HF_TOKEN and deterministically assigns files via `hash(slug) % SHARD_TOTAL == SHARD_ID`.
- Single `list_repo_tree(path=DATE, recursive=False)` is used to enumerate files; only assigned files are processed.
- Files are downloaded via HF CDN (`https://huggingface.co/datasets/.../resolve/main/...`) without Authorization header; failures are logged and non-fatal.
- Each row is projected to `{prompt, response}` using best-effort field mapping and fallback rules; malformed rows are logged and skipped.
- Deduplication uses `lib/dedup.py` md5 store; duplicates are counted and skipped; unique rows are appended to `batches/public-merged/{DATE}/shard{N}-{HHMMSS}.jsonl`.
- Worker exits 0 on overall success (non-zero only on fatal config/IO errors); logs include counts processed, accepted, skipped, and dupes.

## qa — qa @ 2026-05-03T02:59:14.679232Z

PASS: criteria clear and implementable

1. **Acceptance criteria**
- Deterministic shard assignment: for any slug and total=16, `hash(slug) % 16` must equal the assigned shard across runs.
- Single tree enumeration: exactly one `list_repo_tree(path=DATE, recursive=False)` call per run; only files under DATE/ are considered.
- CDN-only downloads: every file fetch uses `https://huggingface.co/datasets/.../resolve/main/...` with no Authorization header; HTTP 200/404/429 are handled gracefully and logged.
- Row projection: each row emitted contains exactly `{prompt, response}`; malformed rows are logged and skipped (counted).
- Deduplication: md5-based dedup via `lib/dedup.py`; duplicate rows are counted and skipped; unique rows are appended to `batches/public-merged/{DATE}/shard{N}-{HHMMSS}.jsonl`.
- Exit semantics: exit code 0 on overall success; non-zero only on fatal config/IO errors (e.g., missing DATE, invalid SHARD_ID).
- Logging: final log line includes counts processed, accepted, skipped (malformed), and dupes.

2. **Unit tests** (pytest-style pseudo-code)
```python
# test_shard_of.py
def test_shard_of_deterministic():
    assert shard_of("repo/file1.parquet", 16) == shard_of("repo/file1.parquet", 16)

def test_shard_of_uniform():
    # sanity: different slugs map across shards (not strict uniformity)
    shards = {shard_of(f"repo/file{i}.parquet", 16) for i in range(100)}
    assert len(shards) > 1

# test_list_date_files.py
def test_list_date_files_calls_once(mock_hf_api):
    list_date_files("2026-05-03")
    assert mock_hf_api.list_repo_tree.call_count == 1
    mock_hf_api.list_repo_tree.assert_called_with(repo_id=REPO_ID, path="2026-05-03", recursive=False)

# test_cdn_download.py
def test_cdn_download_no_auth_header(mock_requests):
    cdn_download("owner/repo", "2026-05-03/file.parquet", "/tmp/out")
    req = mock_requests.get.call_args
    assert "Authorization" not in req.kwargs.get("headers", {})
    assert req.kwargs["url"].startswith("https://huggingface.co/datasets/owner/repo/resolve/main/")

# test_project_row.py
def test_project_row_prompt_response():
    row = {"prompt": "hi", "response": "bye", "extra": 1}
    assert project_row(row) == {"prompt": "hi", "response": "bye"}

def test_project_row_fallback():
    row = {"instruction": "hi", "completion": "bye"}
    assert project_row(row) == {"prompt": "hi", "response": "bye"}

def test_project_row_malformed_skipped():
    row = {"foo": "bar"}
    assert project_row(row) is None

# test_dedup_integration.py
def test_dedup_store_md5(tmp_path):
    store = DedupStore(tmp_path / "dedup.db")
    key = store.key_for(b"hello")
    assert store.seen(key) is False
    store.mark_seen(key)
    assert store.seen(key) is True

# test_main_exit_codes.py
def test_exit_0_on_success(monkeypatch, tmp_path):
    monkeypatch.setenv("SHARD_ID", "0")
    monkeypatch.setenv("SHARD_TOTAL", "16")
    monkeypatch.setenv("DATE", "2026-05-03")
    monkeypatch.setenv("HF_TOKEN", "fake")
    # mock happy path
    with patch_all_happy(tmp_path):
        result = run_main()
    assert result.exit_code == 0

def test_exit_nonzero_on_fatal_config():
    monkeypatch.delenv("DATE", raising=False)
    result = run_main()
    assert result.exit_code != 0
```

3. **Integration tests** (3 happy + 3 edge)

Happy cases
- Happy 1 — deterministic shard isolation: populate DATE/ with 32 files; run 16 workers (SHARD_TOTAL=16) in parallel; verify each file appears in exactly one shard output and total accepted equals unique rows across all shards.
- Happy 2 — end-to-end CDN bypass and projection: single worker processes one valid parquet file; verify download URL pattern (no Authorization), row projection to `{prompt, response}`, and output file exists with correct JSONL lines.
- Happy 3 — dedup across runs: run worker twice with same inputs; second run reports dupes > 0 and accepted = 0; output file unchanged.

Edge cases
- Edge 1 — CDN 429/retry: simulate 429 then 200 on CDN download; verify worker lo
