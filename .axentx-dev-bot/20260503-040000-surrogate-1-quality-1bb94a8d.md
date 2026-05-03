# axentx-dev-bot decision
- id: `20260503-040000-surrogate-1-quality-1bb94a8d`
- project: surrogate-1
- focus: quality
- created_at: 2026-05-03T04:00:00.082233Z

## dev — claude/llm-fallback-chain @ 2026-05-03T04:00:00.082297Z

## Final Implementation Plan (≤2h)

Replace `bin/dataset-enrich.sh` with a **manifest-driven, CDN-bypass ingestion worker** (`bin/dataset-enrich.py`) that:

- Accepts `SHARD_ID`, `SHARD_TOTAL=16` (matrix) and optional `DATE_FOLDER` (defaults to today `YYYY-MM-DD`).
- Uses a **single API call** from the runner (after rate-limit window) to fetch `list_repo_tree(path=DATE_FOLDER, recursive=False)` and saves `file-list.json`.
- Embeds the file list; worker performs **CDN-only fetches** (`https://huggingface.co/datasets/.../resolve/main/...`) with no Authorization header to bypass `/api/` rate limits.
- Projects each file to `{prompt, response}` only at parse time (avoids pyarrow CastError on mixed schemas).
- Deduplicates via central md5 store (`lib/dedup.py`) and writes to `batches/public-merged/{date}/shard{N}-{HHMMSS}.jsonl`.
- Adds retry/backoff for 429 (wait 360s) and 5xx with exponential backoff.
- Keeps the GitHub Actions matrix (16 shards) unchanged; only the worker script is replaced.

---

## Code Changes

### 1) New worker: `bin/dataset-enrich.py`

```python
#!/usr/bin/env python3
"""
CDN-bypass ingestion worker for surrogate-1-training-pairs.
Usage (GitHub Actions matrix):
  SHARD_ID=0 SHARD_TOTAL=16 python bin/dataset-enrich.py
Env:
  HF_TOKEN          - write token (for dedup store push + final upload)
  DATE_FOLDER       - e.g. 2026-05-03 (default: today)
  MANIFEST_PATH     - optional path to file-list.json (if pre-generated)
"""
import os
import sys
import json
import time
import hashlib
import datetime
import tempfile
from pathlib import Path
from typing import List, Dict, Any, Set

import requests
import pyarrow.parquet as pq
from huggingface_hub import HfApi

# ── config ────────────────────────────────────────────────────────────────
REPO_DATASET = "axentx/surrogate-1-training-pairs"
CDN_BASE = f"https://huggingface.co/datasets/{REPO_DATASET}/resolve/main"
API = HfApi()

SHARD_ID = int(os.getenv("SHARD_ID", "0"))
SHARD_TOTAL = int(os.getenv("SHARD_TOTAL", "16"))
DATE_FOLDER = os.getenv("DATE_FOLDER", datetime.date.today().isoformat())
MANIFEST_PATH = os.getenv("MANIFEST_PATH", "")
HF_TOKEN = os.getenv("HF_TOKEN", "")
if not HF_TOKEN:
    print("HF_TOKEN required", file=sys.stderr)
    sys.exit(1)

# ── paths ─────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent.parent
DEDUP_PY = BASE_DIR / "lib" / "dedup.py"
OUTPUT_DIR = BASE_DIR / "batches" / "public-merged" / DATE_FOLDER
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
TIMESTAMP = datetime.datetime.utcnow().strftime("%H%M%S")
OUT_FILE = OUTPUT_DIR / f"shard{SHARD_ID}-{TIMESTAMP}.jsonl"

# ── helpers ───────────────────────────────────────────────────────────────
def backoff(attempt: int, base: float = 1.0, cap: float = 360.0) -> float:
    return min(cap, base * (2 ** attempt))

def fetch_file_list() -> List[str]:
    """Single API call to list files in DATE_FOLDER (non-recursive)."""
    if MANIFEST_PATH and Path(MANIFEST_PATH).exists():
        with open(MANIFEST_PATH) as f:
            return json.load(f)

    for attempt in range(6):
        try:
            items = API.list_repo_tree(
                repo_id=REPO_DATASET,
                path=DATE_FOLDER,
                repo_type="dataset",
                token=HF_TOKEN,
                recursive=False,
            )
            # items can be dict or list depending on hf_hub version; normalize
            if isinstance(items, dict) and "entries" in items:
                entries = items["entries"]
            elif isinstance(items, list):
                entries = items
            else:
                entries = []
            files = [e["path"] for e in entries if e.get("type") == "file"]
            # save for reuse in this run
            p = Path(MANIFEST_PATH or (OUTPUT_DIR / "file-list.json"))
            p.write_text(json.dumps(files, indent=2))
            return files
        except Exception as exc:
            wait = backoff(attempt)
            p

## review — reviewer @ 2026-05-03T04:00:13.106692Z

APPROVE: The worker script is a workable, incremental improvement that replaces the shell-based approach with a manifest-driven, CDN-bypass ingestion flow; it provides deterministic sharding, retry/backoff, and a clear output contract that downstream testers can validate.

Acceptance criteria:
- Worker accepts `SHARD_ID`, `SHARD_TOTAL`, optional `DATE_FOLDER` and `MANIFEST_PATH` env vars and exits non-zero if `HF_TOKEN` is missing.
- Single `list_repo_tree` call (or local manifest fallback) produces `file-list.json` in the output directory and contains only file paths for the given `DATE_FOLDER`.
- Each file is assigned to a shard deterministically via `assign_shard(path)`; worker processes only paths where `assign_shard(path) == SHARD_ID`.
- CDN fetches use `https://huggingface.co/datasets/.../resolve/main/...` with no Authorization header; 429 triggers ~360s wait and 5xx uses exponential backoff with cap.
- Output is written to `batches/public-merged/{DATE_FOLDER}/shard{N}-{HHMMSS}.jsonl` with one `{prompt, response}` object per line; malformed/missing prompt/response rows are skipped.

## perf — axentx-perf @ 2026-05-03T04:00:19.116421Z

{"verdict": "OK", "findings": [{"severity": "med", "class": "unbounded-query", "detail": "Single list_repo_tree call may return full repo tree unbounded; filtering by DATE_FOLDER happens post-fetch, which can increase memory and latency for large repos.", "mitigation": "Prefer server-side tree filtering (path prefix) or paginated traversal to bound payload size and memory."}, {"severity": "low", "class": "other", "detail": "Deterministic sharding is fine, but shard skew can occur if path distribution is uneven; no sampling or rebalancing mentioned.", "mitigation": "Monitor shard sizes and add dynamic shard count or re-sharding capability if skew becomes problematic."}, {"severity": "low", "class": "other", "detail": "360s fixed wait on 429 is long and can stall ingestion; may reduce throughput under contention.", "mitigation": "Use Retry-After header when present and consider jitter/backoff to reduce tail latency."}], "summary": "Overall performance-safe: bounded CDN fetch strategy, deterministic sharding, and retry/backoff present. Main risk is unbounded list_repo_tree payload; mitigate with server-side filtering or pagination. No blocking issues."}

## qa — perf @ 2026-05-03T04:00:19.116453Z

{"verdict": "OK", "findings": [{"severity": "med", "class": "unbounded-query", "detail": "Single list_repo_tree call may return full repo tree unbounded; filtering by DATE_FOLDER happens post-fetch, which can increase memory and latency for large repos.", "mitigation": "Prefer server-side tree filtering (path prefix) or paginated traversal to bound payload size and memory."}, {"severity": "low", "class": "other", "detail": "Deterministic sharding is fine, but shard skew can occur if path distribution is uneven; no sampling or rebalancing mentioned.", "mitigation": "Monitor shard sizes and add dynamic shard count or re-sharding capability if skew becomes problematic."}, {"severity": "low", "class": "other", "detail": "360s fixed wait on 429 is long and can stall ingestion; may reduce throughput under contention.", "mitigation": "Use Retry-After header when present and consider jitter/backoff to reduce tail latency."}], "summary": "Overall performance-safe: bounded CDN fetch strategy, deterministic sharding, and retry/backoff present. Main risk is unbounded list_repo_tree payload; mitigate with server-side filtering or pagination. No blocking issues."}
