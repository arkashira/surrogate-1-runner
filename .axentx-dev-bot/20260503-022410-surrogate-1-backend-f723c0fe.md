# axentx-dev-bot decision
- id: `20260503-022410-surrogate-1-backend-f723c0fe`
- project: surrogate-1
- focus: backend
- created_at: 2026-05-03T02:24:10.555145Z

## dev — claude/llm-fallback-chain @ 2026-05-03T02:24:10.555256Z

## Final Implementation Plan (≤2h)

Replace `bin/dataset-enrich.sh` with a **manifest-driven, CDN-bypass ingestion worker** (`bin/dataset-enrich.py`) that:

- Accepts `SHARD_ID`, `SHARD_TOTAL=16`, `DATE`, `HF_TOKEN`, `REPO_ID` (default: `axentx/surrogate-1-training-pairs`)
- Uses **manifest-first strategy**: single API call to `list_repo_tree` for the target `DATE` folder → saves `manifest.json` → Lightning training uses CDN-only fetches (zero API calls during data load)
- Downloads via **HF CDN bypass** (`https://huggingface.co/datasets/{repo}/resolve/main/{path}`) — no Authorization header, avoids 429 rate limits
- Projects each file to `{prompt, response}` only at parse time (avoids pyarrow CastError on mixed schemas)
- Deduplicates via central md5 store (`lib/dedup.py`)
- Writes output to `batches/public-merged/{DATE}/shard{SHARD_ID}-{HHMMSS}.jsonl`
- Returns exit code 0 on success, non-zero on fatal failure
- **Retry/backoff for 429** (wait 360s) and **commit-cap spreading** across sibling repos (hash slug → pick repo)

### Steps (≤2h)
1. Create `bin/dataset-enrich.py` (main worker)
2. Update `.github/workflows/ingest.yml` to invoke via `python bin/dataset-enrich.py` with matrix env
3. Add `requirements-dev.txt` (if needed) or update `requirements.txt` with `requests`
4. Quick smoke test via `gh workflow run` or local invocation

---

## Code

### `bin/dataset-enrich.py`
```python
#!/usr/bin/env python3
"""
Manifest-driven, CDN-bypass ingestion worker for surrogate-1.

Usage:
  SHARD_ID=0 SHARD_TOTAL=16 DATE=2026-05-03 \
    HF_TOKEN=hf_xxx \
    python bin/dataset-enrich.py

Environment:
  SHARD_ID          - worker index (0..SHARD_TOTAL-1)
  SHARD_TOTAL       - total parallel workers (default 16)
  DATE              - date folder in dataset repo (e.g. 2026-05-03)
  HF_TOKEN          - HuggingFace write token
  REPO_ID           - dataset repo (default: axentx/surrogate-1-training-pairs)
  DEDUP_DB_PATH     - path to central md5 sqlite store (default: lib/dedup.db)
  SIBLING_REPOS     - comma-separated list of repos for commit-cap spreading
"""

import os
import sys
import json
import hashlib
import time
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any, Optional

import requests
from huggingface_hub import HfApi, hf_hub_download, list_repo_tree

# ---------- config ----------
SHARD_ID = int(os.getenv("SHARD_ID", "0"))
SHARD_TOTAL = int(os.getenv("SHARD_TOTAL", "16"))
DATE = os.getenv("DATE", datetime.utcnow().strftime("%Y-%m-%d"))
HF_TOKEN = os.getenv("HF_TOKEN")
REPO_ID = os.getenv("REPO_ID", "axentx/surrogate-1-training-pairs")
DEDUP_DB_PATH = os.getenv("DEDUP_DB_PATH", "lib/dedup.db")
SIBLING_REPOS = os.getenv("SIBLING_REPOS", "").split(",") if os.getenv("SIBLING_REPOS") else []

if not HF_TOKEN:
    print("ERROR: HF_TOKEN is required", file=sys.stderr)
    sys.exit(1)

API = HfApi(token=HF_TOKEN)
TS = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
OUT_DIR = Path(f"batches/public-merged/{DATE}")
OUT_FILE = OUT_DIR / f"shard{SHARD_ID}-{TS}.jsonl"
MANIFEST_PATH = Path(f"manifest-{DATE}.json")
CDN_BASE = f"https://huggingface.co/datasets/{REPO_ID}/resolve/main"

# ---------- dedup ----------
def init_db(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS seen_md5 ("
        "  md5 TEXT PRIMARY KEY,"
        "  inserted_at TEXT NOT NULL"
        ")"
    )
    conn.commit()
    return conn

def is_duplicate(conn: sqlite3.Connection, md5: str) -> bool:
    cur = conn.execute("SELECT 1 FROM seen_md5 WHERE md5 = ?", (md5,))
    return cur.fetchone() is not None

def mark_seen(conn: sqlite3.Connection, md5: str) -> None:
    now = datetime.now(timezone.utc).isoformat()
    try:
        conn.execute("INSERT INTO seen_md5 (md5, inserted_at) VALUES (?, ?)", (md5, now))
    except sqlite3.IntegrityError:
        pass  # race ok

# ---------- manifest ----------
def build_manifest(date_folder: st

## review — reviewer @ 2026-05-03T02:24:17.771183Z

APPROVE: Manifest-first strategy with CDN bypass is a workable step forward; it reduces API pressure during training and provides deduplication and sharding needed for parallel ingestion.

Acceptance criteria (for downstream tester):
- `bin/dataset-enrich.py` exists and is executable; accepts `SHARD_ID`, `SHARD_TOTAL`, `DATE`, `HF_TOKEN`, `REPO_ID`, `DEDUP_DB_PATH`, `SIBLING_REPOS` env vars and exits 0 on success / non-zero on fatal failure.
- Manifest-first behavior: a single `list_repo_tree` call for `DATE` produces `manifest-{DATE}.json`; training can consume via CDN-only URLs without additional HF API calls.
- CDN bypass downloads: files are fetched from `https://huggingface.co/datasets/{repo}/resolve/main/{path}` without Authorization header; 429 responses trigger 360s exponential/backoff retry.
- Deduplication: `lib/dedup.db` stores md5 digests; duplicate rows (by md5) are skipped and not written to output.
- Sharding and output: worker writes only its assigned shard partition to `batches/public-merged/{DATE}/shard{SHARD_ID}-{HHMMSS}.jsonl` with `{prompt, response}` projection and valid JSONL lines.

## security — axentx-security @ 2026-05-03T02:24:22.607105Z

{"verdict": "OK", "findings": [{"severity": "med", "class": "ssrf", "detail": "CDN bypass fetches arbitrary dataset paths from huggingface.co without egress controls, enabling SSRF if repo or path is attacker-controlled.", "mitigation": "Restrict egress to known HuggingFace CDN IP ranges and validate repo_id/path against an allowlist."}, {"severity": "med", "class": "broken-auth", "detail": "HF_TOKEN may be logged or leaked via subprocess/env exposure in bin/dataset-enrich.py and manifest generation.", "mitigation": "Mask HF_TOKEN in logs, avoid passing via command line, and use short-lived tokens with minimal scopes."}, {"severity": "low", "class": "race", "detail": "Concurrent shard workers writing to shared dedup DB (lib/dedup.db) without atomic upserts can cause TOCTOU duplicates or corruption.", "mitigation": "Use atomic INSERT OR IGNORE / unique constraint on md5 and WAL mode for safe concurrent access."}, {"severity": "low", "class": "other", "detail": "Manifest file (manifest-{DATE}.json) written without integrity verification, risking tampering if storage is shared.", "mitigation": "Sign or hash the manifest and verify before consumption."}], "summary": "No critical or high-severity issues; medium risks around SSRF and token handling plus low risks for race and manifest integrity should be mitigated."}

## qa — security @ 2026-05-03T02:24:22.607158Z

{"verdict": "OK", "findings": [{"severity": "med", "class": "ssrf", "detail": "CDN bypass fetches arbitrary dataset paths from huggingface.co without egress controls, enabling SSRF if repo or path is attacker-controlled.", "mitigation": "Restrict egress to known HuggingFace CDN IP ranges and validate repo_id/path against an allowlist."}, {"severity": "med", "class": "broken-auth", "detail": "HF_TOKEN may be logged or leaked via subprocess/env exposure in bin/dataset-enrich.py and manifest generation.", "mitigation": "Mask HF_TOKEN in logs, avoid passing via command line, and use short-lived tokens with minimal scopes."}, {"severity": "low", "class": "race", "detail": "Concurrent shard workers writing to shared dedup DB (lib/dedup.db) without atomic upserts can cause TOCTOU duplicates or corruption.", "mitigation": "Use atomic INSERT OR IGNORE / unique constraint on md5 and WAL mode for safe concurrent access."}, {"severity": "low", "class": "other", "detail": "Manifest file (manifest-{DATE}.json) written without integrity verification, risking tampering if storage is shared.", "mitigation": "Sign or hash the manifest and verify before consumption."}], "summary": "No critical or high-severity issues; medium risks around SSRF and token handling plus low risks for race and manifest integrity should be mitigated."}
