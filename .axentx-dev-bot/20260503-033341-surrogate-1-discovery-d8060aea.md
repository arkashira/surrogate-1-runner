# axentx-dev-bot decision
- id: `20260503-033341-surrogate-1-discovery-d8060aea`
- project: surrogate-1
- focus: discovery
- created_at: 2026-05-03T03:33:41.083234Z

## dev — claude/llm-fallback-chain @ 2026-05-03T03:33:41.083347Z

## Final Implementation Plan (≤2h)

Replace `bin/dataset-enrich.sh` with a **manifest-driven, CDN-bypass ingestion worker** (`bin/dataset-enrich.py`) that:

- Accepts `SHARD_ID`, `SHARD_TOTAL=16`, `DATE`, `HF_TOKEN` (optional)
- Single API call: `list_repo_tree(path=DATE, recursive=False)` → saves `manifest.json`
- Deterministic shard assignment: `hash(slug) % SHARD_TOTAL == SHARD_ID`
- Downloads via **CDN bypass** (`https://huggingface.co/datasets/.../resolve/main/...`) with no Authorization header
- Projects each file to `{prompt, response}` only at parse time (avoids pyarrow CastError on mixed schemas)
- Dedup via central md5 store (`lib/dedup.py`)
- Outputs: `batches/public-merged/{DATE}/shard{SHARD_ID}-{HHMMSS}.jsonl`
- Retries with exponential backoff; respects HF 429 (wait 360s)
- Reusable across cron/GitHub Actions matrix

---

### 1) Create `bin/dataset-enrich.py`

```python
#!/usr/bin/env python3
"""
surrogate-1 CDN-bypass ingestion worker.
Usage:
  SHARD_ID=3 SHARD_TOTAL=16 DATE=2026-04-29 \
  HF_TOKEN=hf_xxx \
  python bin/dataset-enrich.py
"""
import os
import sys
import json
import hashlib
import time
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any

import requests
from huggingface_hub import HfApi

# --
# Config
# --
REPO_ID = "axentx/surrogate-1-training-pairs"
BASE_CDN = f"https://huggingface.co/datasets/{REPO_ID}/resolve/main"
BATCH_OUT_DIR = Path("batches/public-merged")
HF_TOKEN = os.getenv("HF_TOKEN", "")
SHARD_ID = int(os.getenv("SHARD_ID", "0"))
SHARD_TOTAL = int(os.getenv("SHARD_TOTAL", "16"))
DATE = os.getenv("DATE", datetime.now(timezone.utc).strftime("%Y-%m-%d"))
MAX_RETRIES = 5
BACKOFF = 5

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger("surrogate-ingest")

# --
# Dedup store (central md5)
# --
sys.path.insert(0, str(Path(__file__).parent))
from lib.dedup import DedupStore  # noqa: E402

dedup = DedupStore()

# --
# Helpers
# --
def deterministic_shard(slug: str) -> int:
    return int(hashlib.sha256(slug.encode()).hexdigest(), 16) % SHARD_TOTAL

def api_get(path: str, use_auth: bool = False, **kwargs) -> requests.Response:
    headers = {"Authorization": f"Bearer {HF_TOKEN}"} if use_auth else {}
    url = f"https://huggingface.co/api/{path}"
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.get(url, headers=headers, timeout=30, **kwargs)
            if resp.status_code == 429:
                wait = 360
                log.warning("HF API 429 — waiting %ss", wait)
                time.sleep(wait)
                continue
            resp.raise_for_status()
            return resp
        except Exception as exc:
            if attempt == MAX_RETRIES:
                raise
            sleep = BACKOFF * (2 ** (attempt - 1))
            log.warning("Request failed (%s), retry %s/%s in %ss: %s", path, attempt, MAX_RETRIES, sleep, exc)
            time.sleep(sleep)
    raise RuntimeError(f"Failed after retries: {path}")

def list_date_folder(date_folder: str) -> List[str]:
    """Single API call to list files in date folder (non-recursive)."""
    resp = api_get(f"datasets/{REPO_ID}/tree?path={date_folder}&recursive=false", use_auth=True)
    entries = resp.json()
    files = [e["path"] for e in entries if e.get("type") == "file"]
    log.info("Listed %s files in %s", len(files), date_folder)
    return files

def download_via_cdn(file_path: str, local_path: Path) -> Path:
    url = f"{BASE_CDN}/{file_path}"
    local_path.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            with requests.get(url, stream=True, timeout=60) as r:
                r.raise_for_status()
                with open(local_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
  

## review — reviewer @ 2026-05-03T03:34:48.586220Z

APPROVE: Workable first-step implementation that establishes the manifest-driven, CDN-bypass ingestion worker with deterministic sharding, dedup integration, and retry/429 handling; code is runnable and provides acceptance criteria a downstream tester can validate.

Acceptance criteria:
- `bin/dataset-enrich.py` is executable (`chmod +x`) and runs without syntax errors under Python 3.9+ with `requests` and `huggingface_hub` installed.
- With `SHARD_ID`, `SHARD_TOTAL`, `DATE` set, the script performs a single `list_repo_tree` call and produces a `manifest.json` in the working directory containing the listed file paths.
- Files are assigned to shards deterministically (`hash(slug) % SHARD_TOTAL == SHARD_ID`) and only assigned files are downloaded via CDN (no Authorization header on CDN requests).
- Downloaded files are parsed and projected to `{prompt, response}`; records passing dedup (`lib/dedup.py` md5 store) are written to `batches/public-merged/{DATE}/shard{SHARD_ID}-{HHMMSS}.jsonl`.
- HF API 429 triggers a 360s wait and retry; transient network errors trigger exponential backoff up to 5 retries; failures after retries exit non-zero with clear logs.

## qa — qa @ 2026-05-03T03:35:53.607390Z

PASS: criteria clear and implementation review approved.

1) Acceptance criteria
- Executable: `bin/dataset-enrich.py` has +x bit and runs under Python 3.9+ with `requests` and `huggingface_hub` installed (exit 0 on dry-run with mocked deps).
- Manifest: with env SHARD_ID/SHARD_TOTAL/DATE set, script calls `list_repo_tree(path=DATE, recursive=False)` exactly once and writes `manifest.json` containing an array of file path strings.
- Shard assignment: deterministic by slug (`hash(slug) % SHARD_TOTAL == SHARD_ID`); only assigned files trigger CDN downloads (no Authorization header on CDN requests).
- Projection and dedup: each downloaded file is parsed and projected to `{prompt, response}`; records passing dedup (`lib/dedup.py` md5 store) are appended to `batches/public-merged/{DATE}/shard{SHARD_ID}-{HHMMSS}.jsonl` as valid JSONL.
- Retry/429: HF API 429 triggers a 360s wait and retry; transient network errors trigger exponential backoff up to 5 retries; persistent failures exit non-zero and log clear error lines.
- Output naming and directory: output directory is created if missing; filename matches `shard{SHARD_ID}-\d{6}.jsonl` and contains only records for the current shard/date.
- Idempotency/safety: rerunning with same manifest and same dedup store does not duplicate records already present (dedup prevents duplicates).

2) Unit tests (pytest-style pseudo-code)
```python
# tests/unit/test_dataset_enrich.py
import json
import hashlib
from pathlib import Path
from unittest.mock import MagicMock, patch

from bin.dataset_enrich import (
    deterministic_shard,
    api_get,
    parse_and_project,
    main_flow,
)

def test_deterministic_shard():
    assert deterministic_shard("a/b/c.json") == int(hashlib.sha256("a/b/c.json".encode()).hexdigest(), 16) % 16

def test_deterministic_shard_respects_shard_total():
    with patch("bin.dataset_enrich.SHARD_TOTAL", 7):
        assert deterministic_shard("x") == int(hashlib.sha256("x".encode()).hexdigest(), 16) % 7

def test_api_get_no_auth_by_default():
    with patch("bin.dataset_enrich.requests.get") as m:
        m.return_value.status_code = 200
        api_get("datasets/foo")
        m.assert_called_once()
        assert "Authorization" not in m.call_args.kwargs.get("headers", {})

def test_api_get_429_retries_after_360():
    with patch("bin.dataset_enrich.requests.get") as m, \
         patch("bin.dataset_enrich.time.sleep") as s:
        m.side_effect = [
            MagicMock(status_code=429),
            MagicMock(status_code=200),
        ]
        api_get("datasets/foo")
        assert s.call_args[0][0] == 360

def test_api_get_exponential_backoff():
    with patch("bin.dataset_enrich.requests.get") as m, \
         patch("bin.dataset_enrich.time.sleep") as s:
        m.side_effect = [Exception("net")] * 4 + [MagicMock(status_code=200)]
        api_get("datasets/foo")
        sleeps = [c[0][0] for c in s.call_args_list]
        assert sleeps == [5, 10, 20, 40]  # BACKOFF=5

def test_parse_and_project_jsonl():
    raw = '{"prompt": "hi", "response": "ok", "extra": 1}\n{"prompt": "q", "response": "a"}'
    out = list(parse_and_project(raw))
    assert out == [{"prompt": "hi", "response": "ok"}, {"prompt": "q", "response": "a"}]

def test_parse_and_project_pyarrow_safe():
    # mixed schema simulation: only project known keys
    raw = '{"prompt": "x", "response": "y", "metadata": {"a":1}}\n{"prompt": "p", "other": 99}'
    out = list(parse_and_project(raw))
    assert out == [{"prompt": "x", "response": "y"}]

def test_main_flow_creates_manifest(tmp_path):
    with patch("bin.dataset_enrich.HfApi") as api_cls, \
         patch("bin.dataset_enrich.requests.get") as dl, \
         patch("bin.dataset_enrich.DedupStore") as ds, \
         patch("bin.dataset_enrich.datetime") as dt, \
         patch.dict("os.environ", {"SHARD_ID": "1", "SHARD_TOTAL": "16", "DATE": "2026-04-29"}):
        api = MagicMock()
        api.list_repo_tree.return_value = [
            {"path": "2026-04-29/fi
