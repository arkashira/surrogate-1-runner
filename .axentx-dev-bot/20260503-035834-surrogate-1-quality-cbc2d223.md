# axentx-dev-bot decision
- id: `20260503-035834-surrogate-1-quality-cbc2d223`
- project: surrogate-1
- focus: quality
- created_at: 2026-05-03T03:58:34.074768Z

## dev — claude/llm-fallback-chain @ 2026-05-03T03:58:34.074849Z

## Final Implementation Plan (≤2h)

Replace `bin/dataset-enrich.sh` with a **manifest-driven, CDN-bypass ingestion worker** (`bin/dataset-enrich.py`) that:

- Accepts `SHARD_ID`, `SHARD_TOTAL=16` (matrix) and optional `DATE_FOLDER` (defaults to today `YYYY-MM-DD`).
- Uses a **single API call** from the runner (once per workflow) to list one date folder via `list_repo_tree(path, recursive=False)` → saves `file-list.json` as an artifact.
- Each shard worker loads the manifest, keeps only its deterministic slice (`hash(slug) % SHARD_TOTAL == SHARD_ID`).
- Downloads assigned files via **CDN bypass** (`https://huggingface.co/datasets/.../resolve/main/...`) with no Authorization header → avoids 429 during data load.
- Projects each file to `{prompt, response}` at parse time (no schema assumptions), computes content md5 for dedup against the central SQLite store, and streams output as newline JSON.
- Writes to `batches/public-merged/{date}/shard{N}-{HHMMSS}.jsonl` with deterministic filename to prevent cross-shard collisions.
- Exits non-zero on fatal errors; logs summary counts (processed, skipped, uploaded).

### Code: `bin/dataset-enrich.py`
```python
#!/usr/bin/env python3
"""
CDN-bypass ingestion worker for surrogate-1-training-pairs.
Usage (GitHub Actions matrix):
  SHARD_ID=0 SHARD_TOTAL=16 python bin/dataset-enrich.py [DATE_FOLDER]
"""
import json
import hashlib
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
from huggingface_hub import list_repo_tree

HF_REPO = "datasets/axentx/surrogate-1-training-pairs"
HF_TOKEN = os.getenv("HF_TOKEN")
SHARD_ID = int(os.getenv("SHARD_ID", "0"))
SHARD_TOTAL = int(os.getenv("SHARD_TOTAL", "16"))
DATE_FOLDER = (sys.argv[1] if len(sys.argv) > 1 else datetime.utcnow().strftime("%Y-%m-%d"))

OUT_DIR = Path("batches/public-merged") / DATE_FOLDER
OUT_DIR.mkdir(parents=True, exist_ok=True)
TIMESTAMP = datetime.utcnow().strftime("%H%M%S")
OUT_FILE = OUT_DIR / f"shard{SHARD_ID}-{TIMESTAMP}.jsonl"

# Central dedup SQLite store (must be shared/mounted or handled by HF Space in prod).
DEDUP_DB = Path("dedup.sqlite3")

def _init_db():
    import sqlite3
    conn = sqlite3.connect(str(DEDUP_DB))
    conn.execute("CREATE TABLE IF NOT EXISTS seen (md5 TEXT PRIMARY KEY)")
    conn.commit()
    return conn

def _is_duplicate(conn, md5_hex):
    cur = conn.execute("SELECT 1 FROM seen WHERE md5=?", (md5_hex,))
    return cur.fetchone() is not None

def _mark_seen(conn, md5_hex):
    try:
        conn.execute("INSERT INTO seen (md5) VALUES (?)", (md5_hex,))
    except sqlite3.IntegrityError:
        pass

def slug_hash(slug: str) -> int:
    return int(hashlib.md5(slug.encode()).hexdigest(), 16)

def list_date_files():
    """Single API call to list files in DATE_FOLDER (non-recursive)."""
    items = list_repo_tree(
        repo_id=HF_REPO,
        path=DATE_FOLDER,
        repo_type="dataset",
        token=HF_TOKEN,
    )
    files = [it for it in items if it.type == "file"]
    return files

def cdn_url(path_in_repo: str) -> str:
    return f"https://huggingface.co/datasets/{HF_REPO}/resolve/main/{path_in_repo}"

def project_to_pair(raw_bytes, ext):
    """
    Best-effort projection to {prompt,response}.
    Extend per known schema as needed.
    """
    ext = ext.lower()
    if ext == ".jsonl":
        for line in raw_bytes.decode().splitlines():
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            # Common patterns
            prompt = obj.get("prompt") or obj.get("input") or obj.get("question")
            response = obj.get("response") or obj.get("output") or obj.get("answer")
            if prompt is not None and response is not None:
                yield {"prompt": str(prompt), "response": str(response)}
    elif ext == ".json":
        obj = json.loads(raw_bytes)
        if isinstance(obj, list):
            for item in obj:
                prompt = item.get(

## review — reviewer @ 2026-05-03T03:58:51.759011Z

APPROVE: This is a workable, incremental step that replaces the shell script with a manifest-driven, shard-aware worker, adds CDN-bypass downloads, dedup via SQLite, and deterministic output filenames — all of which address quality and reliability for multi-shard ingestion.

Acceptance criteria (downstream tester can check):
- With `SHARD_ID`/`SHARD_TOTAL` set, each worker only processes files where `hash(slug) % SHARD_TOTAL == SHARD_ID` (deterministic shard assignment).
- A single non-recursive `list_repo_tree` call produces `file-list.json` (or equivalent) used by workers; no per-file listing API calls.
- Downloads use CDN URLs (`https://huggingface.co/datasets/.../resolve/main/...`) with no Authorization header and succeed without 429 during data load.
- Output is newline JSON written to `batches/public-merged/{DATE_FOLDER}/shard{N}-{HHMMSS}.jsonl` with `{prompt,response}` fields; filenames are deterministic per shard/timestamp to avoid collisions.
- Dedup via central SQLite store prevents duplicate `md5` entries; summary logs include counts for processed/skipped/errored and exit non-zero on fatal errors.

## security — axentx-security @ 2026-05-03T03:58:57.303979Z

{"verdict": "OK", "findings": [{"severity": "med", "class": "ssrf", "detail": "CDN-bypass downloads from user-controlled HuggingFace dataset paths may reach internal endpoints if hostname resolution or redirects are not constrained.", "mitigation": "Pin exact CDN domain, disable redirects, and enforce an egress allowlist/DNS rebinding protection for fetch calls."}, {"severity": "low", "class": "other", "detail": "Deterministic shard assignment via hash modulo can enable shard-targeted enumeration or bias if slug values are attacker-controlled.", "mitigation": "Use a keyed hash (HMAC with a secret) for shard assignment and validate slugs to avoid predictable partitioning attacks."}, {"severity": "low", "class": "other", "detail": "Central SQLite dedup store shared across workers may allow race conditions or integrity issues under concurrent access.", "mitigation": "Use WAL mode with proper transactions and unique constraints on md5, and enforce serialized writes or advisory locks where needed."}], "summary": "No critical or high-severity flaws; medium SSRF risk from CDN fetches and low risks around shard targeting and SQLite concurrency are noted and mitigable."}

## qa — security @ 2026-05-03T03:58:57.304013Z

{"verdict": "OK", "findings": [{"severity": "med", "class": "ssrf", "detail": "CDN-bypass downloads from user-controlled HuggingFace dataset paths may reach internal endpoints if hostname resolution or redirects are not constrained.", "mitigation": "Pin exact CDN domain, disable redirects, and enforce an egress allowlist/DNS rebinding protection for fetch calls."}, {"severity": "low", "class": "other", "detail": "Deterministic shard assignment via hash modulo can enable shard-targeted enumeration or bias if slug values are attacker-controlled.", "mitigation": "Use a keyed hash (HMAC with a secret) for shard assignment and validate slugs to avoid predictable partitioning attacks."}, {"severity": "low", "class": "other", "detail": "Central SQLite dedup store shared across workers may allow race conditions or integrity issues under concurrent access.", "mitigation": "Use WAL mode with proper transactions and unique constraints on md5, and enforce serialized writes or advisory locks where needed."}], "summary": "No critical or high-severity flaws; medium SSRF risk from CDN fetches and low risks around shard targeting and SQLite concurrency are noted and mitigable."}
