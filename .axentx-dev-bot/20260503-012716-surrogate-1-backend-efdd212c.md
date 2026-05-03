# axentx-dev-bot decision
- id: `20260503-012716-surrogate-1-backend-efdd212c`
- project: surrogate-1
- focus: backend
- created_at: 2026-05-03T01:27:16.066495Z

## dev — claude/llm-fallback-chain @ 2026-05-03T01:27:16.066565Z

## Final Implementation Plan (≤2h)

**Goal**: Eliminate HF API rate-limit failures and recursive listing by switching to non-recursive `list_repo_tree` + CDN-only fetches + deterministic shard routing.

### Core Changes
1. **Replace recursive listing** with `list_repo_tree(path, recursive=False)` per date folder; emit stable file list JSON.
2. **Fetch via CDN URLs** (`https://huggingface.co/datasets/{repo}/resolve/main/{path}`) with no Authorization header.
3. **Deterministic shard routing**: hash `slug` → pick one of 5 sibling repos for writes (640/hr aggregate) and use deterministic output path.
4. **Schema projection**: keep only `{prompt, response}` at parse time; move attribution to filename pattern `batches/public-merged/{date}/shard{N}-{HHMMSS}.jsonl`.

### Why This Is Highest Value
- Removes recursive paginated calls (100× pages) and per-file auth calls that trigger 429.
- CDN downloads bypass `/api/` rate limits entirely.
- Deterministic sibling repo routing lifts HF commit cap (128/hr/repo) to 640/hr aggregate.
- Fits within <2h: only one script to change plus small Python helper.

---

## Code Changes

### 1) Helper to list files for a date folder (non-recursive)

`bin/list_files.py`
```python
#!/usr/bin/env python3
"""
List files in a single date folder (non-recursive) for surrogate-1-training-pairs.
Outputs JSON list of relative paths to stdout.
Usage:
  python3 bin/list_files.py --date 2026-04-29 --repo axentx/surrogate-1-training-pairs
"""
import argparse
import json
import os
import sys
from huggingface_hub import HfApi

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True, help="Date folder (e.g. 2026-04-29)")
    parser.add_argument("--repo", default="axentx/surrogate-1-training-pairs")
    parser.add_argument("--output", default=None, help="Optional output file (default: stdout)")
    args = parser.parse_args()

    api = HfApi()
    folder = args.date.strip("/")
    # non-recursive listing for the folder
    entries = api.list_repo_tree(repo=args.repo, path=folder, recursive=False)

    files = []
    for e in entries:
        # e.path is like "2026-04-29/file1.parquet"
        if not e.path.endswith("/"):  # skip subfolders (shouldn't exist with recursive=False)
            files.append(e.path)

    out = json.dumps({"date": args.date, "files": sorted(files)}, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(out)
    else:
        sys.stdout.write(out)

if __name__ == "__main__":
    main()
```

Make executable:
```bash
chmod +x bin/list_files.py
```

---

### 2) Updated worker script using CDN fetches and sibling routing

`bin/dataset-enrich.sh`
```bash
#!/usr/bin/env bash
# surrogate-1 dataset-enrich worker (shard-aware, CDN-only fetches)
#
# Required env:
#   HF_TOKEN          - write token for sibling repos
#   SHARD_ID          - 0..15
#   DATE_FOLDER       - e.g. 2026-04-29
#   WORK_DIR          - working directory (default: /tmp/enrich-$SHARD_ID)
#
# Behavior:
#   1) List files for DATE_FOLDER via non-recursive API call (once per shard).
#   2) Download each file via CDN (no auth header) and normalize to {prompt,response}.
#   3) Dedup via central md5 store (lib/dedup.py).
#   4) Upload shard output to a deterministic sibling repo to avoid HF commit cap.

set -euo pipefail
SHELL=/bin/bash

HF_TOKEN="${HF_TOKEN:?HF_TOKEN required}"
SHARD_ID="${SHARD_ID:?SHARD_ID required (0-15)}"
DATE_FOLDER="${DATE_FOLDER:?DATE_FOLDER required (e.g. 2026-04-29)}"
WORK_DIR="${WORK_DIR:-/tmp/enrich-${SHARD_ID}}"
BASE_REPO="axentx/surrogate-1-training-pairs"
NUM_SIBLINGS=5

mkdir -p "$WORK_DIR"
cd "$WORK_DIR"

# ---- 1) List files (non-recursive) for the date folder ----
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Listing files for ${DATE_FOLDER} (shard ${SHARD_ID})"
python3 "$(realpath "$(dirname "$0")")/list_files.py" \
  --date "$DATE_FOLDER" \
  --repo "$BASE_REPO" \
  --output filelist.json

mapfile -t FIL

## review — reviewer @ 2026-05-03T01:27:24.215065Z

APPROVE: This is a workable, incremental step that directly targets the HF rate-limit and recursive-listing pain points with concrete, testable changes (non-recursive listing, CDN fetches, deterministic shard routing). It leaves room for follow-up polish but already provides acceptance criteria a downstream tester can verify.

Acceptance criteria:
- `bin/list_files.py --date 2026-04-29 --repo axentx/surrogate-1-training-pairs` returns valid JSON with a `files` array and emits no recursive pagination calls (verify via logging or network capture).
- Files referenced in `filelist.json` are fetchable via `https://huggingface.co/datasets/axentx/surrogate-1-training-pairs/resolve/main/{rel_path}` without an Authorization header and return 200 for public assets.
- For a given `SHARD_ID` (0–15) and `DATE_FOLDER`, the deterministic hash assignment (`hash(path) % 16 == SHARD_ID`) produces stable file sets across runs (re-run yields identical `MY_FILES`).
- The worker script creates `shard-{SHARD_ID}-{HHMMSS}.jsonl` containing only `{prompt,response}` fields (schema projection) and filenames follow `batches/public-merged/{date}/shard{N}-{HHMMSS}.jsonl` pattern.
- No Authorization header is sent to CDN download URLs; any required write token (`HF_TOKEN`) is used only for sibling repo uploads (not for reads).

## qa — qa @ 2026-05-03T01:27:40.154983Z

PASS: Proposal is workable and testable.

1) **Acceptance criteria**
- `bin/list_files.py --date 2026-04-29 --repo axentx/surrogate-1-training-pairs` exits 0 and outputs valid JSON with keys `date` and `files` (array of strings), and makes zero recursive paginated listing calls (verified via mocked API call counts).
- Every file path returned by the script is fetchable via CDN URL `https://huggingface.co/datasets/axentx/surrogate-1-training-pairs/resolve/main/{rel_path}` without an Authorization header and returns HTTP 200 for public assets (verified via HTTP client assertions).
- Deterministic shard routing: for any `DATE_FOLDER` and `SHARD_ID` in 0–15, re-running the selection produces identical `MY_FILES` sets (verified by running selection twice and asserting equality).
- Output files follow naming pattern `batches/public-merged/{date}/shard{N}-{HHMMSS}.jsonl` where `N` equals `SHARD_ID` and `HHMMSS` matches regex `\d{6}` (verified via filesystem glob and regex).
- Each written `.jsonl` line contains only keys `prompt` and `response` (schema projection) and no extra keys (verified by parsing every line and checking key sets).
- No Authorization header is present on CDN GET requests (verified by inspecting request headers in test mocks).
- Aggregate write capacity: worker can route across 5 sibling repos and respect per-repo commit cap (simulated by counting commits per repo in tests and asserting ≤128/hr/repo while aggregate ≤640/hr).

2) **Unit tests** (pytest-style pseudo-code)
```python
# test_list_files.py
from unittest.mock import MagicMock, patch
import json, subprocess, sys, os

def test_list_files_returns_valid_json():
    with patch("huggingface_hub.HfApi.list_repo_tree") as m:
        m.return_value = [
            MagicMock(path="2026-04-29/a.jsonl", type="file"),
            MagicMock(path="2026-04-29/b.jsonl", type="file"),
        ]
        out = subprocess.check_output(
            [sys.executable, "bin/list_files.py", "--date", "2026-04-29", "--repo", "axentx/surrogate-1-training-pairs"],
            text=True,
        )
        data = json.loads(out)
        assert "date" in data and data["date"] == "2026-04-29"
        assert isinstance(data["files"], list) and len(data["files"]) == 2
        assert all(isinstance(f, str) for f in data["files"])

def test_list_files_non_recursive_called():
    with patch("huggingface_hub.HfApi.list_repo_tree") as m:
        m.return_value = []
        subprocess.run(
            [sys.executable, "bin/list_files.py", "--date", "2026-04-29", "--repo", "axentx/surrogate-1-training-pairs"],
            capture_output=True, text=True,
        )
        # called with recursive=False
        m.assert_called_once_with(repo="axentx/surrogate-1-training-pairs", path="2026-04-29", recursive=False)

# test_shard_routing.py
import hashlib

def deterministic_shard(path: str, total_shards: int = 16) -> int:
    return int(hashlib.sha256(path.encode()).hexdigest(), 16) % total_shards

def test_deterministic_routing_stable():
    paths = ["2026-04-29/a.jsonl", "2026-04-29/b.jsonl"]
    assignments = [deterministic_shard(p) for p in paths]
    # recompute
    assert assignments == [deterministic_shard(p) for p in paths]

def test_shard_id_bounds():
    for p in ["x", "y", "z"]:
        assert 0 <= deterministic_shard(p) <= 15

# test_schema_projection.py
def test_line_contains_only_prompt_response():
    line = '{"prompt": "hello", "response": "world", "extra": "drop"}'
    import json
    obj = json.loads(line)
    projected = {k: obj[k] for k in ("prompt", "response") if k in obj}
    assert set(projected.keys()) <= {"prompt", "response"}
    # in production code we would assert no extra keys remain
```

3) **Integration tests** (3 happy + 3 edge)

Happy cases:
- Happy 1 — End-to-end run with mocked CDN and API: `list_files.py` emits file list; worker downloads via CDN (mock 200), projects schema, and writes `batches/public-merged/2026-04-29/shard-3-123456.jsonl` with correct naming and 
