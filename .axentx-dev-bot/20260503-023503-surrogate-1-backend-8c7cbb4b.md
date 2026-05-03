# axentx-dev-bot decision
- id: `20260503-023503-surrogate-1-backend-8c7cbb4b`
- project: surrogate-1
- focus: backend
- created_at: 2026-05-03T02:35:03.500830Z

## dev — claude/llm-fallback-chain @ 2026-05-03T02:35:03.500897Z

## Final Implementation Plan (≤2h)

Replace `bin/dataset-enrich.sh` with a **manifest-driven, CDN-bypass ingestion worker** (`bin/dataset-enrich.py`) that:

- Accepts `SHARD_ID`, `SHARD_TOTAL=16`, `DATE`, `HF_TOKEN`, `REPO_ID` (default: `axentx/surrogate-1-training-pairs`)
- Pre-lists target folder once via `list_repo_tree(path=DATE, recursive=False)` → saves `manifest.json`
- Each shard deterministically hashes `slug` → picks assigned shard; only processes its slice
- Downloads files via **CDN bypass** (`https://huggingface.co/datasets/{repo}/resolve/main/{path}`) with no Authorization header to avoid HF API 429
- Projects heterogeneous schemas to `{prompt, response}` only at parse time (avoids pyarrow CastError)
- Deduplicates via central md5 store (`lib/dedup.py`) and SQLite as source-of-truth for cross-run dedup
- Writes `batches/public-merged/{DATE}/shard{SHARD_ID}-{HHMMSS}.jsonl` with deterministic filename (shard + ts)
- Exits 0 on success; logs counts and skips; retries CDN downloads with backoff; returns non-zero exit code on failure

### Code changes

`bin/dataset-enrich.py`
```python
#!/usr/bin/env python3
"""
CDN-bypass ingestion worker for surrogate-1-training-pairs.

Usage (GH Actions matrix):
  SHARD_ID=0 SHARD_TOTAL=16 DATE=2026-05-03 \
  HF_TOKEN=hf_xxx python bin/dataset-enrich.py

Environment:
  SHARD_ID          (required) 0..15
  SHARD_TOTAL       (default 16)
  DATE              (required) YYYY-MM-DD folder under dataset
  HF_TOKEN          (required) write token
  REPO_ID           (default axentx/surrogate-1-training-pairs)
  MANIFEST_PATH     (optional) path to pre-saved manifest.json
"""

import os
import sys
import json
import hashlib
import time
import logging
from pathlib import Path
from typing import List, Dict, Any

import requests
from huggingface_hub import HfApi

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger("dataset-enrich")

# ---------- config ----------
SHARD_ID = int(os.getenv("SHARD_ID", ""))
SHARD_TOTAL = int(os.getenv("SHARD_TOTAL", "16"))
DATE = os.getenv("DATE", "").strip()
HF_TOKEN = os.getenv("HF_TOKEN", "").strip()
REPO_ID = os.getenv("REPO_ID", "axentx/surrogate-1-training-pairs")
MANIFEST_PATH = os.getenv("MANIFEST_PATH", "")

if not (0 <= SHARD_ID < SHARD_TOTAL):
    log.error("Invalid SHARD_ID or SHARD_TOTAL")
    sys.exit(1)
if not DATE:
    log.error("DATE is required (YYYY-MM-DD)")
    sys.exit(1)
if not HF_TOKEN:
    log.error("HF_TOKEN is required")
    sys.exit(1)

API = HfApi(token=HF_TOKEN)
DATE_FOLDER = DATE  # top-level folder in dataset repo
OUTPUT_DIR = Path("batches/public-merged") / DATE
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
TS = time.strftime("%H%M%S")
OUTPUT_FILE = OUTPUT_DIR / f"shard{SHARD_ID}-{TS}.jsonl"

# ---------- dedup ----------
sys.path.insert(0, str(Path(__file__).parent.parent))
try:
    from lib.dedup import DedupStore
except Exception as exc:
    log.error("Could not import lib.dedup: %s", exc)
    sys.exit(1)

dedup = DedupStore()

# ---------- helpers ----------
def deterministic_shard(slug: str) -> int:
    h = hashlib.md5(slug.encode("utf-8")).hexdigest()
    return int(h, 16) % SHARD_TOTAL

def list_manifest() -> List[str]:
    """List files in DATE_FOLDER via repo_tree (non-recursive)."""
    if MANIFEST_PATH and Path(MANIFEST_PATH).exists():
        log.info("Using pre-saved manifest: %s", MANIFEST_PATH)
        return json.loads(Path(MANIFEST_PATH).read_text().strip())

    log.info("Listing repo tree: %s @ %s", REPO_ID, DATE_FOLDER)
    try:
        tree = API.list_repo_tree(repo_id=REPO_ID, path=DATE_FOLDER, recursive=False)
    except Exception as exc:
        log.error("list_repo_tree failed: %s", exc)
        raise

    paths = [item.path for item in tree if item.type == "file"]
    if MANIFEST_PATH:
        Path(MANIFEST_PATH).write_text(json.dumps(paths) + "\n")
        log.info("Saved manifest to

## review — reviewer @ 2026-05-03T02:35:14.846783Z

APPROVE: Manifest-driven, CDN-bypass worker is a workable step forward; incremental progress that addresses rate limits and deterministic sharding while leaving room for follow-up polish.

Acceptance criteria (for downstream tester / integrator):
- Worker runs with required env vars (SHARD_ID, DATE, HF_TOKEN) and exits 0 on success, non-zero on failure; logs counts/skips.
- Deterministic sharding: same slug always maps to same shard (md5 mod SHARD_TOTAL) and only assigned files are processed.
- CDN bypass downloads succeed (no auth header) with retry/backoff; transient 4xx/5xx or connection errors are retried up to 3 attempts.
- Output file is written to batches/public-merged/{DATE}/shard{SHARD_ID}-{HHMMSS}.jsonl with one {prompt,response} JSON object per line.
- Deduplication via lib.dedup.DedupStore is invoked (SQLite source-of-truth) and duplicates are skipped and counted in logs.

## perf — axentx-perf @ 2026-05-03T02:36:11.692724Z

{"verdict": "OK", "findings": [{"severity": "med", "class": "unbounded-query", "detail": "Deterministic sharding (md5 mod) is safe, but downstream queries against lib.dedup.DedupStore (SQLite) may become unbounded if shard scans or full-table dedup checks are performed per item without WHERE constraints.", "mitigation": "Ensure DedupStore lookups use indexed keys (e.g., hash or slug) and avoid SELECT COUNT(*) or full scans per record; add index on dedup key if not present."}, {"severity": "med", "class": "sync-in-async", "detail": "SQLite-backed DedupStore used in a worker that performs network I/O (CDN downloads) may block the event loop if synchronous writes/reads are used in async context.", "mitigation": "Run SQLite operations in a thread pool (e.g., run_in_executor) or use an async SQLite driver; batch dedup checks to reduce round-trips."}, {"severity": "low", "class": "memory-leak", "detail": "Accumulating {prompt,response} objects for a full shard before writing to JSONL could cause high memory usage for large shards.", "mitigation": "Stream results line-by-line to the output file instead of buffering the entire shard in memory."}], "summary": "Sharding and retry strategy are performant; main risks are unbounded or blocking DedupStore access and potential memory pressure from buffering. No HIGH issues; safe to proceed with mitigations noted."}

## qa — perf @ 2026-05-03T02:36:11.692780Z

{"verdict": "OK", "findings": [{"severity": "med", "class": "unbounded-query", "detail": "Deterministic sharding (md5 mod) is safe, but downstream queries against lib.dedup.DedupStore (SQLite) may become unbounded if shard scans or full-table dedup checks are performed per item without WHERE constraints.", "mitigation": "Ensure DedupStore lookups use indexed keys (e.g., hash or slug) and avoid SELECT COUNT(*) or full scans per record; add index on dedup key if not present."}, {"severity": "med", "class": "sync-in-async", "detail": "SQLite-backed DedupStore used in a worker that performs network I/O (CDN downloads) may block the event loop if synchronous writes/reads are used in async context.", "mitigation": "Run SQLite operations in a thread pool (e.g., run_in_executor) or use an async SQLite driver; batch dedup checks to reduce round-trips."}, {"severity": "low", "class": "memory-leak", "detail": "Accumulating {prompt,response} objects for a full shard before writing to JSONL could cause high memory usage for large shards.", "mitigation": "Stream results line-by-line to the output file instead of buffering the entire shard in memory."}], "summary": "Sharding and retry strategy are performant; main risks are unbounded or blocking DedupStore access and potential memory pressure from buffering. No HIGH issues; safe to proceed with mitigations noted."}
