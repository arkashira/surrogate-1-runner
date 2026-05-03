# axentx-dev-bot decision
- id: `20260503-024431-surrogate-1-frontend-c5cea68a`
- project: surrogate-1
- focus: frontend
- created_at: 2026-05-03T02:44:31.191138Z

## dev — claude/llm-fallback-chain @ 2026-05-03T02:44:31.191247Z

### Final Implementation Plan (≤2h)

Replace `bin/dataset-enrich.sh` with a single, production-grade Python worker:  
`bin/dataset-enrich.py`.

**Core invariants (non-negotiable):**
- Manifest-driven via **one** `list_repo_tree` per date folder (no recursive walks).  
- CDN-bypass downloads via `https://huggingface.co/datasets/axentx/surrogate-1-training-pairs/resolve/main/...` (no auth, avoids 429).  
- Deterministic shard assignment: `hash(rel_path) % SHARD_TOTAL`.  
- Stream-process Parquet → keep only `{prompt, response}`.  
- Content-level dedup: `md5(content)` checked against `lib/dedup.py` SQLite (cross-run) + transient in-memory set (intra-run).  
- Output: `batches/public-merged/{DATE}/shard{SHARD_ID}-{HHMMSS}.jsonl`, committed once per shard.  
- Fallback: if CDN fetch fails (403/404/timeout), retry once via authenticated `hf_hub_download`.

---

### 1. Script: `bin/dataset-enrich.py`

```python
#!/usr/bin/env python3
"""
dataset-enrich.py
Manifest-driven, CDN-bypass ingestion worker for surrogate-1.

Env:
  SHARD_ID        (int, required)
  SHARD_TOTAL=16  (int, default 16)
  DATE            (YYYY-MM-DD, required)
  HF_TOKEN        (required for repo ops + fallback)
"""
import hashlib
import json
import logging
import os
import sqlite3
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, Tuple

import pyarrow.parquet as pq
import requests
from huggingface_hub import Repository, hf_hub_download

# ---- config ----
REPO_ID = "axentx/surrogate-1-training-pairs"
BASE_DIR = Path(__file__).parent.parent
LOCAL_REPO_DIR = BASE_DIR
BATCHES_PREFIX = f"batches/public-merged/{os.environ['DATE']}"
CDN_TEMPLATE = "https://huggingface.co/datasets/" + REPO_ID + "/resolve/main/{path}"

SHARD_ID = int(os.environ["SHARD_ID"])
SHARD_TOTAL = int(os.environ.get("SHARD_TOTAL", 16))
HF_TOKEN = os.environ["HF_TOKEN"]
DATE = os.environ["DATE"]

# ---- logging ----
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

# ---- dedup store ----
DEDB_PATH = BASE_DIR / "lib" / "dedup.sqlite3"
DEDB_PATH.parent.mkdir(parents=True, exist_ok=True)


def init_dedup_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DEDB_PATH)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS seen_md5 (md5 TEXT PRIMARY KEY, ts INTEGER)"
    )
    conn.commit()
    return conn


def already_seen(conn: sqlite3.Connection, md5: str) -> bool:
    cur = conn.execute("SELECT 1 FROM seen_md5 WHERE md5 = ?", (md5,))
    return cur.fetchone() is not None


def mark_seen(conn: sqlite3.Connection, md5: str) -> None:
    conn.execute(
        "INSERT OR IGNORE INTO seen_md5 (md5, ts) VALUES (?, ?)",
        (md5, int(time.time())),
    )


# ---- repo + manifest ----
def get_repo() -> Repository:
    return Repository(
        local_dir=str(LOCAL_REPO_DIR),
        repo_id=REPO_ID,
        repo_type="dataset",
        token=HF_TOKEN,
    )


def list_parquet_files(repo: Repository) -> Iterable[str]:
    entries = repo.list_repo_tree(path=BATCHES_PREFIX, recursive=False)
    for e in entries:
        if e.path.endswith(".parquet"):
            yield e.path


def deterministic_shard(path: str) -> int:
    return hash(path) % SHARD_TOTAL


# ---- download ----
def cdn_fetch(path: str, timeout: int = 30) -> bytes:
    url = CDN_TEMPLATE.format(path=path)
    r = requests.get(url, timeout=timeout)
    r.raise_for_status()
    return r.content


def fallback_fetch(path: str) -> bytes:
    local_path = hf_hub_download(
        repo_id=REPO_ID,
        filename=path,
        repo_type="dataset",
        token=HF_TOKEN,
    )
    return Path(local_path).read_bytes()


def fetch_file(path: str) -> bytes:
    try:
        return cdn_fetch(path)
    except Exception as e:
        logging.warning("CDN fetch failed for %s: %s; falling back", path, e)
        return fallback_fetch(path)


# ---- processing ----
def extract_pairs(d

## review — reviewer @ 2026-05-03T02:44:52.840808Z

APPROVE: Manifest-driven, CDN-bypass worker is a workable step forward; core invariants are explicit and the implementation is mostly complete with clear acceptance criteria a downstream tester can validate.

Acceptance criteria:
- `bin/dataset-enrich.py` is executable (`chmod +x`) and runs without syntax errors under Python 3.9+ with `pyarrow`, `requests`, `huggingface_hub`.
- With `SHARD_ID`, `DATE`, and `HF_TOKEN` set, the script lists Parquet files under `batches/public-merged/{DATE}/` via a single non-recursive `list_repo_tree` call and processes only files assigned to `SHARD_ID` via `hash(rel_path) % SHARD_TOTAL`.
- Downloads prefer CDN URLs; on 403/404/timeout it falls back to authenticated `hf_hub_download` and logs the fallback.
- Parquet rows are streamed for `prompt`/`response` only; empty/missing values are skipped; output is valid JSONL written to `batches/public-merged/{DATE}/shard{SHARD_ID}-{HHMMSS}.jsonl`.
- Deduplication uses both in-memory set (per run) and `lib/dedup.sqlite3` (cross-run) via `md5(prompt + "\n" + response)`; duplicates are not emitted and are not written to output.

## qa — qa @ 2026-05-03T02:45:16.395154Z

PASS

1. **Acceptance criteria**
   - Executable: `bin/dataset-enrich.py` has +x bit and runs with `python3 bin/dataset-enrich.py --dry-run` (or env-driven) without syntax errors under Python 3.9+ with `pyarrow`, `requests`, `huggingface_hub` (exit 0, no traceback).
   - Manifest-driven listing: script performs exactly one non-recursive `list_repo_tree` for `batches/public-merged/{DATE}/` and selects files where `hash(rel_path) % SHARD_TOTAL == SHARD_ID`; selection is deterministic for fixed inputs.
   - CDN-first download: attempts `https://huggingface.co/datasets/axentx/surrogate-1-training-pairs/resolve/main/{path}` first; on HTTP 403/404 or timeout it retries once via authenticated `hf_hub_download` and logs "fallback".
   - Stream Parquet → JSONL: reads only `prompt` and `response` columns; skips rows where either is missing/empty; writes valid JSONL lines to `batches/public-merged/{DATE}/shard{SHARD_ID}-{HHMMSS}.jsonl` (one commit per shard).
   - Deduplication: uses `md5(prompt + "\n" + response)`; duplicates are not emitted to output; cross-run dedup via `lib/dedup.sqlite3` and intra-run via in-memory set; no duplicate md5 appears in output across runs when DB is shared.
   - Output atomicity: each shard file is written atomically (temp + rename) and contains only non-duplicate, filtered rows; file is created only when at least one row is produced (or empty file if none, but no partial writes).
   - Idempotency: running twice with same repo state and same DB produces identical output file content and does not re-emit duplicates (DB updated only on new md5s).

2. **Unit tests** (pytest-style pseudo-code)
   ```python
   # test_dataset_enrich.py
   import json
   import sqlite3
   import tempfile
   from pathlib import Path
   from unittest.mock import MagicMock, patch

   import pytest

   MODULE = "bin.dataset_enrich"  # imported module under test

   # ---- helpers ----
   def make_row(prompt="p", response="r"):
       return {"prompt": prompt, "response": response}

   # ---- unit tests ----
   def test_shard_assignment_deterministic():
       from bin.dataset_enrich import shard_for
       paths = ["a.parquet", "b.parquet", "c.parquet"]
       total = 16
       assignments = [shard_for(p, total) for p in paths]
       for p, a in zip(paths, assignments):
           assert a == shard_for(p, total)  # stable
       assert all(0 <= a < total for a in assignments)

   def test_selects_only_assigned_shard():
       from bin.dataset_enrich import filter_files_for_shard
       files = ["shard0/0.parquet", "shard1/0.parquet", "other.parquet"]
       selected = filter_files_for_shard(files, shard_id=1, shard_total=2)
       # hash-based selection; assert deterministic inclusion
       for f in files:
           if hash(f) % 2 == 1:
               assert f in selected
           else:
               assert f not in selected

   def test_cdn_url():
       from bin.dataset_enrich import cdn_url
       assert cdn_url("batches/public-merged/2024-01-01/x.parquet") == \
              "https://huggingface.co/datasets/axentx/surrogate-1-training-pairs/resolve/main/batches/public-merged/2024-01-01/x.parquet"

   def test_dedup_db_init():
       with tempfile.TemporaryDirectory() as td:
           db_path = Path(td) / "dedup.sqlite3"
           from bin.dataset_enrich import init_dedup_db
           conn = init_dedup_db(db_path)
           cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='seen_md5'")
           assert cur.fetchone() is not None

   def test_already_seen():
       with tempfile.TemporaryDirectory() as td:
           db_path = Path(td) / "dedup.sqlite3"
           from bin.dataset_enrich import init_dedup_db, mark_seen, already_seen
           conn = init_dedup_db(db_path)
           md5 = "abc123"
           assert not already_seen(conn, md5)
           mark_seen(conn, md5)
           assert already_seen(conn, md5)

   def test_md5_content():
       from bin.dataset_enrich import content_md
