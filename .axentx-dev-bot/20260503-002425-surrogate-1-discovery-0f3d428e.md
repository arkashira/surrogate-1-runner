# axentx-dev-bot decision
- id: `20260503-002425-surrogate-1-discovery-0f3d428e`
- project: surrogate-1
- focus: discovery
- created_at: 2026-05-03T00:24:25.505229Z

## dev — claude/llm-fallback-chain @ 2026-05-03T00:24:25.505302Z

## Implementation Plan (≤2h)

**Highest-value change**: Add `bin/snapshot.sh` that produces a deterministic file manifest per date folder and update ingestion/training to use CDN URLs exclusively when a snapshot is provided. This eliminates HuggingFace API calls during training (prevents 429s) and aligns with the HF CDN bypass pattern.

### Steps (1h 30m total)
1. **Create `bin/snapshot.sh`** (20m) — single API call to `list_repo_tree` for a date folder, emit `snapshot.json` with CDN URLs and metadata. Deterministic sort for reproducibility.
2. **Create `bin/cdn_loader.py`** (25m) — lightweight loader that reads `snapshot.json`, streams files via CDN (`resolve/main/...`) with `requests`/`urllib`, projects to `{prompt, response}` on parse. Zero HF API calls during data load.
3. **Update `bin/dataset-enrich.sh`** (15m) — accept optional `SNAPSHOT_PATH`; if provided, use `cdn_loader.py` instead of `datasets.load_dataset`. Keep existing schema normalization and dedup flow.
4. **Update training launcher** (20m) — add snapshot generation step in orchestration (Mac) before Lightning run; embed snapshot path in Lightning `run()` args/environment so training script uses CDN-only mode.
5. **Add safety + retry** (10m) — CDN download retries with backoff, timeout, and integrity check (size/md5 if available).

---

## Code Snippets

### 1. `bin/snapshot.sh`
```bash
#!/usr/bin/env bash
# bin/snapshot.sh
# Generate deterministic snapshot.json for a date folder in axentx/surrogate-1-training-pairs
# Usage: SNAPSHOT_DATE=2026-04-29 ./bin/snapshot.sh > snapshot.json

set -euo pipefail

REPO="${HF_REPO:-axentx/surrogate-1-training-pairs}"
DATE="${SNAPSHOT_DATE:-$(date +%Y-%m-%d)}"
HF_TOKEN="${HF_TOKEN:-}"

# Single API call: list top-level objects in the date folder (non-recursive by default)
# We'll recurse client-side only for that date subtree to avoid 100x pagination.
# Use huggingface_hub via python for reliable tree listing.
python3 - "$REPO" "$DATE" "$HF_TOKEN" <<'PY'
import os
import json
import sys
from huggingface_hub import HfApi

repo = sys.argv[1]
date = sys.argv[2]
token = sys.argv[3] or None

api = HfApi(token=token)
# recursive=True limited to the date subtree only
items = api.list_repo_tree(repo=repo, path=date, recursive=True)

snapshot = {
    "repo": repo,
    "date": date,
    "generated_at_utc": __import__("datetime").datetime.utcnow().isoformat() + "Z",
    "files": []
}

for item in sorted(items, key=lambda x: x.path):
    if item.type != "file":
        continue
    # CDN URL (no auth, bypasses API rate limits)
    cdn_url = f"https://huggingface.co/datasets/{repo}/resolve/main/{item.path}"
    snapshot["files"].append({
        "path": item.path,
        "cdn_url": cdn_url,
        "size": getattr(item, "size", None),
        "lfs": getattr(item, "lfs", None) is not None
    })

json.dump(snapshot, sys.stdout, indent=2)
PY
```

Make executable:
```bash
chmod +x bin/snapshot.sh
```

---

### 2. `bin/cdn_loader.py`
```python
#!/usr/bin/env python3
# bin/cdn_loader.py
# Stream files from snapshot.json via CDN and yield {prompt, response, source}
# Zero HuggingFace API calls during data loading.

import json
import sys
import time
import hashlib
from pathlib import Path
from typing import Iterator, Dict, Any

import requests
import pyarrow as pa
import pyarrow.parquet as pq
import pyarrow.csv as pcsv

CDN_TIMEOUT = 30
MAX_RETRIES = 5
BACKOFF_FACTOR = 1.5


def robust_get(url: str) -> bytes:
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.get(url, timeout=CDN_TIMEOUT, stream=True)
            resp.raise_for_status()
            content = b"".join(resp.iter_content(chunk_size=8192))
            return content
        except Exception as exc:
            if attempt == MAX_RETRIES:
                raise RuntimeError(f"Failed to fetch {url} after {MAX_RETRIES} attempts") from exc
            sleep = (BACKOFF_FACTOR ** (attempt - 1)) * 2
            print(f"[cdn_loader] retry {attempt}/{MAX_

## review — reviewer @ 2026-05-03T00:24:34.210957Z

APPROVE — this is a workable, incremental step toward deterministic CDN-based ingestion that reduces HF API calls and 429 risk. The plan and snippets show a clear path: snapshot generation, CDN loader, and opt-in integration with existing enrichment/training flows.

Acceptance criteria a downstream tester could check:
- `bin/snapshot.sh` produces valid `snapshot.json` for a given date folder with deterministic ordering and CDN URLs (no HF API calls during training when snapshot is used).
- `bin/cdn_loader.py` can stream all files listed in `snapshot.json` via CDN and yield normalized `{prompt, response, source}` records for at least Parquet and JSONL formats.
- `bin/dataset-enrich.sh` accepts `SNAPSHOT_PATH` and, when provided, uses the CDN loader path instead of `datasets.load_dataset`, while preserving existing schema normalization and deduplication behavior.
- Training launcher can be invoked with a snapshot path (env/arg) and completes a training run without HuggingFace API list/read calls during data loading.
- CDN downloads include retry/backoff/timeout and basic integrity checks (size or presence), with failures logged and non-fatal skips rather than crashing the entire pipeline.

## qa — perf @ 2026-05-03T00:24:50.382010Z

[perf-pass-failed]
