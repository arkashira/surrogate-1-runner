# axentx-dev-bot decision
- id: `20260503-002125-surrogate-1-quality-258a3ddb`
- project: surrogate-1
- focus: quality
- created_at: 2026-05-03T00:21:25.900996Z

## dev — claude/llm-fallback-chain @ 2026-05-03T00:21:25.901052Z

## Final Implementation Plan  
**Goal:** Eliminate HF API rate-limits during training, avoid PyArrow CastError, keep ingestion deterministic, and require ≤2h to ship.

---

### 1) Highest-value improvement (≤2h)
Add `bin/snapshot.sh` that produces a **deterministic per-date manifest** and update ingestion/training to use **CDN-only fetches** when a manifest is present.  
- Removes recursive `list_repo_files`/`list_repo_tree` calls during training (eliminates 429s).  
- Avoids `load_dataset(streaming=True)` on heterogeneous repos (prevents CastError).  
- Keeps Mac as orchestrator-only; heavy data movement runs on GitHub Actions/HF Space/Lightning.  
- Enables reproducible training runs (same manifest → same data/sharding).

---

### 2) Concrete changes

#### A. Add `bin/snapshot.sh`
- Inputs: `REPO`, `DATE` (e.g. `2026-04-29`), optional `OUT_DIR`.  
- Single API call: `list_repo_tree(path=DATE, recursive=false)` (non-recursive to avoid pagination/429).  
- Output: `snapshots/{REPO_SLUG}/{DATE}/manifest.json`  
  ```json
  {
    "repo": "owner/repo",
    "date": "2026-04-29",
    "snapshot_ts": "2026-04-29T14:03:00Z",
    "files": ["2026-04-29/file1.parquet", "2026-04-29/file2.parquet"],
    "count": 2
  }
  ```
- Deterministic lexicographic ordering for reproducible sharding.  
- Commit snapshots to repo (or push to dataset repo via sibling-repo hashing respecting 128/hr HF API cap).

#### B. Update `bin/dataset-enrich.sh`
- Add optional `--snapshot snapshots/.../manifest.json`.  
- If provided, skip recursive listing; drive per-file ingestion via manifest.  
- Project to `{prompt,response}` at parse time; write to `batches/public-merged/<date>/shard<N>-<HHMMSS>.jsonl`.

#### C. Add training-side support (`lib/manifest_loader.py`)
- Accept `--manifest snapshots/.../manifest.json`.  
- When manifest present, construct CDN URLs:  
  `https://huggingface.co/datasets/{repo}/resolve/main/{file_path}`  
- Stream via `requests` + `pyarrow.parquet` (or download-then-read) with `streaming=True`-like behavior per file.  
- No `load_dataset(..., streaming=True)` on repo root; download individual parquet files via CDN then parse.

#### D. GitHub Actions (optional polish)
- Add one-off `snapshot.yml` that runs `bin/snapshot.sh` for the latest date folder and commits snapshot to repo (or dataset repo).  
- Keep existing 16-shard matrix workflow unchanged; it can consume snapshots to avoid per-run listing.

---

### 3) Code snippets

#### `bin/snapshot.sh`
```bash
#!/usr/bin/env bash
# bin/snapshot.sh
# Usage: HF_TOKEN=... bin/snapshot.sh <repo> <date> [out_dir]
# Example: HF_TOKEN=... bin/snapshot.sh axentx/surrogate-1-training-pairs 2026-04-29 snapshots
set -euo pipefail

REPO="${1:-axentx/surrogate-1-training-pairs}"
DATE="${2:-$(date +%Y-%m-%d)}"
OUT_DIR="${3:-snapshots}"
HF_TOKEN="${HF_TOKEN:-}"
API_ROOT="https://huggingface.co/api"

mkdir -p "${OUT_DIR}/${REPO}/${DATE}"

# Single non-recursive tree call to avoid pagination/429
echo "Listing ${REPO} tree for ${DATE} (non-recursive)..."
TREE_JSON=$(curl -sSf \
  -H "Authorization: Bearer ${HF_TOKEN}" \
  "${API_ROOT}/datasets/${REPO}/tree?path=${DATE}&recursive=false")

# Extract file paths (type "file") and sort deterministically
FILES=$(echo "$TREE_JSON" | python3 -c "
import sys, json
tree = json.load(sys.stdin)
paths = [item['path'] for item in tree if item.get('type') == 'file']
for p in sorted(paths):
    print(p)
")

if [ -z "$FILES" ]; then
  echo "No files found for ${DATE} in ${REPO}"
  exit 1
fi

SNAP_TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
MANIFEST="${OUT_DIR}/${REPO}/${DATE}/manifest.json"

python3 -c "
import json, os
repo = os.environ['REPO']
date = os.environ['DATE']
files = os.environ['FILES'].splitlines()
manifest = {
    'repo': repo,
    'date': date,
    'snapshot_ts': os.environ['SNAP_TS'],
    'files': files,
    'count': len(files)
}
with open(os.environ['MANIFEST'], 'w') as f:
    json.dump(manifest, f, indent=2)
print(f'Wrote {len(files)} entries to {os.environ[\"MA

## review — reviewer @ 2026-05-03T00:21:32.201664Z

APPROVE: This is a workable, incremental step that directly targets HF API rate-limits and CastError while keeping ingestion deterministic and shipping within ~2h. It proposes concrete, runnable artifacts (snapshot.sh, manifest_loader.py) and a clear migration path (manifest-driven CDN fetches instead of recursive listing/load_dataset on heterogeneous repos).

Acceptance criteria a downstream tester could check:
- `bin/snapshot.sh` runs with a valid HF_TOKEN and produces `snapshots/{repo}/{date}/manifest.json` containing deterministic, lexicographically sorted file entries and valid metadata (repo, date, snapshot_ts, count).
- When `--manifest` is provided, `bin/dataset-enrich.sh` skips recursive listing and processes only files listed in the manifest, writing `batches/public-merged/<date>/shard-*.jsonl` with `{prompt,response}` projection.
- `lib/manifest_loader.py` (or equivalent training-side loader) accepts a manifest, constructs valid CDN URLs, downloads individual parquet files, and yields rows with the requested columns without calling `load_dataset(..., streaming=True)` on the repo root.
- No recursive `list_repo_tree`/`list_repo_files` calls occur during training when a manifest is present (verify via logs or by running with a low HF API quota and confirming no 429s).
- Manifest-based runs are reproducible: two training runs using the same manifest file produce identical data order and shard contents (barring non-deterministic shuffle).

## qa — qa @ 2026-05-03T00:22:09.143889Z

PASS: 

### 1) Acceptance criteria
- `bin/snapshot.sh` exits 0 with valid HF_TOKEN and produces `snapshots/{repo_slug}/{DATE}/manifest.json` containing keys `repo`, `date`, `snapshot_ts`, `files` (array), `count`; `files` is lexicographically sorted and non-empty when tree has files.
- Manifest `count` equals the length of `files`; each file path begins with `{DATE}/` and has a `.parquet` extension.
- With `--manifest` provided, `bin/dataset-enrich.sh` skips recursive listing (no `list_repo_tree` recursive calls in logs) and emits `batches/public-merged/<date>/shard-*.jsonl` where every line is valid JSON with `prompt` and `response` fields.
- `lib/manifest_loader.py` accepts `--manifest`, constructs CDN URLs of form `https://huggingface.co/datasets/{repo}/resolve/main/{file_path}`, streams each parquet file, and yields rows without ever invoking `load_dataset(..., streaming=True)` on the repo root.
- Training run with manifest present produces zero recursive `list_repo_tree`/`list_repo_files` API calls (verified via request logs or mock) and completes without 429 errors under a constrained API quota.
- Two training runs using the same manifest produce identical shard contents and row order (determinism) when shuffle seed is fixed and no external non-determinism is introduced.

### 2) Unit tests
```python
# tests/unit/test_snapshot.py
import json, subprocess, os, tempfile, pytest

def test_snapshot_sh_creates_valid_manifest():
    with tempfile.TemporaryDirectory() as out:
        # mock HF API via fixture or recorded response in CI
        result = subprocess.run(
            ["bash", "bin/snapshot.sh", "owner/dummy", "2026-04-29", out],
            env={**os.environ, "HF_TOKEN": "fake"}, capture_output=True, text=True
        )
        assert result.returncode == 0
        manifest_path = os.path.join(out, "owner/dummy/2026-04-29/manifest.json")
        assert os.path.exists(manifest_path)
        with open(manifest_path) as f:
            m = json.load(f)
        assert m["repo"] == "owner/dummy"
        assert m["date"] == "2026-04-29"
        assert "T" in m["snapshot_ts"] and "Z" in m["snapshot_ts"]
        assert isinstance(m["files"], list)
        assert m["count"] == len(m["files"])
        assert all(f.startswith("2026-04-29/") and f.endswith(".parquet") for f in m["files"])
        assert m["files"] == sorted(m["files"])  # deterministic order

# tests/unit/test_dataset_enrich.py
def test_dataset_enrich_skips_recursive_listing_when_manifest(tmp_path, mocker):
    manifest = tmp_path / "manifest.json"
    manifest.write_text('{"repo":"x/y","date":"2026-04-29","files":["2026-04-29/a.parquet"],"count":1}')
    list_spy = mocker.spy(subprocess, "run")
    out = tmp_path / "batches"
    result = subprocess.run(
        ["bash", "bin/dataset-enrich.sh", "--manifest", str(manifest), "--out", str(out)],
        capture_output=True, text=True
    )
    assert result.returncode == 0
    # ensure no recursive listing occurred (implementation-specific log/flag check)
    calls = [c for c in list_spy.call_args_list if "list_repo_tree" in str(c)]
    assert not any("--recursive" in str(c) or "-r" in str(c) for c in calls)

# tests/unit/test_manifest_loader.py
def test_manifest_loader_constructs_cdn_urls_and_avoids_load_dataset(mocker):
    mock_read_parquet = mocker.patch("pyarrow.parquet.read_table")
    mock_requests = mocker.patch("requests.get")
    mock_load_dataset = mocker.patch("datasets.load_dataset")
    from lib.manifest_loader import stream_from_manifest
    manifest = {"repo":"x/y","date":"2026-04-29","files":["2026-04-29/a.parquet"],"count":1}
    list(stream_from_manifest(manifest))
    assert mock_load_dataset.call_count == 0
    assert mock_requests.call_count == 1
    called_url = mock_requests.call_args[0][0]
    assert called_url == "https://huggingface.co/datasets/x/y/resolve/main/2026-04-29/a.parquet"
```

### 3) Integration tests
Happy paths:
- Snapshot → manifest → dataset-enrich → training: run end-to-en
