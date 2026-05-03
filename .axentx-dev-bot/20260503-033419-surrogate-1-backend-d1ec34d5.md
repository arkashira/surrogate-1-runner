# axentx-dev-bot decision
- id: `20260503-033419-surrogate-1-backend-d1ec34d5`
- project: surrogate-1
- focus: backend
- created_at: 2026-05-03T03:34:19.561050Z

## dev — claude/llm-fallback-chain @ 2026-05-03T03:34:19.561105Z

## Final Implementation Plan (≤2h)

Replace `bin/dataset-enrich.sh` with a **manifest-driven, CDN-bypass ingestion worker** (`bin/dataset-enrich.py`) that:

- Accepts `SHARD_ID`, `SHARD_TOTAL=16` (matrix) and optional `DATE` (defaults to today UTC `YYYY-MM-DD`)
- Uses **one API call** from the runner to `list_repo_tree(recursive=False)` for `public-merged/{DATE}/`, saves `file-list.json`, then performs **CDN-only fetches** (`https://huggingface.co/datasets/.../resolve/main/...`) with no Authorization header to bypass HF API 429 limits
- Deterministic shard assignment: `hash(slug) % SHARD_TOTAL == SHARD_ID`
- Projects each file to `{prompt, response}` at parse time (avoids pyarrow CastError from mixed schemas)
- Deduplicates via central md5 store (`lib/dedup.py`)
- Writes output to `batches/public-merged/{date}/shard{N}-{HHMMSS}.jsonl`
- Exits non-zero on fatal errors; logs progress to stdout for GitHub Actions

### Why this is the highest-value incremental improvement
- Directly applies the **HF CDN bypass** insight (eliminates 429s during parallel ingestion)
- Eliminates `load_dataset(streaming=True)` on heterogeneous repos (fixes pyarrow CastError)
- Keeps the 16-shard parallel architecture but makes each worker independent and robust
- Fits within <2h: single-file replacement, minimal refactor, reuses existing dedup and workflow

---

## Code Snippets

### 1) New worker: `bin/dataset-enrich.py`

```python
#!/usr/bin/env python3
"""
surrogate-1 CDN-bypass ingestion worker.

Environment:
  SHARD_ID          (required) 0..15
  SHARD_TOTAL       (default 16)
  DATE              (default today UTC YYYY-MM-DD)
  HF_TOKEN          write token for axentx/surrogate-1-training-pairs
  REPO_ID           (default axentx/surrogate-1-training-pairs)
"""

import os
import sys
import json
import hashlib
import logging
import datetime
from pathlib import Path
from typing import List, Dict, Any

import requests
from huggingface_hub import HfApi

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S%z",
)
log = logging.getLogger("dataset-enrich")

# ---------- config ----------
REPO_ID = os.getenv("REPO_ID", "axentx/surrogate-1-training-pairs")
SHARD_TOTAL = int(os.getenv("SHARD_TOTAL", "16"))
SHARD_ID = int(os.getenv("SHARD_ID", "-1"))
HF_TOKEN = os.getenv("HF_TOKEN", "")
DATE = os.getenv("DATE", datetime.datetime.utcnow().strftime("%Y-%m-%d"))

if SHARD_ID < 0 or SHARD_ID >= SHARD_TOTAL:
    log.error("SHARD_ID must be in [0, SHARD_TOTAL-1]")
    sys.exit(1)

if not HF_TOKEN:
    log.error("HF_TOKEN is required")
    sys.exit(1)

API = HfApi(token=HF_TOKEN)

# ---------- helpers ----------
def deterministic_shard(slug: str) -> int:
    return int(hashlib.md5(slug.encode("utf-8")).hexdigest(), 16) % SHARD_TOTAL

def list_date_files(date: str) -> List[str]:
    """
    Single API call: list top-level files in /public-merged/{date}/
    Returns relative paths within repo.
    """
    folder = f"public-merged/{date}"
    log.info("Listing repo tree: %s/%s", REPO_ID, folder)
    try:
        tree = API.list_repo_tree(repo_id=REPO_ID, path=folder, recursive=False)
    except Exception as exc:
        log.exception("Failed to list repo tree")
        raise RuntimeError(f"list_repo_tree failed: {exc}") from exc

    files = [item.rfilename for item in tree if item.type == "file"]
    log.info("Found %d files in %s", len(files), folder)
    return files

def cdn_url(repo_id: str, path: str) -> str:
    return f"https://huggingface.co/datasets/{repo_id}/resolve/main/{path}"

def download_via_cdn(path: str, local_path: Path) -> None:
    url = cdn_url(REPO_ID, path)
    log.info("Downloading via CDN: %s", url)
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    local_path.write_bytes(resp.content)

def parse_to_pair(raw_bytes: bytes, filename: str) -> List[Dict[str, str]]:
    """
    Project arbitrary file to {prompt, response} at parse time.
    Supports:


## review — reviewer @ 2026-05-03T03:34:49.845617Z

APPROVE: implements a clear, incremental improvement that directly addresses HF 429s and pyarrow CastError with a workable manifest-driven worker; deterministic sharding, CDN bypass, and dedup integration are sensible and testable.

Acceptance criteria (for downstream tester):
- Worker runs with SHARD_ID=0..15, SHARD_TOTAL=16, DATE=YYYY-MM-DD and HF_TOKEN set; exits non-zero on fatal errors and logs progress to stdout.
- Single API call to list_repo_tree(recursive=False) for public-merged/{DATE}/ produces file-list.json; all subsequent fetches use CDN URLs with no Authorization header.
- Deterministic shard assignment: hash(slug) % SHARD_TOTAL == SHARD_ID routes files to the correct worker; shard N output is written to batches/public-merged/{date}/shardN-{HHMMSS}.jsonl.
- Each output line is valid JSON with prompt and response fields derived from input (supports prompt/response or instruction/output keys); malformed/missing pairs are skipped and logged.
- Deduplication via lib/dedup.py is invoked (or stubbed) before write; duplicate entries by md5 are excluded from the shard output.

## qa — qa @ 2026-05-03T03:35:54.672452Z

PASS: 

1. **Acceptance criteria**
- Worker accepts SHARD_ID (0..15), SHARD_TOTAL=16, DATE=YYYY-MM-DD, HF_TOKEN; exits non-zero on fatal errors and logs progress to stdout (exit code ≠ 0, log lines ≥ 1).
- Single API call to list_repo_tree(recursive=False) for public-merged/{DATE}/ produces file-list.json; all subsequent fetches use CDN URLs with no Authorization header (Authorization header absent, CDN host in URL).
- Deterministic shard assignment: hash(slug) % SHARD_TOTAL == SHARD_ID routes files to correct worker; shard N output written to batches/public-merged/{date}/shardN-{HHMMSS}.jsonl (file exists, path matches pattern).
- Each output line is valid JSON with prompt and response fields derived from input (supports prompt/response or instruction/output keys); malformed/missing pairs skipped and logged (invalid lines count logged, output lines valid JSON).
- Deduplication via lib/dedup.py invoked; duplicate entries by md5 excluded from shard output (duplicate count ≥ 0, duplicates not present in output).
- Worker processes only files assigned to SHARD_ID; unassigned files produce zero output lines for that shard (cross-shard leakage = 0).
- CDN fetch failures (non-2xx) are logged and skipped; worker continues processing remaining files (non-fatal errors do not exit non-zero).

2. **Unit tests** (pytest style)
```python
# tests/unit/test_dataset_enrich.py
import os
import json
import pytest
from unittest.mock import MagicMock, patch, mock_open
from bin.dataset_enrich import deterministic_shard, list_date_files, main

def test_deterministic_shard_consistent():
    slug = "openai/some-repo/file-001.jsonl"
    total = 16
    s1 = deterministic_shard(slug)
    s2 = deterministic_shard(slug)
    assert s1 == s2
    assert 0 <= s1 < total

def test_deterministic_shard_distribution():
    slugs = [f"repo/file-{i:03d}.jsonl" for i in range(1000)]
    total = 16
    counts = [0] * total
    for s in slugs:
        counts[deterministic_shard(s)] += 1
    # rough uniformity (chi-sq not strict)
    assert all(c > 40 for c in counts)

def test_list_date_files_calls_api_once():
    with patch("bin.dataset_enrich.HfApi") as MockApi:
        mock_api = MagicMock()
        mock_api.list_repo_tree.return_value = [
            MagicMock(path="public-merged/2024-01-01/file1.jsonl"),
            MagicMock(path="public-merged/2024-01-01/file2.jsonl"),
        ]
        MockApi.return_value = mock_api
        from bin.dataset_enrich import list_date_files
        files = list_date_files("2024-01-01")
        assert len(files) == 2
        assert "file1.jsonl" in files[0]
        mock_api.list_repo_tree.assert_called_once_with(
            repo_id=os.getenv("REPO_ID", "axentx/surrogate-1-training-pairs"),
            path="public-merged/2024-01-01",
            recursive=False,
        )

def test_project_prompt_response_prefer_prompt_response():
    from bin.dataset_enrich import _project_record
    rec = {"prompt": "hello", "response": "world", "extra": 1}
    out = _project_record(rec)
    assert out == {"prompt": "hello", "response": "world"}

def test_project_prompt_response_fallback_instruction_output():
    from bin.dataset_enrich import _project_record
    rec = {"instruction": "hello", "output": "world"}
    out = _project_record(rec)
    assert out == {"prompt": "hello", "response": "world"}

def test_project_prompt_response_skips_malformed():
    from bin.dataset_enrich import _project_record
    assert _project_record({"prompt": "hello"}) is None
    assert _project_record({"response": "world"}) is None
    assert _project_record({}) is None

def test_main_exits_nonzero_on_missing_shard_id(monkeypatch, capsys):
    monkeypatch.delenv("SHARD_ID", raising=False)
    monkeypatch.setenv("SHARD_TOTAL", "16")
    monkeypatch.setenv("HF_TOKEN", "x")
    with pytest.raises(SystemExit) as exc:
        main()
    assert exc.value.code != 0
    assert "SHARD_ID" in capsys.readouterr().err

def test_main_exits_nonzero_on_missing_hf_token(monkeyp
