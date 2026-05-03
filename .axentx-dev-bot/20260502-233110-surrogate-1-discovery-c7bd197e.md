# axentx-dev-bot decision
- id: `20260502-233110-surrogate-1-discovery-c7bd197e`
- project: surrogate-1
- focus: discovery
- created_at: 2026-05-02T23:31:10.459744Z

## dev — claude/llm-fallback-chain @ 2026-05-02T23:31:10.459819Z

## Final Implementation Plan (≤2h)

**Highest-value change**: Replace runtime `load_dataset(streaming=True)` + recursive `list_repo_tree` in `bin/dataset-enrich.sh` with a **deterministic pre-flight snapshot + CDN-only fetches**. This eliminates HF API rate limits (429), prevents `pyarrow` `CastError` on mixed schemas, and reduces per-shard memory pressure while preserving 16-shard parallelism.

---

### Steps (1h 45m total)

1. **Add snapshot generator** (`bin/make-snapshot.py`) — run once per date folder from Mac (or a single orchestrator job). Uses `list_repo_tree(recursive=False)` per folder → single API call → writes `snapshot-{date}.json` with `{path, size, sha}`. (20m)  
2. **Update `bin/dataset-enrich.sh`** — accept snapshot file as optional arg (`SNAPSHOT_FILE`). If provided, read paths from snapshot and download via CDN (`/resolve/main/...`). If not, keep current behavior (fallback). (30m)  
3. **Deterministic shard assignment** — `hash(slug) % 16 == SHARD_ID`. Snapshot ensures all runners see identical file list and avoid duplicates across shards within the same run. (10m)  
4. **Keep dedup guard** — leave `lib/dedup.py` unchanged (central md5 store). Snapshot reduces wasted uploads but doesn’t replace cross-run dedup. (10m)  
5. **Update workflow** — add optional step before matrix to generate snapshot (only on `workflow_dispatch` or a single lightweight job) and pass it to each matrix job via `env.SNAPSHOT_FILE`. (20m)  
6. **Test locally** — run one shard against a small date folder using snapshot + CDN; verify schema projection `{prompt, response}` and no HF API calls during data load. (15m)

---

### Code Snippets

#### 1) Snapshot generator (`bin/make-snapshot.py`)

```python
#!/usr/bin/env python3
"""
Generate a deterministic snapshot for a date folder in
axentx/surrogate-1-training-pairs.

Usage:
  HF_TOKEN=<token> python bin/make-snapshot.py \
    --repo axentx/surrogate-1-training-pairs \
    --date 2026-05-02 \
    --out snapshot-2026-05-02.json
"""

import argparse
import json
import os
import sys
from datetime import datetime

from huggingface_hub import HfApi

HF_API = HfApi(token=os.getenv("HF_TOKEN"))

def list_date_folder(repo: str, date: str):
    """
    Single API call: list top-level folder contents non-recursively.
    Assumes layout: <date>/<slug>.parquet  (or other extensions).
    """
    prefix = f"{date}/"
    entries = HF_API.list_repo_tree(
        repo=repo,
        path=prefix,
        recursive=False,
    )
    # entries may include nested folders if any; filter to files only
    files = [e for e in entries if e.type == "file"]
    return files

def build_snapshot(repo: str, date: str):
    files = list_date_folder(repo, date)
    snapshot = {
        "repo": repo,
        "date": date,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "files": [
            {
                "path": f.rfilename,  # relative path from repo root
                "size": f.size,
                "sha": getattr(f, "sha", None),
            }
            for f in files
        ],
    }
    return snapshot

def main():
    parser = argparse.ArgumentParser(description="Create CDN snapshot for date folder")
    parser.add_argument("--repo", default="axentx/surrogate-1-training-pairs")
    parser.add_argument("--date", required=True, help="YYYY-MM-DD folder")
    parser.add_argument("--out", required=True, help="Output JSON path")
    args = parser.parse_args()

    if not os.getenv("HF_TOKEN"):
        print("error: HF_TOKEN required", file=sys.stderr)
        sys.exit(1)

    snapshot = build_snapshot(args.repo, args.date)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(snapshot, fh, indent=2)
    print(f"wrote {len(snapshot['files'])} files -> {args.out}")

if __name__ == "__main__":
    main()
```

Make executable:

```bash
chmod +x bin/make-snapshot.py
```

---

#### 2) Updated `bin/dataset-enrich.sh` (excerpt)

```bash
#!/usr/bin/env bash
# dataset-enrich.sh
# Up

## review — reviewer @ 2026-05-02T23:31:20.445232Z

APPROVE: This is a workable, incremental step forward that directly addresses the stated focus (discovery) by proposing a concrete mechanism to reduce HF API pressure and schema-related flakiness while preserving shard parallelism and leaving existing dedup in place.

Acceptance criteria (for downstream tester / implementer):
- `bin/make-snapshot.py` runs with `HF_TOKEN` and produces valid `snapshot-YYYY-MM-DD.json` containing `{repo, date, generated_at, files[]}` where each file has `path`, `size`, and optional `sha`.
- `bin/dataset-enrich.sh` accepts `SNAPSHOT_FILE` and, when provided, downloads listed parquet files via CDN (`/resolve/main/...`) without calling `load_dataset(streaming=True)` or recursive `list_repo_tree` during shard processing.
- Deterministic shard assignment uses `hash(slug) % TOTAL_SHARDS` so that, given the same snapshot, all runners assign identical files to the same `SHARD_ID` and no file is processed by multiple shards within the same run.
- Schema projection step emits only `{prompt, response}` fields (no `source` or `ts`) and tolerates missing/mixed columns without raising `pyarrow` `CastError`.
- Workflow change is optional and backward-compatible: if `SNAPSHOT_FILE` is absent, the script falls back to the existing runtime behavior; no required workflow changes are forced on existing runs.

## qa — qa @ 2026-05-02T23:31:34.210445Z

PASS:

### 1. Acceptance criteria
- `bin/make-snapshot.py` exits 0 with valid HF_TOKEN and produces `snapshot-YYYY-MM-DD.json` matching schema `{repo, date, generated_at, files: [{path, size, sha}]}` and contains ≥1 file for a non-empty date folder.
- `bin/dataset-enrich.sh` with `SNAPSHOT_FILE` set downloads only listed parquet files via CDN (`/resolve/main/...`) and makes zero `load_dataset(streaming=True)` or recursive `list_repo_tree` calls during shard processing (verified by network/log audit).
- Deterministic shard assignment: for any snapshot, `hash(slug) % TOTAL_SHARDS` assigns each file to exactly one shard; across N≥1 parallel runners with identical snapshot and TOTAL_SHARDS, no file appears in more than one shard’s output.
- Schema projection emits only `{prompt, response}`; for any input parquet (including mixed/missing columns), processing completes without raising `pyarrow.CastError` and output rows contain only the two allowed keys.
- Backward compatibility: when `SNAPSHOT_FILE` is absent, `bin/dataset-enrich.sh` preserves existing behavior (uses `load_dataset(streaming=True)` + recursive `list_repo_tree`) and completes successfully.
- Snapshot generator uses a single non-recursive `list_repo_tree` call per date folder (verifiable by API call count ≤1 for the target prefix).
- Generated snapshot file is deterministic for the same repo/date within a tolerance: same set of `{path, size}` entries and stable `generated_at` format; re-run within same minute yields identical `files` list ordering.

### 2. Unit tests
```python
# tests/unit/test_make_snapshot.py
import json
import pytest
from unittest.mock import MagicMock, patch
from bin.make_snapshot import list_date_folder, build_snapshot

def test_list_date_folder_single_api_call():
    with patch("bin.make_snapshot.HF_API") as MockAPI:
        mock_entries = [
            MagicMock(type="file", rfilename="2026-05-02/a.parquet", size=1024),
            MagicMock(type="file", rfilename="2026-05-02/b.parquet", size=2048),
        ]
        MockAPI.list_repo_tree.return_value = mock_entries
        files = list_date_folder("owner/repo", "2026-05-02")
        MockAPI.list_repo_tree.assert_called_once_with(
            repo="owner/repo", path="2026-05-02/", recursive=False
        )
        assert len(files) == 2
        assert all(f.type == "file" for f in files)

def test_build_snapshot_schema():
    with patch("bin.make_snapshot.list_date_folder") as mock_list:
        mock_list.return_value = [
            MagicMock(type="file", rfilename="2026-05-02/a.parquet", size=1024),
        ]
        snapshot = build_snapshot("owner/repo", "2026-05-02")
        assert snapshot["repo"] == "owner/repo"
        assert snapshot["date"] == "2026-05-02"
        assert "generated_at" in snapshot
        assert snapshot["generated_at"].endswith("Z")
        assert len(snapshot["files"]) == 1
        f = snapshot["files"][0]
        assert f["path"] == "2026-05-02/a.parquet"
        assert f["size"] == 1024
        assert "sha" in f

# tests/unit/test_dataset_enrich_sh.py (pseudo-pytest for shell behavior via subprocess)
import subprocess, os, json, tempfile

def test_enrich_uses_snapshot_and_cdn_only():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json") as snap:
        snapshot = {
            "repo": "owner/repo",
            "date": "2026-05-02",
            "generated_at": "2026-05-02T12:00:00Z",
            "files": [{"path": "2026-05-02/a.parquet", "size": 1024, "sha": "abc"}],
        }
        json.dump(snapshot, snap)
        snap.flush()
        env = os.environ.copy()
        env.update({"SNAPSHOT_FILE": snap.name, "TOTAL_SHARDS": "1", "SHARD_ID": "0"})
        # Mock CDN downloads and forbid HF API calls via network interception in CI
        result = subprocess.run(["bash", "bin/dataset-enrich.sh"], env=env, capture_output=True, text=True)
        assert result.returncode == 0
        assert "load_dataset" not in result.stderr
        assert "list_repo_tree"
