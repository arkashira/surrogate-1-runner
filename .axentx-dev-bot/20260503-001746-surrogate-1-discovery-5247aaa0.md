# axentx-dev-bot decision
- id: `20260503-001746-surrogate-1-discovery-5247aaa0`
- project: surrogate-1
- focus: discovery
- created_at: 2026-05-03T00:17:46.771409Z

## dev — claude/llm-fallback-chain @ 2026-05-03T00:17:46.771520Z

## Final Implementation Plan — Pre-flight snapshot generator for surrogate-1

**Single highest-value improvement**: Add a deterministic pre-flight manifest (`bin/snapshot.sh`) that lists dataset files **once per date folder** and emits a CDN-only file manifest so training can fetch shards with **zero HF API calls**, eliminating 429 risk and enabling reproducible shard selection.

**Why this now**
- Removes `list_repo_tree`/`load_dataset` API hammer during training.
- Fits ≤2h: one new script + small, backward-compatible changes to `dataset-enrich.sh`.
- Reuses existing cron/workflow model; no infra changes.

---

### Changes (merged + reconciled)

1. **Add `bin/hf_list_tree.py`** (canonical, testable helper)  
   Thin wrapper around `huggingface_hub.list_repo_tree` used by `snapshot.sh`. Keeps Bash simple and enables unit tests.

2. **Add `bin/snapshot.sh`**  
   - Inputs: `REPO_OWNER`, `REPO_NAME`, `DATE` (e.g. `2026-05-03`), optional `OUT_JSON`.  
   - Single API call per date folder (`recursive=False`).  
   - Emits deterministic JSON manifest:
     - `repo`, `date`, `generated_at_utc`, `count`, `files[]` sorted by path, `sha256_manifest`.  
   - Validation: non-empty, sorted, no duplicate paths, CDN URLs reachable (optional curl check).  
   - Exits non-zero on API failure so CI can retry with backoff.

3. **Update `bin/dataset-enrich.sh`** (backward-compatible)  
   - Accept optional `MANIFEST_FILE`.  
   - If present and valid, workers read CDN URLs from manifest instead of calling HF API.  
   - Fallback to current listing behavior when absent.

4. **(Optional) Training script guidance**  
   - Read `MANIFEST_FILE` from env.  
   - Stream from CDN URLs directly (e.g. `requests`/`aiohttp` or `hf_hub_download` with `repo_type="dataset"` and `repo_id` + `filename`).  
   - No `load_dataset` or `list_repo_files` during training.

---

### Implementation details

#### `bin/hf_list_tree.py`
```python
#!/usr/bin/env python3
"""
List top-level files in a repo path (non-recursive) using huggingface_hub.
Usage:
  HF_TOKEN=... ./bin/hf_list_tree.py <owner> <repo> <path>

Outputs JSON list of objects:
  [{"path": "...", "size": ...}, ...]
"""
import json
import os
import sys
from huggingface_hub import HfApi

def main() -> None:
    if len(sys.argv) != 4:
        print("Usage: hf_list_tree.py <owner> <repo> <path>", file=sys.stderr)
        sys.exit(1)
    owner, repo, path = sys.argv[1], sys.argv[2], sys.argv[3]
    api = HfApi(token=os.environ.get("HF_TOKEN"))
    entries = api.list_repo_tree(
        repo=f"{owner}/{repo}",
        path=path,
        repo_type="dataset",
        recursive=False,
    )
    files = []
    seen = set()
    for e in entries:
        if e.type == "file":
            if e.path in seen:
                print(f"Duplicate path in listing: {e.path}", file=sys.stderr)
                sys.exit(1)
            seen.add(e.path)
            files.append({"path": e.path, "size": getattr(e, "size", None)})
    # Deterministic ordering
    files.sort(key=lambda x: x["path"])
    print(json.dumps(files, separators=(",", ":")))

if __name__ == "__main__":
    main()
```

Make executable:
```bash
chmod +x bin/hf_list_tree.py
```

---

#### `bin/snapshot.sh`
```bash
#!/usr/bin/env bash
# bin/snapshot.sh
# Usage: HF_TOKEN=... ./bin/snapshot.sh <owner> <repo> <date> [out_json]
#
# Produces manifest: batches/public-merged/<date>/file-manifest-<YYYYMMDD>.json
# Format:
# {
#   "repo": "owner/repo",
#   "date": "YYYY-MM-DD",
#   "generated_at_utc": "...",
#   "count": N,
#   "sha256_manifest": "...",
#   "files": [
#     {"path": "...", "cdn_url": "...", "size": ...},
#     ...
#   ]
# }

set -euo pipefail

REPO_OWNER="${1:-axentx}"
REPO_NAME="${2:-surrogate-1-training-pairs}"
DATE="${3:-$(date +%F)}"
OUTDIR="batches/public-merged/${DATE}"
OUTFILE="${4:-${OUTDIR}/file-manifest-$(echo "$DATE" | tr -d '-').json}"

mkdir -p "$OUTDIR"

echo "[$(date -u +%FT%T%z)] snapshot: listing ${REPO_OWNER}/${REPO_NAME} path='${DATE}/' rec

## review — reviewer @ 2026-05-03T00:19:23.626539Z

APPROVE: Deterministic pre-flight manifest is a workable, incremental step that removes HF API hammer during training and provides a testable path to reproducible shard selection.

Acceptance criteria:
- `bin/hf_list_tree.py` is executable, accepts `<owner> <repo> <path>`, outputs sorted JSON list of file objects, and exits non-zero on API/duplicate-path errors.
- `bin/snapshot.sh` accepts `REPO_OWNER`, `REPO_NAME`, `DATE`, optional `OUT_JSON`, performs a single non-recursive `list_repo_tree` call, and emits a deterministic manifest with `repo`, `date`, `generated_at_utc`, `count`, sorted `files[]`, `cdn_url`, and `sha256_manifest`; exits non-zero on API failure or empty listing.
- `bin/dataset-enrich.sh` accepts optional `MANIFEST_FILE`; when present and valid, workers consume CDN URLs from the manifest and skip HF listing calls; otherwise falls back to existing behavior without breaking existing workflows.
- Manifest validation checks: non-empty, sorted paths, no duplicate paths, and optional CDN reachability (curl HEAD) with clear error output and non-zero exit on failure.
- Reproducibility: manifest generation is deterministic (same inputs → same JSON bytes), and `sha256_manifest` covers the canonical file list so downstream jobs can verify integrity before training shard selection.

## qa — qa @ 2026-05-03T00:20:05.493078Z

PASS: deterministic pre-flight manifest plan is approved and testable.

1. **Acceptance criteria**
- `bin/hf_list_tree.py` is executable, accepts `<owner> <repo> <path>`, outputs sorted JSON list of file objects, and exits non-zero on API/duplicate-path errors.
- `bin/snapshot.sh` accepts `REPO_OWNER`, `REPO_NAME`, `DATE`, optional `OUT_JSON`, performs a single non-recursive `list_repo_tree` call, and emits a deterministic manifest with `repo`, `date`, `generated_at_utc`, `count`, sorted `files[]`, `cdn_url`, and `sha256_manifest`; exits non-zero on API failure or empty listing.
- `bin/dataset-enrich.sh` accepts optional `MANIFEST_FILE`; when present and valid, workers consume CDN URLs from the manifest and skip HF listing calls; otherwise falls back to existing behavior without breaking existing workflows.
- Manifest validation checks: non-empty, sorted paths, no duplicate paths, and optional CDN reachability (curl HEAD) with clear error output and non-zero exit on failure.
- Reproducibility: manifest generation is deterministic (same inputs → same JSON bytes), and `sha256_manifest` covers the canonical file list so downstream jobs can verify integrity before training shard selection.
- CDN URLs in manifest follow the pattern `https://cdn-lfs.huggingface.co/...` (or equivalent) and are reachable (HTTP 200/206/403-for-auth) within a timeout.
- No HF API calls occur during training when `MANIFEST_FILE` is provided and valid (observable via mocked network or audit log).

2. **Unit tests**
```python
# tests/unit/test_hf_list_tree.py
import json, subprocess, os, pytest

def test_hf_list_tree_executable():
    assert os.access("bin/hf_list_tree.py", os.X_OK)

def test_hf_list_tree_usage():
    proc = subprocess.run(["python3", "bin/hf_list_tree.py"], capture_output=True, text=True)
    assert proc.returncode != 0
    assert "Usage" in proc.stderr

def test_hf_list_tree_output_sorted_and_unique(monkeypatch):
    from unittest.mock import MagicMock
    mock_entries = [
        MagicMock(type="file", path="z/a.json", size=100),
        MagicMock(type="file", path="a/b.json", size=200),
        MagicMock(type="file", path="a/c.json", size=150),
    ]
    monkeypatch.setattr("huggingface_hub.HfApi.list_repo_tree", lambda *a, **k: mock_entries)
    proc = subprocess.run(
        ["python3", "bin/hf_list_tree.py", "owner", "repo", "data/"],
        capture_output=True, text=True, env={**os.environ, "HF_TOKEN": "x"}
    )
    assert proc.returncode == 0
    out = json.loads(proc.stdout)
    paths = [f["path"] for f in out]
    assert paths == sorted(paths)
    assert len(paths) == len(set(paths))

def test_hf_list_tree_duplicate_exits_nonzero(monkeypatch):
    from unittest.mock import MagicMock
    mock_entries = [
        MagicMock(type="file", path="a.json", size=100),
        MagicMock(type="file", path="a.json", size=100),
    ]
    monkeypatch.setattr("huggingface_hub.HfApi.list_repo_tree", lambda *a, **k: mock_entries)
    proc = subprocess.run(
        ["python3", "bin/hf_list_tree.py", "owner", "repo", "data/"],
        capture_output=True, text=True, env={**os.environ, "HF_TOKEN": "x"}
    )
    assert proc.returncode != 0
    assert "Duplicate" in proc.stderr

# tests/unit/test_snapshot.py (pytest-style for shell via subprocess)
def test_snapshot_sh_outputs_required_fields(tmp_path, monkeypatch):
    out = tmp_path / "manifest.json"
    # Mock hf_list_tree.py to return deterministic files
    mock_script = tmp_path / "hf_list_tree.py"
    mock_script.write_text("""
import json, sys
print(json.dumps([{"path": "2026-05-03/a.json", "size": 100}, {"path": "2026-05-03/b.json", "size": 200}]))
""")
    monkeypatch.setenv("PATH", f"{tmp_path}:{os.environ['PATH']}")
    monkeypatch.setenv("REPO_OWNER", "owner")
    monkeypatch.setenv("REPO_NAME", "repo")
    monkeypatch.setenv("DATE", "2026-05-03")
    proc = subprocess.run(["bash", "bin/snapshot.sh"], capture_output=True, text=True, env=dict(os.environ, OUT_JSON=str(out)))
    assert p
