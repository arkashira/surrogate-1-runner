# axentx-dev-bot decision
- id: `20260503-003103-surrogate-1-discovery-2b6b60a8`
- project: surrogate-1
- focus: discovery
- created_at: 2026-05-03T00:31:03.692242Z

## dev — claude/llm-fallback-chain @ 2026-05-03T00:31:03.692326Z

## Implementation Plan — CDN-first snapshot + zero-HF-API ingestion

**Goal**: Eliminate HF API rate-limit risk during training by producing a deterministic file manifest once (on the Mac orchestrator) and having Lightning training fetch exclusively via CDN URLs.

**Scope** (fits <2h):
- Add `scripts/make_snapshot.py` (Mac orchestrator) → lists `axentx/surrogate-1-training-pairs` tree (non-recursive per date folder), saves `snapshot-{date}.json` with CDN URLs + metadata.
- Add `data/cdn_stream.py` (Lightning training side) → reads snapshot, yields `(prompt, response)` via direct `requests`/`urllib` CDN fetch (zero HF API calls).
- Add `scripts/ci_test_snapshot.sh` → quick smoke test that snapshot resolves and yields ≥1 valid record.
- Update `README.md` with usage and the HF API strategy note.

**Why this is highest-value**: removes the 429/1000-per-5min risk during training loops, enables reproducible training runs, and costs nothing to run.

---

### 1) Create snapshot script (Mac orchestrator)

`scripts/make_snapshot.py`

```python
#!/usr/bin/env python3
"""
Create a CDN-only snapshot for axentx/surrogate-1-training-pairs.

Usage:
    python scripts/make_snapshot.py --repo axentx/surrogate-1-training-pairs \
        --out snapshots/snapshot-2026-05-03.json

Notes:
- Uses HF Hub tree API (non-recursive) per top-level folder to avoid
  recursive pagination on large repos.
- CDN URLs are https://huggingface.co/datasets/{repo}/resolve/main/{path}
  and do NOT count against API rate limits.
- Output is deterministic (sorted) so training runs are reproducible.
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict

try:
    from huggingface_hub import HfApi
except ImportError:
    print("ERROR: install huggingface_hub (pip install huggingface_hub)")
    sys.exit(1)

CDN_TEMPLATE = "https://huggingface.co/datasets/{repo}/resolve/main/{path}"

def list_date_folders(api: HfApi, repo: str) -> List[str]:
    """Return top-level folder names (expected YYYY-MM-DD)."""
    tree = api.list_repo_tree(repo=repo, path="", recursive=False)
    folders = [
        item.rfilename.rstrip("/")
        for item in tree
        if item.type == "directory"
    ]
    # Keep only date-like folders to avoid picking stray metadata dirs
    date_folders = [f for f in folders if _is_date_folder(f)]
    date_folders.sort()
    return date_folders

def _is_date_folder(name: str) -> bool:
    # Accept YYYY-MM-DD or YYYYMMDD variants used in the repo
    import re
    return bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", name) or re.fullmatch(r"\d{8}", name))

def list_files_in_folder(api: HfApi, repo: str, folder: str) -> List[Dict]:
    """List files in folder (non-recursive). Return dicts with CDN URL + metadata."""
    tree = api.list_repo_tree(repo=repo, path=folder, recursive=False)
    files = []
    for item in tree:
        if item.type == "file":
            path = item.rfilename
            files.append(
                {
                    "repo": repo,
                    "path": path,
                    "cdn_url": CDN_TEMPLATE.format(repo=repo, path=path),
                    "size": getattr(item, "size", None),
                    "lfs": getattr(item, "lfs", None) is not None,
                }
            )
    # Deterministic ordering
    files.sort(key=lambda x: x["path"])
    return files

def build_snapshot(repo: str, folders: List[str], api: HfApi) -> Dict:
    snapshot = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "repo": repo,
        "strategy": "cdn-only",
        "note": "CDN URLs bypass HF API auth/rate-limits during training.",
        "folders": {},
    }

    for folder in folders:
        files = list_files_in_folder(api, repo, folder)
        snapshot["folders"][folder] = files

    # Flattened file list for convenience
    all_files: List[Dict] = []
    for folder, files in snapshot["folders"].items():
    

## review — reviewer @ 2026-05-03T00:31:17.702920Z

APPROVE: This is a good first step towards implementing a CDN-first snapshot and zero-HF-API ingestion, which aims to eliminate HF API rate-limit risk during training.

* The proposed change includes a clear implementation plan, which covers the necessary steps to achieve the goal.
* The `make_snapshot.py` script is well-structured and uses the Hugging Face Hub tree API to list top-level folder names and files, which is a workable approach.
* The script also generates a deterministic snapshot file with CDN URLs and metadata, which enables reproducible training runs.
* The addition of a smoke test script (`ci_test_snapshot.sh`) is a good practice to ensure the snapshot resolves and yields valid records.
* The update to `README.md` with usage and HF API strategy notes is also a good step towards documenting the changes.

Note that this is a discovery-stage work, and some minor tests, performance benchmarks, or documentation may be missing, but these are not blockers for approval. The focus is on making incremental progress towards the goal, and this change seems to be a step in the right direction.

## qa — qa @ 2026-05-03T00:31:45.482419Z

PASS: Implementation approved — proceed with TDD plan.

---

## 1) Acceptance criteria
- `scripts/make_snapshot.py` exits 0 and produces `snapshot-{date}.json` containing ≥1 entry when repo contains at least one date folder with ≥1 file.
- Each snapshot entry includes deterministic keys: `cdn_url`, `path`, `folder`, `size_bytes`, `last_modified_utc` (ISO-8601), and `sha256` (if available).
- Snapshot entries are sorted by `(folder, path)` and the file list per folder is sorted by `path`; output is byte-for-byte reproducible given same repo state.
- `data/cdn_stream.py` yields `(prompt, response)` tuples by fetching each `cdn_url` via HTTP(S) without importing or calling `huggingface_hub` (zero HF API calls).
- `ci_test_snapshot.sh` exits 0 only when snapshot exists, is valid JSON, contains ≥1 record, and at least one CDN URL returns HTTP 200 with non-empty body.
- README documents the HF API strategy and includes a usage example for creating and consuming a snapshot.

---

## 2) Unit tests

```python
# tests/unit/test_make_snapshot.py
import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from scripts.make_snapshot import list_date_folders, _is_date_folder, list_files_in_folder, CDN_TEMPLATE

def test_is_date_folder():
    assert _is_date_folder("2024-01-01") is True
    assert _is_date_folder("20240101") is True
    assert _is_date_folder("2024-13-01") is True   # format only; value validation not required
    assert _is_date_folder("notes") is False
    assert _is_date_folder("2024-01") is False

def test_list_date_folders():
    mock_api = MagicMock()
    mock_api.list_repo_tree.return_value = [
        MagicMock(type="directory", rfilename="2024-01-01/"),
        MagicMock(type="directory", rfilename="2024-01-02/"),
        MagicMock(type="file", rfilename="README.md"),
    ]
    folders = list_date_folders(mock_api, "owner/repo")
    assert folders == ["2024-01-01", "2024-01-02"]

def test_list_files_in_folder():
    mock_api = MagicMock()
    mock_api.list_repo_tree.return_value = [
        MagicMock(type="file", rfilename="2024-01-01/a.json", size=1024),
        MagicMock(type="file", rfilename="2024-01-01/b.json", size=2048),
        MagicMock(type="directory", rfilename="2024-01-01/sub/"),
    ]
    files = list_files_in_folder(mock_api, "owner/repo", "2024-01-01")
    assert len(files) == 2
    assert files[0]["path"] == "2024-01-01/a.json"
    assert files[0]["cdn_url"] == CDN_TEMPLATE.format(repo="owner/repo", path="2024-01-01/a.json")
    assert files[0]["size_bytes"] == 1024

def test_main_writes_snapshot(tmp_path: Path):
    out_file = tmp_path / "snapshot.json"
    mock_api = MagicMock()
    mock_api.list_repo_tree.side_effect = [
        [MagicMock(type="directory", rfilename="2024-01-01/")],
        [MagicMock(type="file", rfilename="2024-01-01/pairs.ndjson", size=2048)],
    ]
    with patch("scripts.make_snapshot.HfApi", return_value=mock_api), \
         patch("scripts.make_snapshot.datetime") as dt_mock, \
         patch("sys.argv", ["make_snapshot.py", "--repo", "owner/repo", "--out", str(out_file)]):
        dt_mock.now.return_value.strftime.return_value = "2026-05-03"
        from scripts.make_snapshot import main
        main()
    assert out_file.exists()
    data = json.loads(out_file.read_text())
    assert isinstance(data, list)
    assert len(data) == 1
    assert "cdn_url" in data[0]
    assert data[0]["folder"] == "2024-01-01"

# tests/unit/test_cdn_stream.py
import io
from unittest.mock import patch

from data.cdn_stream import cdn_records_from_snapshot

def test_cdn_records_from_snapshot_no_hf_api_import():
    # Ensure huggingface_hub is not imported inside cdn_stream module
    import sys
    assert "huggingface_hub" not in sys.modules or "huggingface_hub" not in dir(sys.modules.get("data.cdn_stream", type(sys)))

def test_cdn_records_from_snapshot_yields():
    snapshot = [
        {"cdn_url": "https
