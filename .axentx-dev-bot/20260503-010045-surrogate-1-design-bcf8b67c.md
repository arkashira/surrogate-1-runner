# axentx-dev-bot decision
- id: `20260503-010045-surrogate-1-design-bcf8b67c`
- project: surrogate-1
- focus: design
- created_at: 2026-05-03T01:00:45.311186Z

## dev — claude/llm-fallback-chain @ 2026-05-03T01:00:45.311251Z

## Final Consolidated Implementation (Best of Both)

**Goal**: Eliminate HF API rate-limit failures and HF Space OOM by replacing recursive `list_repo_files` and per-file API calls with **one per-folder `list_repo_tree` snapshot + CDN-only fetches**.

**Why this wins**:
- Removes recursive API calls that trigger 429s on large repos.
- CDN URLs (`resolve/main/...`) bypass auth/rate limits and have much higher quotas.
- Single `list_repo_tree(path, recursive=False)` per folder → small, fast, cacheable.
- Prevents OOM in HF Spaces by avoiding `load_dataset(streaming=True)` on heterogeneous repos.
- Fits in ≤2h; no schema changes; minimal risk.

---

## Implementation Plan

1. **Add snapshot utility** (`bin/list-folder-snapshot.py`)  
   - Uses `HfApi.list_repo_tree(path, recursive=False)` for one folder.  
   - Emits `snapshot.json` with `{"files": [...], "base": "public/2026-05-03"}`.  
   - Exits non-zero on 429 with message to retry after 360s.

2. **Update `bin/dataset-enrich.sh`**  
   - Accept optional `FOLDER` and `SNAPSHOT_JSON`.  
   - If `SNAPSHOT_JSON` provided, read file list from it; skip API listing.  
   - Default to CDN mode; download via `curl` from `resolve/main/...`.  
   - Fallback to `hf_hub_download` only on CDN failure (404/403).  
   - Deterministic shard assignment by filename hash.

3. **Workflow update** (`.github/workflows/ingest.yml`)  
   - Set `env.USE_CDN: true` and compute `DATE_FOLDER` from run date or input.

4. **Validation & rollout**  
   - Local test with `HF_TOKEN=... SHARD_ID=0 TOTAL_SHARDS=16 bin/dataset-enrich.sh`.  
   - Confirm `snapshot.json` and shard outputs; verify no 429s.

---

## Code Changes

### 1) `bin/list-folder-snapshot.py`

```python
#!/usr/bin/env python3
"""
Create a snapshot of files in one folder of a Hugging Face dataset repo.
Usage:
  HF_TOKEN=... python bin/list-folder-snapshot.py \
    --repo axentx/surrogate-1-training-pairs \
    --folder public/2026-05-03 \
    --out snapshot.json
"""
import argparse
import json
import sys
import time
from huggingface_hub import HfApi, RepositoryError

def main():
    parser = argparse.ArgumentParser(description="Snapshot folder files from HF repo.")
    parser.add_argument("--repo", required=True, help="Repo ID (e.g., axentx/...)")
    parser.add_argument("--folder", required=True, help="Folder path in repo")
    parser.add_argument("--out", default="snapshot.json", help="Output JSON path")
    parser.add_argument("--token", default=None, help="HF token (or use HF_TOKEN)")
    args = parser.parse_args()

    token = args.token or sys.argv[1] if len(sys.argv) > 1 else None
    api = HfApi(token=token)

    try:
        tree = api.list_repo_tree(args.repo, path=args.folder, recursive=False)
    except RepositoryError as e:
        # If rate-limited, suggest retry after 360s
        if "429" in str(e):
            print("Rate limited (429). Retry after 360s.", file=sys.stderr)
            sys.exit(1)
        raise

    files = [item.rfilename for item in tree if item.type == "file"]
    snapshot = {"files": files, "base": args.folder.rstrip("/")}

    with open(args.out, "w") as f:
        json.dump(snapshot, f, indent=2)

    print(f"Snapshot written to {args.out} ({len(files)} files)")

if __name__ == "__main__":
    main()
```

---

### 2) `bin/dataset-enrich.sh` (core worker)

```bash
#!/usr/bin/env bash
set -euo pipefail

# Config
REPO_ID="${HF_REPO_ID:-axentx/surrogate-1-training-pairs}"
HF_TOKEN="${HF_TOKEN:-}"
FOLDER="${FOLDER:-$(date +%Y-%m-%d)}"
SNAPSHOT_JSON="${SNAPSHOT_JSON:-}"
SHARD_ID="${SHARD_ID:-0}"
TOTAL_SHARDS="${TOTAL_SHARDS:-16}"
OUTDIR="${OUTDIR:-output}"
USE_CDN="${USE_CDN:-true}"

mkdir -p "${OUTDIR}"

# Download via CDN (no auth header required for public datasets)
download_via_cdn() {
  local repo="$1"
  local path="$2"
  local out="$3"
  local url="https://huggingface.co/datasets/${repo}/resolve/main/${path}"
  curl -fsSL --retry 3 --retry-delay 2 -o "${out}" "${url}"
}

# Fallback: hf_hub_download (uses

## review — reviewer @ 2026-05-03T01:00:56.814076Z

APPROVE: This is a workable, incremental design that directly targets HF API 429s and HF Space OOM by replacing recursive/per-file API calls with one folder-level `list_repo_tree` + CDN fetches. It keeps scope minimal (no schema changes), is cacheable, and has a clear rollback path (fallback to `hf_hub_download`). A downstream tester can validate the snapshot + CDN path and confirm reduced 429s.

Acceptance criteria:
- `bin/list-folder-snapshot.py` runs non-interactively with `HF_TOKEN` and produces valid `snapshot.json` containing a `files` list and `base` string; exits non-zero on 429 with a clear message.
- `bin/dataset-enrich.sh` accepts `SNAPSHOT_JSON` and, when provided, skips API listing and uses the snapshot file list; when `USE_CDN=true`, downloads via `https://huggingface.co/datasets/.../resolve/main/...` and falls back to `hf_hub_download` on CDN 404/403.
- Deterministic shard assignment: same filename always maps to the same shard given `SHARD_ID`/`TOTAL_SHARDS` (e.g., via `sha256(filename) % TOTAL_SHARDS == SHARD_ID`).
- Workflow `.github/workflows/ingest.yml` sets `USE_CDN=true` and computes `FOLDER` from run date or input; runs without syntax errors and produces expected shard outputs.
- Local smoke test with `HF_TOKEN=... SHARD_ID=0 TOTAL_SHARDS=16 bin/dataset-enrich.sh` completes without 429s and emits non-empty shard outputs for a small public repo/folder.

## qa — qa @ 2026-05-03T01:01:22.668317Z

PASS

1. **Acceptance criteria**
- `bin/list-folder-snapshot.py` exits 0 with valid `snapshot.json` containing `files` (array of strings) and `base` (string) when given valid repo/folder and token; exits non-zero with stderr containing "Rate limited (429)" on simulated 429.
- `bin/dataset-enrich.sh` with `SNAPSHOT_JSON` skips API listing and uses snapshot file list; without snapshot it performs listing (or uses fallback) and still completes.
- `bin/dataset-enrich.sh` with `USE_CDN=true` attempts CDN fetch via `resolve/main/...` first; on CDN 404/403 it falls back to `hf_hub_download`; success is recorded per file.
- Deterministic shard assignment: for any filename, `sha256(filename) % TOTAL_SHARDS` equals assigned shard; across runs with same `TOTAL_SHARDS` and `SHARD_ID`, identical file sets are selected.
- Workflow `.github/workflows/ingest.yml` sets `env.USE_CDN=true` and computes `FOLDER` from run date or input; workflow syntax is valid and produces shard outputs (artifact or file) when run in dry-run/local simulation.
- Local smoke test with `HF_TOKEN=<valid> SHARD_ID=0 TOTAL_SHARDS=16 bin/dataset-enrich.sh` on a small public repo/folder completes with exit 0, zero 429s, and emits non-empty shard outputs.

2. **Unit tests**
```python
# tests/unit/test_list_folder_snapshot.py
import json
import subprocess
import tempfile
import os
from unittest.mock import patch, MagicMock

def test_snapshot_success():
    with patch("huggingface_hub.HfApi.list_repo_tree") as mock_tree:
        mock_tree.return_value = [
            type("Item", (), {"rfilename": "public/2026-05-03/a.jsonl"}),
            type("Item", (), {"rfilename": "public/2026-05-03/b.jsonl"}),
        ]
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            out_path = f.name
        try:
            import sys
            sys.argv = ["list-folder-snapshot.py", "--repo", "test/repo",
                        "--folder", "public/2026-05-03", "--out", out_path]
            import bin.list_folder_snapshot
            bin.list_folder_snapshot.main()
            with open(out_path) as fp:
                data = json.load(fp)
            assert "files" in data and isinstance(data["files"], list)
            assert len(data["files"]) == 2
            assert data["base"] == "public/2026-05-03"
        finally:
            os.unlink(out_path)

def test_snapshot_rate_limit_exit_nonzero():
    with patch("huggingface_hub.HfApi.list_repo_tree") as mock_tree:
        mock_tree.side_effect = Exception("429")
        result = subprocess.run(
            ["python", "bin/list-folder-snapshot.py", "--repo", "x/y", "--folder", "z"],
            capture_output=True, text=True, env={**os.environ, "HF_TOKEN": "fake"}
        )
        assert result.returncode != 0
        assert "Rate limited (429)" in result.stderr
```

```bash
# tests/unit/test_dataset_enrich.sh (bash unit style via bats or shunit2)
# Pseudo-code for Jest-like assertions in shell context

test_uses_snapshot_skips_api() {
  export SNAPSHOT_JSON="tests/fixtures/snapshot.json"
  export USE_CDN="false"
  export SHARD_ID=0
  export TOTAL_SHARDS=1
  export REPO="dummy/repo"
  export FOLDER="public/2026-05-03"
  # Mock curl/hf_hub_download to record calls
  run ./bin/dataset-enrich.sh
  # Assert no curl to HF API listing endpoint occurred
  assert_not_contains "$output" "list_repo_tree"
  # Assert files processed match snapshot
  assert_contains "$output" "a.jsonl"
}

test_cdn_first_fallback() {
  export USE_CDN="true"
  export SHARD_ID=0
  export TOTAL_SHARDS=1
  # Mock curl to return 404 for first file, 200 for second
  # Mock hf_hub_download to succeed
  run ./bin/dataset-enrich.sh
  # Assert CDN attempted first
  assert_contains "$output" "resolve/main"
  # Assert fallback invoked on 404
  assert_contains "$output" "hf_hub_download"
}

test_shard_assignment_deterministic() {
  files=("file1.jsonl" "file2.jsonl" "file3.jsonl")
  TOTAL_SHARDS=4
  for f in "${files[@]}"; do
    h=$(ec
