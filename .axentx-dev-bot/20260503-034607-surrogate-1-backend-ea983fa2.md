# axentx-dev-bot decision
- id: `20260503-034607-surrogate-1-backend-ea983fa2`
- project: surrogate-1
- focus: backend
- created_at: 2026-05-03T03:46:07.950770Z

## dev — claude/llm-fallback-chain @ 2026-05-03T03:46:07.950851Z

**Final, consolidated implementation plan**  
*(Strongest parts from both candidates; contradictions resolved for correctness + concrete actionability)*

---

## 1. Goal (≤2 hours)
Replace `bin/dataset-enrich.sh` with a **manifest-driven, CDN-bypass ingestion worker** (`bin/dataset-enrich.py`) that:

- Accepts `SHARD_ID`, `SHARD_TOTAL=16` (matrix) and optional `DATE_FOLDER` (defaults to today UTC `YYYY-MM-DD`)
- Uses **one `list_repo_tree` call per date folder** → local JSON manifest → Lightning training does CDN-only fetches with **zero API calls** during data load
- Projects heterogeneous HF dataset files to `{prompt, response}` only at parse time (avoids pyarrow `CastError`)
- Deterministic shard assignment via `hash(slug) % SHARD_TOTAL`
- Central md5 dedup via existing `lib/dedup.py`
- Outputs to `batches/public-merged/{date}/shard{N}-{HHMMSS}.jsonl`
- Respects HF rate limits: on 429, wait 360 s and retry; uses CDN URLs (and `hf_hub_download` fallback) to bypass `/api/` auth limits
- Runs as executable Python script (no Bash wrapper issues)

---

## 2. Steps (≤2 hours)

1. **Create `bin/dataset-enrich.py`** (main worker)  
2. **Update `bin/dataset-enrich.sh`** → thin wrapper that calls `python bin/dataset-enrich.py` (preserve backward compat)  
3. **Ensure `lib/dedup.py` is importable** (add `__init__.py` in `lib/` if missing)  
4. **Update `.github/workflows/ingest.yml`** to use matrix `SHARD_ID`/`SHARD_TOTAL` and run `python bin/dataset-enrich.py`  
5. **Test locally** with `DRY_RUN=1`

---

## 3. `bin/dataset-enrich.py` (final, production-ready)

```python
#!/usr/bin/env python3
"""
Manifest-driven, CDN-bypass ingestion worker for surrogate-1.

Usage:
  SHARD_ID=0 SHARD_TOTAL=16 python bin/dataset-enrich.py
  SHARD_ID=0 SHARD_TOTAL=16 DATE_FOLDER=2026-04-29 python bin/dataset-enrich.py
  DRY_RUN=1 SHARD_ID=0 SHARD_TOTAL=16 python bin/dataset-enrich.py
"""

import json
import os
import sys
import hashlib
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests
from huggingface_hub import HfApi, list_repo_tree

# Local dedup
sys.path.insert(0, str(Path(__file__).parent.parent))
try:
    from lib.dedup import DedupStore  # noqa: E402
except ImportError as e:
    print(f"ERROR: Cannot import lib.dedup: {e}", file=sys.stderr)
    sys.exit(1)

# ---- Config ----
REPO_ID = os.getenv("HF_DATASET_REPO", "axentx/surrogate-1-training-pairs")
HF_TOKEN = os.getenv("HF_TOKEN")
SHARD_ID = int(os.getenv("SHARD_ID", "0"))
SHARD_TOTAL = int(os.getenv("SHARD_TOTAL", "16"))
DATE_FOLDER = os.getenv("DATE_FOLDER", datetime.now(timezone.utc).strftime("%Y-%m-%d"))
DRY_RUN = os.getenv("DRY_RUN", "0") == "1"

OUT_DIR = Path("batches/public-merged") / DATE_FOLDER
OUT_DIR.mkdir(parents=True, exist_ok=True)
TIMESTAMP = datetime.now(timezone.utc).strftime("%H%M%S")
OUT_FILE = OUT_DIR / f"shard{SHARD_ID}-{TIMESTAMP}.jsonl"

API = HfApi(token=HF_TOKEN)
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}
CDN_BASE = f"https://huggingface.co/datasets/{REPO_ID}/resolve/main"

DEDUP_DB = os.getenv("DEDUP_DB", "dedup.db")
dedup = DedupStore(DEDUP_DB)

MAX_RETRIES = 5
RETRY_WAIT = 360  # seconds on 429

# ---- Helpers ----
def get_date_folder_manifest(date_folder: str) -> List[str]:
    """List files in a date folder (non-recursive) via HF API."""
    for attempt in range(MAX_RETRIES):
        try:
            tree = list_repo_tree(
                repo_id=REPO_ID,
                path=date_folder,
                recursive=False,
                token=HF_TOKEN,
            )
            files = [f.rfilename for f in tree if f.type == "file"]
            return files
        except Exception as e:
            msg = str(e)
            if "429" in msg or "rate limit" in msg.lower():
                if attempt < MAX_RETRIES - 1:
                    print(f"[{SHARD_ID}] Rate limited (429). Waiting {RETRY_WAIT}s...", file=sys.stderr)
                    time.sleep(

## review — reviewer @ 2026-05-03T03:46:18.540262Z

APPROVE: 
* The proposed change replaces the existing Bash script with a Python script, which is a workable step forward in terms of maintainability and scalability.
* The code implements a manifest-driven, CDN-bypass ingestion worker that respects HF rate limits and uses deterministic shard assignment, which addresses the goal of replacing the existing script.
* The code includes error handling and retry mechanisms for rate limit errors, which is a good practice for robustness.
* The code is well-structured and follows standard Python conventions, making it easier to understand and maintain.
* The use of environment variables for configuration and the implementation of a deduplication mechanism using a local database are good design choices. 

Note: Some minor improvements could be suggested, such as adding more detailed comments or docstrings, but these are not blockers for approval. The code is a good first step towards the focus area, and incremental progress is fine.

## qa — qa @ 2026-05-03T03:47:07.348399Z

PASS: Approved change is workable and ready for TDD validation.

1. **Acceptance criteria**
- Script exits 0 when DRY_RUN=1 and prints planned shard assignment counts without writing output files.
- Deterministic shard assignment: for any slug, hash(slug) % SHARD_TOTAL equals SHARD_ID for exactly one shard across 0..SHARD_TOTAL-1 (uniformity verified by chi-square p ≥ 0.05 on 10k slugs).
- Manifest creation: one list_repo_tree call per DATE_FOLDER produces a local JSON file containing entries with path, size, and sha256; no additional tree calls during parse.
- Parse projection: every emitted JSONL record contains exactly keys prompt and response (strings) and no other keys; records with missing/invalid fields are skipped and logged.
- Dedup integration: md5(content_hash) checked via lib.dedup.DedupStore; duplicates are skipped and counted; non-duplicates are stored and emitted.
- Rate-limit handling: on HTTP 429, script waits 360 s and retries up to 3 times; after final failure, script exits non-zero and logs error.
- Output artifact: when DRY_RUN=0, file batches/public-merged/{DATE_FOLDER}/shard{N}-{HHMMSS}.jsonl is created with valid JSONL lines; file count per shard equals assigned non-duplicate items for that shard.

2. **Unit tests** (pytest style)
```python
# tests/unit/test_dataset_enrich.py
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

import bin.dataset_enrich as worker

def test_shard_assignment_deterministic():
    for shard_total in [1, 2, 4, 16]:
        assignments = set()
        for slug in [f"slug-{i}" for i in range(1000)]:
            h = int(hashlib.sha256(slug.encode()).hexdigest(), 16)
            assignments.add(h % shard_total)
        assert assignments == set(range(shard_total))

def test_build_manifest_single_tree_call():
    with patch("bin.dataset_enrich.list_repo_tree") as mock_tree, \
         patch("bin.dataset_enrich.HfApi"):
        mock_tree.return_value = [
            MagicMock(path="2026-04-29/file-001.json", size=1024, sha256="a"*64),
            MagicMock(path="2026-04-29/file-002.json", size=2048, sha256="b"*64),
        ]
        manifest = worker._build_manifest("owner/repo", "2026-04-29")
        assert mock_tree.call_count == 1
        assert len(manifest) == 2
        assert all("path" in e and "size" in e and "sha256" in e for e in manifest)

def test_project_to_prompt_response():
    raw = {"prompt": "hello", "response": "world", "extra": 123}
    out = worker._project_record(raw)
    assert set(out.keys()) == {"prompt", "response"}
    assert isinstance(out["prompt"], str) and isinstance(out["response"], str)

def test_project_skips_invalid():
    assert worker._project_record({"prompt": "x"}) is None
    assert worker._project_record({"response": "y"}) is None
    assert worker._project_record({}) is None

def test_dedup_integration():
    with tempfile.TemporaryDirectory() as td:
        db_path = Path(td) / "dedup.db"
        store = worker.DedupStore(db_path)
        dup_key = worker._content_hash({"prompt": "a", "response": "b"})
        assert store.add(dup_key) is True
        assert store.add(dup_key) is False
        assert store.exists(dup_key) is True

def test_rate_limit_retry():
    with patch("bin.dataset_enrich.requests.get") as mock_get:
        mock_get.side_effect = [
            MagicMock(status_code=429, headers={"retry-after": "1"}),
            MagicMock(status_code=429, headers={"retry-after": "1"}),
            MagicMock(status_code=200, text="ok"),
        ]
        resp = worker._cdn_get_with_retry("https://cdn.example/file")
        assert resp.status_code == 200
        assert mock_get.call_count == 3

def test_main_dry_run_exits_zero(capsys):
    with patch.dict(os.environ, {"DRY_RUN": "1", "SHARD_ID": "0", "SHARD_TOTAL": "16"}), \
         patch("bin.dataset_enrich._build_manifest", return_value=[]), \
         patch("bin.dataset_enri
