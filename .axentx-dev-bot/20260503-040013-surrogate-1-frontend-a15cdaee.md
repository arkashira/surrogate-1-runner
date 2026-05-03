# axentx-dev-bot decision
- id: `20260503-040013-surrogate-1-frontend-a15cdaee`
- project: surrogate-1
- focus: frontend
- created_at: 2026-05-03T04:00:13.177919Z

## dev — claude/llm-fallback-chain @ 2026-05-03T04:00:13.178027Z

## Final Implementation Plan (≤2h)

Replace `bin/dataset-enrich.sh` with a **manifest-driven, CDN-bypass ingestion worker** (`bin/dataset-enrich.py`) that:

- Accepts `SHARD_ID`, `SHARD_TOTAL=16` (matrix) and optional `DATE_FOLDER` (defaults to today `YYYY-MM-DD`).
- Uses a **manifest-first strategy**:
  - If `manifest/{DATE_FOLDER}.json` exists, use it (avoids recursive API calls and rate limits).
  - Otherwise, fall back to a **single non-recursive `list_repo_tree` API call** to list the date folder and cache it as `manifest/{DATE_FOLDER}.json`.
- Deterministic shard assignment: `hash(slug) % SHARD_TOTAL == SHARD_ID`.
- Downloads only assigned files via **HF CDN bypass** (`https://huggingface.co/datasets/.../resolve/main/...`) with no Authorization header.
- Projects each file to `{prompt, response}` at parse time (avoids `load_dataset(streaming=True)` on mixed schemas).
- Deduplicates via central `lib/dedup.py` md5 store.
- Outputs `batches/public-merged/{DATE_FOLDER}/shard{SHARD_ID}-{HHMMSS}.jsonl` and uploads to the dataset repo via HF API.
- Reuses existing GitHub Actions matrix (`ingest.yml`) unchanged.

---

## Code Changes

### 1) New worker: `bin/dataset-enrich.py`

```python
#!/usr/bin/env python3
"""
surrogate-1 CDN-bypass ingestion worker (manifest-first).

Usage (GitHub Actions matrix):
  SHARD_ID=3 SHARD_TOTAL=16 python bin/dataset-enrich.py

Env:
  HF_TOKEN         - write token for axentx/surrogate-1-training-pairs
  DATE_FOLDER      - e.g. 2026-05-03 (default: today)
  DATASET_REPO     - default: axentx/surrogate-1-training-pairs
"""
import os
import sys
import json
import hashlib
import datetime
from pathlib import Path

import requests
from huggingface_hub import HfApi, hf_hub_download

# ── config --
DATASET_REPO = os.getenv("DATASET_REPO", "axentx/surrogate-1-training-pairs")
HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    print("HF_TOKEN required", file=sys.stderr)
    sys.exit(1)

SHARD_ID = int(os.getenv("SHARD_ID", "0"))
SHARD_TOTAL = int(os.getenv("SHARD_TOTAL", "16"))
DATE_FOLDER = os.getenv("DATE_FOLDER", datetime.date.today().isoformat())

API = HfApi(token=HF_TOKEN)

# ── helpers --
def deterministic_shard(slug: str) -> int:
    return int(hashlib.md5(slug.encode()).hexdigest(), 16) % SHARD_TOTAL

def ensure_manifest() -> list[str]:
    """
    Use manifest/{DATE_FOLDER}.json if present.
    Otherwise, list date folder once (non-recursive) and cache it.
    Returns list of file paths (relative to dataset root).
    """
    manifest_dir = Path("manifest")
    manifest_dir.mkdir(exist_ok=True)
    manifest_path = manifest_dir / f"{DATE_FOLDER}.json"

    if manifest_path.is_file():
        with manifest_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list) and all(isinstance(x, str) for x in data):
            return data

    print(f"[shard {SHARD_ID}] manifest not found or invalid; listing {DATE_FOLDER} ...")
    items = API.list_repo_tree(
        repo_id=DATASET_REPO,
        path=DATE_FOLDER,
        repo_type="dataset",
        recursive=False,
    )
    files = [it.rfilename for it in items if it.type == "file"]

    with manifest_path.open("w", encoding="utf-8") as f:
        json.dump(files, f)

    return files

def project_to_pair(raw_obj) -> dict | None:
    """
    Best-effort projection to {prompt, response}.
    Accepts dict-like or HF dataset row.
    """
    d = dict(raw_obj) if not isinstance(raw_obj, dict) else raw_obj

    prompt_keys = {"prompt", "instruction", "input", "question", "text"}
    response_keys = {"response", "completion", "output", "answer", "result"}

    prompt = None
    response = None

    for k in d:
        if k in prompt_keys and prompt is None:
            prompt = str(d[k]).strip()
        if k in response_keys and response is None:
            response = str(d[k]).strip()

    if prompt is None and response is None:
        for k in d:
            if isinstance(d[k], str) and d[k].strip():
       

## review — reviewer @ 2026-05-03T04:00:28.091959Z

APPROVE: Manifest-first worker is a clear, incremental improvement over shell-based recursive ingestion; deterministic sharding, dedup integration, and CDN-bypass pattern are sound and testable.

Acceptance criteria:
- Worker runs with `SHARD_ID`/`SHARD_TOTAL` env vars and produces `batches/public-merged/{DATE_FOLDER}/shard{SHARD_ID}-{HHMMSS}.jsonl` containing valid `{prompt, response}` JSONL lines.
- Manifest caching works: if `manifest/{DATE_FOLDER}.json` exists it is used; otherwise a single non-recursive `list_repo_tree` call is made and cached.
- Deterministic shard assignment is consistent: same `rel_path` always maps to the same shard for a fixed `SHARD_TOTAL`.
- Dedup integration via `lib/dedup.py` prevents duplicate writes (md5 store checked before emitting records).
- HF CDN-bypass downloads occur without Authorization header and fall back to HF API if needed; no recursive API calls per file.

## perf — axentx-perf @ 2026-05-03T04:00:42.380293Z

{"verdict": "OK", "findings": [{"severity": "med", "class": "unbounded-query", "detail": "Manifest-first avoids per-file recursion, but list_repo_tree may return unbounded tree size for large repos; no pagination or size cap mentioned. Could cause OOM or latency spikes at scale.", "mitigation": "Add pagination or max-tree-size limit; stream tree entries and shard on the fly without full materialization."}, {"severity": "low", "class": "memory-leak", "detail": "Manifest caching and dedup md5 store may grow unbounded across shards/runs if not bounded or pruned.", "mitigation": "Bound cache TTL and dedup store size; use LRU or time-partitioned cleanup."}, {"severity": "low", "class": "sync-in-async", "detail": "HF CDN-bypass fallback to HF API may introduce blocking I/O if not async; could stall shard processing.", "mitigation": "Ensure fully async HTTP client with timeouts and connection pooling."}], "summary": "Manifest-first, deterministic sharding, dedup, and CDN-bypass are performance-positive. Main risk is unbounded list_repo_tree payload; bound or stream it. Otherwise safe to proceed."}

## qa — perf @ 2026-05-03T04:00:42.380347Z

{"verdict": "OK", "findings": [{"severity": "med", "class": "unbounded-query", "detail": "Manifest-first avoids per-file recursion, but list_repo_tree may return unbounded tree size for large repos; no pagination or size cap mentioned. Could cause OOM or latency spikes at scale.", "mitigation": "Add pagination or max-tree-size limit; stream tree entries and shard on the fly without full materialization."}, {"severity": "low", "class": "memory-leak", "detail": "Manifest caching and dedup md5 store may grow unbounded across shards/runs if not bounded or pruned.", "mitigation": "Bound cache TTL and dedup store size; use LRU or time-partitioned cleanup."}, {"severity": "low", "class": "sync-in-async", "detail": "HF CDN-bypass fallback to HF API may introduce blocking I/O if not async; could stall shard processing.", "mitigation": "Ensure fully async HTTP client with timeouts and connection pooling."}], "summary": "Manifest-first, deterministic sharding, dedup, and CDN-bypass are performance-positive. Main risk is unbounded list_repo_tree payload; bound or stream it. Otherwise safe to proceed."}
