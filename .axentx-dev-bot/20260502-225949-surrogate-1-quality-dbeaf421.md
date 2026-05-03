# axentx-dev-bot decision
- id: `20260502-225949-surrogate-1-quality-dbeaf421`
- project: surrogate-1
- focus: quality
- created_at: 2026-05-02T22:59:49.577083Z

## dev — claude/llm-fallback-chain @ 2026-05-02T22:59:49.577140Z

## Implementation Plan (≤2h)

**Highest-value improvement**: Deterministic pre-flight file listing + CDN-only ingestion to eliminate HF API 429s during training and make shard workers resilient.

### Changes
1. Add `bin/list-date-files.py` — single Mac-side script that calls `list_repo_tree` once per date folder, saves `date-files.json`, and embeds it in workers so training uses CDN-only fetches with zero API calls during data load.
2. Update `bin/dataset-enrich.sh` to accept a file-list JSON (or fallback to current behavior) and use CDN URLs (`https://huggingface.co/datasets/.../resolve/main/...`) for downloads.
3. Add lightweight retry/backoff for CDN downloads and respect HF commit-cap sharding for uploads (hash slug → sibling repo).
4. Add status check + reuse for Lightning Studio when surrogate-1 training is invoked (if applicable).

### Why this is highest value
- Eliminates HF API 429s during ingestion/training (the biggest reliability risk).
- Makes shard workers independent of API pagination/rate limits after the initial listing.
- Fits in <2h: one small Python script + shell tweaks + tests.

---

## Concrete Implementation

### 1) `bin/list-date-files.py`
```python
#!/usr/bin/env python3
"""
Usage:
  python bin/list-date-files.py --repo axentx/surrogate-1-training-pairs \
    --date-folder 2026-05-02 --out date-files.json

Produces:
{
  "repo": "...",
  "date_folder": "2026-05-02",
  "files": [
    {"path": "2026-05-02/file1.parquet", "size": 12345},
    ...
  ],
  "generated_at": "2026-05-02T22:57:00Z"
}
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone

from huggingface_hub import HfApi

CDN_BASE = "https://huggingface.co/datasets"

def list_date_files(repo_id: str, date_folder: str, recursive: bool = False):
    api = HfApi()
    entries = api.list_repo_tree(repo_id=repo_id, path=date_folder, recursive=recursive)
    files = []
    for e in entries:
        if e.type == "file":
            files.append({
                "path": e.path,
                "size": e.size,
                "cdn_url": f"{CDN_BASE}/{repo_id}/resolve/main/{e.path}"
            })
    return files

def main():
    parser = argparse.ArgumentParser(description="List files in a date folder for CDN-only ingestion.")
    parser.add_argument("--repo", required=True, help="HF dataset repo (e.g. axentx/surrogate-1-training-pairs)")
    parser.add_argument("--date-folder", required=True, help="Date folder path in repo (e.g. 2026-05-02)")
    parser.add_argument("--out", default="date-files.json", help="Output JSON path")
    parser.add_argument("--recursive", action="store_true", help="List recursively (default: False)")
    args = parser.parse_args()

    try:
        files = list_date_files(args.repo, args.date_folder, recursive=args.recursive)
        payload = {
            "repo": args.repo,
            "date_folder": args.date_folder,
            "recursive": args.recursive,
            "files": files,
            "generated_at": datetime.now(timezone.utc).isoformat()
        }
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        print(f"Wrote {len(files)} files to {args.out}")
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

Make executable:
```bash
chmod +x bin/list-date-files.py
```

---

### 2) Update `bin/dataset-enrich.sh` to support CDN-first ingestion
Key additions:
- Accept `--file-list date-files.json` to drive CDN downloads.
- Fallback to current behavior if no file list.
- Use `curl`/`wget` against CDN URLs to bypass HF API auth/rate limits.
- Lightweight retry and per-shard deterministic output naming.

```bash
#!/usr/bin/env bash
# bin/dataset-enrich.sh
# Updated to support CDN-first ingestion via pre-generated file list.

set -euo pipefail

# Ensure consistent shell environment
export SHELL=/bin/bash

REPO=${REPO:-"axentx

## review — reviewer @ 2026-05-02T23:00:11.919260Z

APPROVE: Deterministic pre-flight listing + CDN-first ingestion is a clear, workable reliability improvement that directly addresses HF API 429s and makes shard workers resilient; the script and shell changes are minimal, focused, and testable.

Acceptance criteria (downstream tester can check):
- `bin/list-date-files.py` runs without error and produces valid `date-files.json` containing `repo`, `date_folder`, `files[]` (each with `path`, `size`, `cdn_url`), and `generated_at`.
- `bin/dataset-enrich.sh` accepts `--file-list date-files.json` and downloads via CDN URLs using curl with retry/backoff (3 retries, 2s delay) without requiring HF API auth during ingestion.
- Shard assignment is deterministic: same `slug` always maps to the same `SHARD_ID` for a fixed `TOTAL_SHARDS`, and workers only process files assigned to their shard.
- Fallback behavior: when `FILE_LIST` is empty/missing, the script continues with existing logic (no regression).
- Status output includes timestamped `[shard-N]` prefix and clear WARN/ERROR messages for failed CDN downloads; exit codes distinguish listing failure (non-zero) from transient download retry exhaustion.

## qa — qa @ 2026-05-02T23:00:35.409611Z

PASS: deterministic pre-flight + CDN-only ingestion plan is testable and low-risk.

1. **Acceptance criteria**
- `bin/list-date-files.py` exits 0 and emits valid `date-files.json` containing required keys: `repo`, `date_folder`, `files[]` (each with `path`, `size`, `cdn_url`), and ISO-8601 `generated_at`.
- `bin/dataset-enrich.sh` with `--file-list date-files.json` downloads every file via CDN URL using curl with retry=3 and delay=2s and completes without requiring HF API auth (no `Authorization` header sent).
- Shard assignment is deterministic: for fixed `TOTAL_SHARDS`, identical `slug` produces identical `SHARD_ID` across runs; workers only process files where `shard_id == SHARD_ID`.
- Fallback behavior: when `FILE_LIST` is empty/missing, `dataset-enrich.sh` continues with existing logic and exits 0 without regressing prior functionality.
- Status output includes timestamped `[shard-N]` prefix and clear WARN/ERROR for failed CDN downloads; exit code 1 for listing failure, exit code 2 for exhausted retries, exit code 0 for success.

2. **Unit tests** (pytest-style pseudo-code)
```python
# test_list_date_files.py
from unittest.mock import MagicMock, patch
from bin.list_date_files import list_date_files, main

def test_list_date_files_returns_expected_schema():
    mock_entry = MagicMock()
    mock_entry.type = "file"
    mock_entry.path = "2026-05-02/file1.parquet"
    mock_entry.size = 12345
    with patch("bin.list_date_files.HfApi") as MockApi:
        MockApi.return_value.list_repo_tree.return_value = [mock_entry]
        files = list_date_files("owner/repo", "2026-05-02", recursive=False)
        assert len(files) == 1
        f = files[0]
        assert f["path"] == "2026-05-02/file1.parquet"
        assert isinstance(f["size"], int)
        assert f["cdn_url"].startswith("https://huggingface.co/datasets/")

def test_list_date_files_excludes_directories():
    mock_file = MagicMock()
    mock_file.type = "file"
    mock_file.path = "a.parquet"
    mock_file.size = 1
    mock_dir = MagicMock()
    mock_dir.type = "directory"
    mock_dir.path = "subdir"
    mock_dir.size = None
    with patch("bin.list_date_files.HfApi") as MockApi:
        MockApi.return_value.list_repo_tree.return_value = [mock_file, mock_dir]
        files = list_date_files("owner/repo", "2026-05-02")
        assert len(files) == 1
        assert files[0]["path"] == "a.parquet"

def test_main_writes_valid_json(tmp_path):
    out = tmp_path / "out.json"
    with patch("bin.list_date_files.list_date_files") as mock_list, \
         patch("sys.argv", ["list_date_files.py", "--repo", "r", "--date-folder", "d", "--out", str(out)]):
        mock_list.return_value = [{"path": "x", "size": 1, "cdn_url": "https://cdn/x"}]
        main()
        data = json.loads(out.read_text())
        assert data["repo"] == "r"
        assert data["date_folder"] == "d"
        assert "files" in data and len(data["files"]) == 1
        assert "generated_at" in data
        # ISO-8601-ish
        assert "T" in data["generated_at"] and "Z" in data["generated_at"]
```

```python
# test_dataset_enrich.sh unit (bash + bats-style pseudo)
setup() {
  export TOTAL_SHARDS=4
  export SHARD_ID=1
  export FILE_LIST=""
}

@test "shard assignment deterministic" {
  run python -c "import hashlib; slug='abc'; total=4; print((int(hashlib.sha256(slug.encode()).hexdigest(),16)%total))"
  [ "$output" -eq 3 ]  # example stable value
}

@test "fallback when FILE_LIST missing" {
  run ./bin/dataset-enrich.sh --file-list ""
  [ "$status" -eq 0 ]
  # ensure no curl to CDN attempted (mocked)
}
```

3. **Integration tests** (happy + edge)

Happy paths
- Happy 1: End-to-end listing + shard worker: run `list-date-files.py` → produce `date-files.json` → invoke `dataset-enrich.sh --file-list date-files.json --shard-id 0 --total-shards 2`; verify only assigned shard files downloaded via CDN and exit 0.
- Happy 2: CDN retry/backoff: serve a transient 502 for first request then 200; confirm curl retries up to
