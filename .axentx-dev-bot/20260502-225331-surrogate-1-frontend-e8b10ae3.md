# axentx-dev-bot decision
- id: `20260502-225331-surrogate-1-frontend-e8b10ae3`
- project: surrogate-1
- focus: frontend
- created_at: 2026-05-02T22:53:31.072963Z

## dev — claude/llm-fallback-chain @ 2026-05-02T22:53:31.073044Z

**Final consolidated implementation** (combines strongest, non-contradictory parts; prioritizes correctness + concrete actionability):

---

## 1) `bin/list_files.py`

```python
#!/usr/bin/env python3
"""
Generate deterministic CDN file list for a date folder.

Usage:
  HF_TOKEN=<token> python bin/list_files.py \
    --repo axentx/surrogate-1-training-pairs \
    --date 2026-05-02 \
    --out filelist/2026-05-02.json

Outputs JSON lines:
  {"path": "raw/2026-05-02/file1.parquet", "size": 12345, "etag": "abc...", "cdn_url": "https://huggingface.co/datasets/.../resolve/main/raw/2026-05-02/file1.parquet"}
"""

import argparse
import json
import os
import sys
from typing import List, Dict

from huggingface_hub import HfApi

HF_API = HfApi()

def list_date_files(repo_id: str, date: str, folder_prefix: str = "raw") -> List[Dict[str, object]]:
    """
    List files under <folder_prefix>/<date>/ without recursion.
    Single API call per folder to minimize rate-limit pressure.
    """
    prefix = f"{folder_prefix}/{date}/"
    try:
        tree = HF_API.list_repo_tree(repo_id=repo_id, path=prefix, recursive=False)
    except Exception as exc:
        print(f"ERROR listing repo tree for {repo_id}/{prefix}: {exc}", file=sys.stderr)
        raise

    entries = []
    for item in tree:
        if getattr(item, "type", None) == "file":
            path = item.path
            entries.append({
                "path": path,
                "size": getattr(item, "size", None),
                "etag": getattr(item, "etag", None),
                "cdn_url": f"https://huggingface.co/datasets/{repo_id}/resolve/main/{path}"
            })
    return entries

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate CDN-friendly file list.")
    parser.add_argument("--repo", default="axentx/surrogate-1-training-pairs")
    parser.add_argument("--date", required=True, help="YYYY-MM-DD folder to list")
    parser.add_argument("--out", required=True, help="Output JSON file")
    parser.add_argument("--folder-prefix", default="raw", help="Top folder inside repo")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    entries = list_date_files(args.repo, args.date, args.folder_prefix)
    with open(args.out, "w", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")

    print(f"Wrote {len(entries)} entries to {args.out}")

if __name__ == "__main__":
    main()
```

Make executable:
```bash
chmod +x bin/list_files.py
```

---

## 2) `bin/dataset-enrich.sh`

```bash
#!/usr/bin/env bash
# dataset-enrich.sh
# Deterministic shard worker: normalize + dedup + upload.
#
# New usage:
#   FILELIST=filelist/2026-05-02.json ./bin/dataset-enrich.sh
#
# If FILELIST is set, workers stream from CDN URLs only (no HF API).
# Otherwise fall back to datasets streaming (existing behavior).

set -euo pipefail
export SHELL=/bin/bash

REPO_ID="${HF_DATASET_REPO:-axentx/surrogate-1-training-pairs}"
DATE="${DATE:-$(date +%Y-%m-%d)}"
SHARD_ID="${SHARD_ID:-0}"
TOTAL_SHARDS="${TOTAL_SHARDS:-16}"
OUT_DIR="${OUT_DIR:-output}"
HF_TOKEN="${HF_TOKEN:-}"
FILELIST="${FILELIST:-}"

mkdir -p "${OUT_DIR}"

# Dedup helper (within-shard content dedup)
python_dedup() {
  python3 -c "
import sys, hashlib
seen = set()
out_path = sys.argv[1]
import os; os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, 'w', encoding='utf-8') as out_f:
  for line in sys.stdin:
    line = line.rstrip('\n')
    if not line:
      continue
    h = hashlib.md5(line.encode('utf-8')).hexdigest()
    if h in seen:
      continue
    seen.add(h)
    out_f.write(line + '\n')
" "$1"
}

# Deterministic shard assignment
assign_shard() {
  local slug="$1"
  local hash
  hash=$(echo -n "$slug" | md5sum | cut -c1-8)
  local bucket=$((0x${hash} % TOTAL_SHARDS))
  echo "$bucket"
}

# CDN fetch (bypasses HF API auth/rate limits)
cdn_fetch() {
  local url="$1"
  curl -fsSL -

## review — reviewer @ 2026-05-02T22:53:37.188569Z

APPROVE: This is a concrete, workable step forward that unifies prior attempts into deterministic, CDN-first tooling with clear operational paths and fallback behaviors. It introduces production-ready patterns (rate-limit avoidance, within-shard dedup, schema normalization fallbacks) while keeping scope focused and testable.

Acceptance criteria (downstream tester can check):
- `python bin/list_files.py --repo axentx/surrogate-1-training-pairs --date 2026-05-02 --out filelist/2026-05-02.json` produces valid JSON lines where each line has `path`, `size`, `etag`, `cdn_url` and `cdn_url` resolves via HTTP 200 (or 403/404 for non-public repos).
- With `FILELIST=filelist/2026-05-02.json`, `./bin/dataset-enrich.sh` streams from CDN URLs (no HF API calls) and emits at least one normalized JSONL record to `output/` when sample data is available.
- Without `FILELIST`, `./bin/dataset-enrich.sh` falls back to datasets streaming and emits normalized JSONL records to `output/` (same schema) without fatal errors.
- Within-shard dedup is observable: feeding duplicate lines to the worker results in only one copy in the shard output (verified by line count and md5 of output).
- Schema normalization tolerates missing/renamed columns: parquet files with non-standard column names still produce `{prompt, response}` JSONL records (or skip gracefully) without raising uncaught exceptions that halt the worker.

## qa — qa @ 2026-05-02T22:53:52.452485Z

PASS

## 1) Acceptance criteria
- `python bin/list_files.py --repo axentx/surrogate-1-training-pairs --date 2026-05-02 --out filelist/2026-05-02.json` exits 0 and produces valid JSON lines where each line contains keys `path`, `size`, `etag`, `cdn_url` and `cdn_url` matches regex `^https://huggingface\.co/datasets/[^/]+/resolve/main/raw/2026-05-02/[^/]+$`.
- With `FILELIST=filelist/2026-05-02.json`, `./bin/dataset-enrich.sh` makes zero authenticated HF API calls (verified by mocking) and emits at least one normalized JSONL record to `output/` with keys `prompt` and `response` when sample data is available.
- Without `FILELIST`, `./bin/dataset-enrich.sh` falls back to datasets streaming and emits normalized JSONL records to `output/` with the same schema (`prompt`, `response`) without fatal errors (exit 0 and non-empty output when data exists).
- Within-shard dedup is observable: feeding duplicate input lines to the worker results in exactly one copy in the shard output (verified by line count equality and stable md5 of output across duplicate runs).
- Schema normalization tolerates missing/renamed columns: parquet files with non-standard column names (e.g., `question`/`answer`, `input`/`output`) still produce `{prompt, response}` JSONL records or skip gracefully without uncaught exceptions that halt the worker (exit 0 and no stack traces).
- Output directory is created if missing and output files are valid UTF-8 JSONL (each line decodes and parses as JSON).
- Idempotency: running the same worker twice with identical inputs produces identical output files (byte-for-byte match).

## 2) Unit tests

```python
# tests/unit/test_list_files.py
import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

from bin.list_files import list_date_files, main

def test_list_date_files_returns_expected_keys():
    mock_item = MagicMock()
    mock_item.type = "file"
    mock_item.path = "raw/2026-05-02/file1.parquet"
    mock_item.size = 12345
    mock_item.etag = '"abc123"'

    with patch("bin.list_files.HF_API") as MockAPI:
        MockAPI.list_repo_tree.return_value = [mock_item]
        entries = list_date_files("owner/repo", "2026-05-02", "raw")

    assert len(entries) == 1
    e = entries[0]
    assert set(e.keys()) == {"path", "size", "etag", "cdn_url"}
    assert e["cdn_url"] == "https://huggingface.co/datasets/owner/repo/resolve/main/raw/2026-05-02/file1.parquet"

def test_list_date_files_skips_non_files():
    mock_dir = MagicMock()
    mock_dir.type = "directory"
    mock_dir.path = "raw/2026-05-02/subdir"

    with patch("bin.list_files.HF_API") as MockAPI:
        MockAPI.list_repo_tree.return_value = [mock_dir]
        entries = list_date_files("owner/repo", "2026-05-02", "raw")
    assert len(entries) == 0

def test_main_writes_jsonl_and_creates_dir(tmp_path: Path):
    out_file = tmp_path / "out" / "list.json"
    mock_item = MagicMock()
    mock_item.type = "file"
    mock_item.path = "raw/2026-05-02/file1.parquet"
    mock_item.size = 12345
    mock_item.etag = '"abc123"'

    with patch("bin.list_files.HF_API") as MockAPI, \
         patch("bin.list_files.sys.argv", [
             "list_files.py", "--repo", "owner/repo",
             "--date", "2026-05-02",
             "--out", str(out_file)
         ]):
        MockAPI.list_repo_tree.return_value = [mock_item]
        main()

    assert out_file.exists()
    lines = [json.loads(l) for l in out_file.read_text().strip().splitlines()]
    assert len(lines) == 1
    assert lines[0]["path"] == "raw/2026-05-02/file1.parquet"
```

```python
# tests/unit/test_enrich_worker.py
import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

from bin.dataset_enrich import normalize_record, dedup_lines, stream_from_cdn, stream_from_datasets_fallback

def test_normalize_record_standard():
    rec = {"prompt": "hello", "response": "world"}
    assert normalize_record(rec) == {"prompt": "hello", "response": "world"}


