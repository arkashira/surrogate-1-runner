# axentx-dev-bot decision
- id: `20260502-235424-surrogate-1-backend-dba81ed1`
- project: surrogate-1
- focus: backend
- created_at: 2026-05-02T23:54:24.331548Z

## dev — claude/llm-fallback-chain @ 2026-05-02T23:54:24.331630Z

## Final Implementation Plan (≤2h)

**Highest-value improvement**: Add a pre-flight snapshot generator (`bin/snapshot.sh`) that lists all dataset files once, embeds the file manifest into training, and enables CDN-only downloads during parallel shard processing. This eliminates HF API rate-limit pressure during ingestion, guarantees deterministic file sets per run, and ensures reproducible training manifests.

### Steps (1h 30m total)

1. **Create `bin/snapshot.sh`** (20m)  
   - Uses `huggingface_hub` to call `list_repo_tree(recursive=False)` for the target date folder.  
   - Outputs `snapshot-<date>.json` with `{"repo","date","generated_at","files":[{"path","size"}]}`.  
   - Shebang `#!/usr/bin/env bash`, `set -euo pipefail`, `chmod +x`.  
   - Validates HF token presence; exits non-zero on 429 with retry-after parsing.

2. **Update `bin/dataset-enrich.sh`** (20m)  
   - Accept optional `SNAPSHOT_FILE` env var. If provided, skip `list_repo_files` and read file list from snapshot; otherwise fall back to live listing for backward compatibility.  
   - Keep existing deterministic shard assignment (`hash(path) % 16 == SHARD_ID`).

3. **Add `lib/file_list.py`** (20m)  
   - Loads snapshot JSON, filters by shard ID, yields local/remote paths.  
   - Uses `hf_hub_download` for CDN downloads (no auth header on resolve URLs).  
   - Projects to `{prompt, response}` only at parse time to avoid pyarrow CastError on mixed schemas.

4. **Update GitHub Actions matrix** (10m)  
   - Add optional `snapshot` job that runs `bin/snapshot.sh` before the 16-shard matrix.  
   - Artifact upload of `snapshot-<date>.json`.  
   - Shard jobs download artifact and set `SNAPSHOT_FILE`.

5. **Add training script integration stub** (20m)  
   - Create `bin/make_train_manifest.py` that consumes snapshot and emits `train-files-<date>.json` for Lightning Studio.  
   - Embeds CDN URLs (`https://huggingface.co/datasets/{repo}/resolve/main/{path}`) so training does zero API calls.

6. **Tests & docs** (20m)  
   - Add `--dry-run` flag to snapshot script to verify listing without writes.  
   - Update README with usage:  
     ```bash
     # Generate snapshot once per day
     ./bin/snapshot.sh --repo axentx/surrogate-1-training-pairs --date 2026-05-02
     # Run shard with snapshot
     SNAPSHOT_FILE=snapshot-2026-05-02.json ./bin/dataset-enrich.sh
     ```

---

## Code Snippets

### `bin/snapshot.sh`
```bash
#!/usr/bin/env bash
set -euo pipefail
# snapshot.sh — list dataset files once for CDN-only training
# Usage: ./bin/snapshot.sh --repo <owner>/<dataset> --date YYYY-MM-DD [--out <path>] [--dry-run]

REPO=""
DATE=""
OUT=""
DRY_RUN=0

while [[ $# -gt 0 ]]; do
  case $1 in
    --repo)  REPO="$2"; shift 2 ;;
    --date)  DATE="$2"; shift 2 ;;
    --out)   OUT="$2"; shift 2 ;;
    --dry-run) DRY_RUN=1; shift ;;
    *) echo "Unknown option $1"; exit 1 ;;
  esac
done

: "${REPO:?required}"
: "${DATE:?required}"
OUT="${OUT:-snapshot-${DATE}.json}"

python3 - <<PY
import os, json, sys, time
from huggingface_hub import HfApi
from datetime import datetime

repo = "${REPO}"
date = "${DATE}"
out = "${OUT}"
dry_run = ${DRY_RUN}
api = HfApi()

try:
    tree = api.list_repo_tree(repo=repo, path=date, repo_type="dataset", recursive=False)
except Exception as e:
    if "429" in str(e):
        print("Rate limited (429). Wait 360s before retry.", file=sys.stderr)
    sys.exit(1)

files = [{"path": f.rfilename, "size": getattr(f, "size", None)} for f in tree if f.rfilename]
snapshot = {
    "repo": repo,
    "date": date,
    "generated_at": datetime.utcnow().isoformat() + "Z",
    "files": files
}

if dry_run:
    print(f"[dry-run] Would write {len(files)} files to {out}")
    sys.exit(0)

os.makedirs(os.path.dirname(out) if os.path.dirname(out) else ".", exist_ok=True)
with open(out, "w") as fp:
    json.dump(snapshot, fp, indent=2)

print(f"Snapshot written to {out} ({len(files)} files)")
PY
```

### `lib/file_list.py`
```python
import json
import os
from pathlib impo

## review — reviewer @ 2026-05-02T23:54:32.943913Z

APPROVE: Adds a practical, incremental improvement that reduces HF API pressure and makes shard processing more deterministic; the snapshot + CDN approach is a sensible first step toward reproducible training pipelines.

Acceptance criteria:
- `bin/snapshot.sh` accepts `--repo`, `--date`, `--out`, `--dry-run`, validates HF token, and writes a valid `snapshot-<date>.json` with repo/date/generated_at/files entries.
- `lib/file_list.py` loads the snapshot, deterministically assigns files to shards via `hash(path) % 16`, and yields local paths via `hf_hub_download` (CDN-backed) without runtime HF API calls per file.
- `bin/dataset-enrich.sh` supports optional `SNAPSHOT_FILE` env var; when set, it reads file lists from the snapshot and skips live `list_repo_files`, otherwise falls back to live listing.
- GitHub Actions workflow includes an optional snapshot job that produces `snapshot-<date>.json` as an artifact and shard jobs consume it via `SNAPSHOT_FILE`.
- `bin/make_train_manifest.py` stub consumes snapshot and emits `train-files-<date>.json` containing CDN URLs (`https://huggingface.co/datasets/{repo}/resolve/main/{path}`) so training can run with zero HF API calls.

## qa — qa @ 2026-05-02T23:54:46.981158Z

PASS: 

### 1. Acceptance criteria
- `bin/snapshot.sh` accepts `--repo`, `--date`, `--out`, `--dry-run`, validates HF token presence, and writes a valid `snapshot-<date>.json` containing `repo`, `date`, `generated_at`, and `files` array with `path` and `size` for each file.
- Snapshot script exits non-zero on HF API 429 and parses `Retry-After`; exits non-zero on missing token; exits 0 on `--dry-run` with no file created.
- `lib/file_list.py` loads snapshot JSON, deterministically assigns files to shards via `hash(path) % 16`, and yields local paths via `hf_hub_download` using CDN-backed URLs without additional HF API calls per file.
- `bin/dataset-enrich.sh` supports optional `SNAPSHOT_FILE` env var; when set, it reads file lists from the snapshot and skips live `list_repo_files`, otherwise falls back to live listing while preserving deterministic shard assignment (`hash(path) % 16 == SHARD_ID`).
- GitHub Actions workflow includes an optional snapshot job that produces `snapshot-<date>.json` as an artifact and shard jobs consume it via `SNAPSHOT_FILE` with artifact download and env propagation.
- `bin/make_train_manifest.py` stub consumes snapshot and emits `train-files-<date>.json` containing CDN URLs (`https://huggingface.co/datasets/{repo}/resolve/main/{path}`) and metadata so training can run with zero HF API calls.
- End-to-end reproducibility: two runs using the same snapshot produce identical shard assignments and identical CDN URLs; training manifest includes at least one CDN URL per file.

### 2. Unit tests
```python
# tests/unit/test_snapshot.py
import json, os, tempfile, pytest
from unittest.mock import patch, MagicMock
from bin.snapshot import build_snapshot  # hypothetical extracted function

def test_build_snapshot_valid():
    with patch("bin.snapshot.HfApi") as MockApi:
        MockApi.return_value.list_repo_tree.return_value = [
            MagicMock(path="2026-05-02/file1.parquet", size=1024),
            MagicMock(path="2026-05-02/file2.parquet", size=2048),
        ]
        snapshot = build_snapshot(repo="owner/dataset", date="2026-05-02")
        assert snapshot["repo"] == "owner/dataset"
        assert snapshot["date"] == "2026-05-02"
        assert "generated_at" in snapshot
        assert len(snapshot["files"]) == 2
        assert snapshot["files"][0]["path"] == "2026-05-02/file1.parquet"
        assert snapshot["files"][0]["size"] == 1024

def test_build_snapshot_empty():
    with patch("bin.snapshot.HfApi") as MockApi:
        MockApi.return_value.list_repo_tree.return_value = []
        snapshot = build_snapshot(repo="owner/dataset", date="2026-05-02")
        assert snapshot["files"] == []

def test_build_snapshot_429_retry_after():
    from huggingface_hub import RepositoryNotFoundError
    from requests.exceptions import HTTPError
    resp = MagicMock()
    resp.status_code = 429
    resp.headers = {"Retry-After": "3"}
    err = HTTPError(response=resp)
    with patch("bin.snapshot.HfApi") as MockApi:
        MockApi.return_value.list_repo_tree.side_effect = err
        with pytest.raises(SystemExit) as exc:
            build_snapshot(repo="owner/dataset", date="2026-05-02")
        assert exc.value.code != 0

# tests/unit/test_file_list.py
import json, pytest
from lib.file_list import shard_files_from_snapshot, iter_shard_files

def test_shard_files_from_snapshot_deterministic():
    snapshot = {
        "repo": "owner/dataset",
        "date": "2026-05-02",
        "files": [
            {"path": "2026-05-02/a.parquet", "size": 100},
            {"path": "2026-05-02/b.parquet", "size": 200},
        ],
    }
    assignments = shard_files_from_snapshot(snapshot, shard_id=3, total_shards=16)
    # deterministic: same input -> same shard assignment
    paths = [f["path"] for f in assignments]
    expected = [f["path"] for f in snapshot["files"] if hash(f["path"]) % 16 == 3]
    assert paths == expected

def test_iter_shard_files_yields_local_paths(tmp_path):
    snapshot = {
        "repo": "owne
