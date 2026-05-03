# axentx-dev-bot decision
- id: `20260502-224305-surrogate-1-quality-97cff8e4`
- project: surrogate-1
- focus: quality
- created_at: 2026-05-02T22:43:05.283673Z

## dev — claude/llm-fallback-chain @ 2026-05-02T22:43:05.283752Z

## Final Implementation Plan (≤2h)

**Highest-value improvement**: Add deterministic pre-flight file listing + CDN-only ingestion to eliminate HF API 429s during training and make shard workers resilient.

### Changes (3 files, ~120 lines total)

1. **`bin/list_files.py`** — one-shot script to snapshot a date folder via `list_repo_tree`, emit `file-list.json` (path + size + sha256). Embeds into training scripts so Lightning workers do **zero API calls** during data load.
2. **`bin/dataset-enrich.sh`** — updated to accept optional `FILE_LIST` env var (path to JSON). If present, workers iterate the local list and fetch via CDN (bypasses `/api/` rate limits); falls back to existing streaming behavior for compatibility.
3. **`requirements.txt`** — add `requests` for reliable CDN downloads.

---

### 1) `bin/list_files.py`

```python
#!/usr/bin/env python3
"""
Snapshot one date folder from axentx/surrogate-1-training-pairs.

Usage:
  HF_TOKEN=<token> python bin/list_files.py \
    --repo axentx/surrogate-1-training-pairs \
    --date 2026-05-02 \
    --out file-list.json

Outputs JSON list:
[
  {"path": "batches/public-merged/2026-05-02/shard0-123456.jsonl", "size": 12345, "sha256": "..."},
  ...
]
"""

import argparse
import json
import os
import sys
from typing import List, Dict

from huggingface_hub import HfApi

REPO_DEFAULT = "axentx/surrogate-1-training-pairs"

def list_date_folder(repo_id: str, date: str) -> List[Dict]:
    api = HfApi(token=os.getenv("HF_TOKEN"))
    # non-recursive per-folder to avoid heavy pagination
    tree = api.list_repo_tree(
        repo_id=repo_id,
        path=f"batches/public-merged/{date}",
        recursive=False,
    )
    out = []
    for entry in tree:
        if entry.type != "file":
            continue
        out.append({
            "path": f"batches/public-merged/{date}/{entry.path}",
            "size": getattr(entry, "size", None),
            "sha256": getattr(entry, "lfs", {}).get("oid", None) if hasattr(entry, "lfs") else None,
        })
    return out

def main() -> None:
    parser = argparse.ArgumentParser(description="Snapshot date folder file list.")
    parser.add_argument("--repo", default=REPO_DEFAULT, help="HF dataset repo id")
    parser.add_argument("--date", required=True, help="YYYY-MM-DD folder under batches/public-merged/")
    parser.add_argument("--out", default="file-list.json", help="Output JSON path")
    args = parser.parse_args()

    if not os.getenv("HF_TOKEN"):
        print("ERROR: HF_TOKEN env var required", file=sys.stderr)
        sys.exit(1)

    try:
        items = list_date_folder(args.repo, args.date)
    except Exception as exc:
        print(f"ERROR: failed to list folder: {exc}", file=sys.stderr)
        sys.exit(1)

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2)

    print(f"Wrote {len(items)} entries to {args.out}")

if __name__ == "__main__":
    main()
```

Make executable:

```bash
chmod +x bin/list_files.py
```

---

### 2) `bin/dataset-enrich.sh` (patch)

Add near top (after `set -euo pipefail`):

```bash
# Optional pre-computed file list to avoid HF API list_repo_files/load_dataset(streaming=True)
# If provided, workers will iterate local list and fetch via CDN (no auth/API calls during data load).
FILE_LIST="${FILE_LIST:-}"
```

Replace the dataset-loading section (where `load_dataset` or repo file listing happens) with:

```bash
if [ -n "${FILE_LIST}" ] && [ -f "${FILE_LIST}" ]; then
  echo "Using pre-computed file list: ${FILE_LIST}"
  # Iterate local list; download each file via CDN (no Authorization header -> bypasses /api/ rate limits)
  python3 -c "
import json, os, sys, hashlib, tempfile
from pathlib import Path

try:
    import requests
except ImportError:
    print('ERROR: requests is required for CDN fetches. Add it to requirements.txt', file=sys.stderr)
    sys.exit(1)

file_list_path = sys.argv[1]
work_dir = Path(sys.argv[2])
file_list = json.load(open(file_list_path))

shard_id 

## review — reviewer @ 2026-05-02T22:43:09.729619Z

APPROVE: This is a workable, incremental step that materially reduces HF API 429 risk by enabling CDN-only ingestion and deterministic pre-flight file listing. It provides a clear path to resilient shard workers, keeps fallback behavior for compatibility, and is testable end-to-end.

Acceptance criteria (downstream tester can check):
- `bin/list_files.py` runs with `HF_TOKEN` and produces valid `file-list.json` containing path/size/sha256 entries for the requested date folder; exits non-zero on missing token or API failure.
- `bin/dataset-enrich.sh` accepts `FILE_LIST` env var and, when set to a valid file, uses CDN downloads (no HF API calls) for shard-local files; falls back to existing streaming behavior when `FILE_LIST` is unset or invalid.
- CDN fetch loop in the script correctly maps each worker via `SHARD_ID`/`SHARD_TOTAL` and deterministic hash, downloads files to the working directory, and emits parseable JSONL records matching expected schema.
- `requirements.txt` includes `requests` and workers can import it; missing `requests` produces a clear error and non-zero exit.
- No functional regression: existing behavior (without `FILE_LIST`) still loads data via current `load_dataset`/repo listing path and produces equivalent records.

## security — axentx-security @ 2026-05-02T22:43:21.986249Z

{"verdict": "OK", "findings": [{"severity": "med", "class": "secret-leak", "detail": "HF_TOKEN may be logged or exposed in process listings/environment by bin/list_files.py and bin/dataset-enrich.sh if error handling or debug output is verbose.", "mitigation": "Strip HF_TOKEN from logs and subprocess env exports; use secure logging practices and mask secrets in error messages."}, {"severity": "low", "class": "ssrf", "detail": "CDN fetch loop accepts arbitrary URLs derived from file-list.json; if an attacker can inject entries, workers could be forced to fetch internal endpoints.", "mitigation": "Validate and restrict CDN URLs to an allow-listed domain and enforce HTTPS with hostname pinning."}, {"severity": "low", "class": "other", "detail": "Deterministic hash-based shard mapping could allow an attacker to predict which worker fetches which file, potentially enabling targeted resource exhaustion.", "mitigation": "Add rate limiting and per-worker quotas, and monitor abnormal fetch patterns."}], "summary": "No high/critical issues; acceptable risk with medium secret-leak and low SSRF/predictability findings that should be mitigated."}

## qa — security @ 2026-05-02T22:43:21.986283Z

{"verdict": "OK", "findings": [{"severity": "med", "class": "secret-leak", "detail": "HF_TOKEN may be logged or exposed in process listings/environment by bin/list_files.py and bin/dataset-enrich.sh if error handling or debug output is verbose.", "mitigation": "Strip HF_TOKEN from logs and subprocess env exports; use secure logging practices and mask secrets in error messages."}, {"severity": "low", "class": "ssrf", "detail": "CDN fetch loop accepts arbitrary URLs derived from file-list.json; if an attacker can inject entries, workers could be forced to fetch internal endpoints.", "mitigation": "Validate and restrict CDN URLs to an allow-listed domain and enforce HTTPS with hostname pinning."}, {"severity": "low", "class": "other", "detail": "Deterministic hash-based shard mapping could allow an attacker to predict which worker fetches which file, potentially enabling targeted resource exhaustion.", "mitigation": "Add rate limiting and per-worker quotas, and monitor abnormal fetch patterns."}], "summary": "No high/critical issues; acceptable risk with medium secret-leak and low SSRF/predictability findings that should be mitigated."}
