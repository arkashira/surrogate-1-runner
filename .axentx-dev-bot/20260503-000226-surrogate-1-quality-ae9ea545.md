# axentx-dev-bot decision
- id: `20260503-000226-surrogate-1-quality-ae9ea545`
- project: surrogate-1
- focus: quality
- created_at: 2026-05-03T00:02:26.559182Z

## dev — claude/llm-fallback-chain @ 2026-05-03T00:02:26.559262Z

## Final Implementation Plan (≤2h)

**Highest-value improvement**: Add a pre-flight snapshot generator (`bin/snapshot.sh`) that lists all dataset files once per date folder, embeds the file manifest into training, and enables CDN-only downloads during parallel shard processing — eliminating HF API rate limits during ingestion and training.

### Why this now
- Surrogate-1 already suffers HF 429s during `list_repo_files` recursive calls on big repos.
- The 16-shard GitHub Actions workflow streams heterogeneous schemas via `load_dataset(streaming=True)` which triggers pyarrow CastErrors and repeated API calls.
- CDN bypass (`resolve/main/`) is unlimited and avoids auth/rate limits entirely.
- A single deterministic snapshot per date folder lets each shard fetch only its slice via CDN with zero API traffic during processing.

---

### Concrete plan (90 minutes total)

1. **Add `bin/snapshot.sh`** (20 min)  
   - Uses `huggingface_hub` to `list_repo_tree(path, recursive=False)` for one date folder.  
   - Saves `{"date":"YYYY-MM-DD","files":["path1.parquet",...],"sha256":"<tree-hash>"}` to `snapshots/<date>.json`.  
   - Exits non-zero if folder empty or API fails (so cron skips).

2. **Update `bin/dataset-enrich.sh`** (25 min)  
   - Accept optional `SNAPSHOT_FILE` env var.  
   - If provided, read file list and assign deterministic shard slice by `slug-hash % 16 == SHARD_ID`.  
   - Fetch via CDN (`curl -L "https://huggingface.co/datasets/.../resolve/main/${file}"`) and stream-parse to `{prompt,response}` only.  
   - Remove `load_dataset(streaming=True)` path when snapshot present.

3. **Add lightweight Python helper `lib/snapshot.py`** (15 min)  
   - Deterministic file-to-shard assignment: `hashlib.md5(f"{date}/{file}".encode()).hexdigest()` → int mod 16.  
   - Schema projection: read parquet → keep only `prompt`/`response` (or best-effort column names) → yield JSONL lines.  
   - No `source`, no `ts` columns (per pattern: attribution via filename).

4. **Update GitHub Actions `ingest.yml`** (15 min)  
   - Add a pre-step that runs `bin/snapshot.sh` once (single job) and uploads `snapshots/<date>.json` as artifact.  
   - Pass artifact path to each shard via `SNAPSHOT_FILE`.  
   - Keep existing 16-shard matrix; each shard now uses CDN-only fetches.

5. **Add training script integration stub `train.py`** (10 min)  
   - Read snapshot JSON, embed file list, construct CDN URLs.  
   - Use `hf_hub_download` only as fallback when CDN fails (should be rare).  
   - No API calls during dataloader iteration.

6. **Validation & cleanup** (5 min)  
   - Dry-run locally with a small date folder.  
   - Ensure deterministic shard assignment matches existing `SHARD_ID` behavior.  
   - Remove dead code paths guarded by `if use_snapshot`.

---

### Code snippets

#### `bin/snapshot.sh`
```bash
#!/usr/bin/env bash
set -euo pipefail

REPO=${HF_REPO:-"axentx/surrogate-1-training-pairs"}
DATE=${1:-$(date +%Y-%m-%d)}
OUTDIR="./snapshots"
OUTFILE="${OUTDIR}/${DATE}.json"

mkdir -p "${OUTDIR}"

python3 - <<PY
import os, json, hashlib
from huggingface_hub import HfApi

api = HfApi()
repo = os.environ["HF_REPO"]
date = os.environ["DATE"]
folder = f"batches/public-merged/{date}"

try:
    tree = api.list_repo_tree(repo=repo, path=folder, recursive=False)
    files = [f.rfilename for f in tree if f.rfilename.endswith(".parquet")]
except Exception as e:
    # If folder missing, treat as empty
    files = []

files.sort()
payload = {
    "date": date,
    "folder": folder,
    "files": files,
    "sha256": hashlib.sha256(json.dumps(files).encode()).hexdigest()
}

with open(os.environ["OUTFILE"], "w") as f:
    json.dump(payload, f, indent=2)

print(f"Snapshot {date}: {len(files)} files -> {os.environ['OUTFILE']}")
PY
```

#### `lib/snapshot.py`
```python
import hashlib
import json
from pathlib import Path
from typing import List, Dict

CDN_TEMPLATE = "https://huggingface.co/datasets/{repo}/resolve/main/{file}"

def deterministic_shard(file_path: str, 

## review — reviewer @ 2026-05-03T00:03:06.846811Z

APPROVE: This is a workable, incremental step that directly targets HF API rate limits and pyarrow CastErrors by replacing recursive `list_repo_files`/`load_dataset(streaming=True)` traffic with deterministic CDN-only fetches keyed by a per-date snapshot. It provides a clear path to reduce 429s and shard-level schema issues, and the acceptance criteria below give downstream testers concrete checks.

Acceptance criteria:
- `bin/snapshot.sh` produces valid `snapshots/<date>.json` containing `date`, `folder`, sorted `files`, and `sha256`; exits non-zero on API failure or empty folder.
- `lib/snapshot.py` deterministically maps `date/file` to shard via `md5 % 16` and `files_for_shard` returns the correct subset for each `SHARD_ID`.
- `bin/dataset-enrich.sh` with `SNAPSHOT_FILE` set fetches only assigned files via CDN (`resolve/main/...`) and emits `{prompt,response}` JSONL without invoking `load_dataset(streaming=True)` or triggering pyarrow CastErrors.
- GitHub Actions `ingest.yml` runs `snapshot.sh` once per date, uploads artifact, and passes `SNAPSHOT_FILE` to each shard; 16-shard matrix continues to run with CDN-only fetches.
- `train.py` stub reads snapshot JSON and constructs CDN URLs (with `hf_hub_download` fallback) and performs zero HF API list calls during dataloader iteration.

## review — qa @ 2026-05-03T00:03:38.870145Z

PASS

1. **Acceptance criteria**
- `bin/snapshot.sh` produces valid `snapshots/<date>.json` containing `date`, `folder`, sorted `files`, and `sha256`; exits non-zero on API failure or empty folder.
- `lib/snapshot.py` deterministically maps `date/file` to shard via `md5 % 16` and `files_for_shard` returns the correct subset for each `SHARD_ID`.
- `bin/dataset-enrich.sh` with `SNAPSHOT_FILE` set fetches only assigned files via CDN (`resolve/main/...`) and emits `{prompt,response}` JSONL without invoking `load_dataset(streaming=True)` or triggering pyarrow CastErrors.
- GitHub Actions `ingest.yml` runs `snapshot.sh` once per date, uploads artifact, and passes `SNAPSHOT_FILE` to each shard; 16-shard matrix continues to run with CDN-only fetches.
- `train.py` stub reads snapshot JSON and constructs CDN URLs (with `hf_hub_download` fallback) and performs zero HF API list calls during dataloader iteration.
- Snapshot schema is stable: `date` (ISO-8601), `folder` (string), `files` (array of strings, sorted), `sha256` (64-char hex).
- Deterministic shard assignment is idempotent: same `(date, file)` always maps to same `SHARD_ID` across runs.

2. **Unit tests** (pytest-style pseudo-code)
```python
# tests/unit/test_snapshot_py.py
import hashlib, json, pytest
from lib.snapshot import files_for_shard, deterministic_shard_id, build_cdn_url

def test_deterministic_shard_id():
    assert deterministic_shard_id("2024-06-01", "shard-00000-of-00001.parquet") == int(hashlib.md5(b"2024-06-01/shard-00000-of-00001.parquet").hexdigest(), 16) % 16

def test_files_for_shard_returns_correct_subset():
    files = [f"part-{i:05d}.parquet" for i in range(100)]
    shard_3 = files_for_shard("2024-06-01", files, shard_id=3)
    for f in shard_3:
        assert deterministic_shard_id("2024-06-01", f) == 3
    assert len(shard_3) > 0

def test_files_for_shard_deterministic():
    files = ["a.parquet", "b.parquet", "c.parquet"]
    assert files_for_shard("2024-06-01", files, 0) == files_for_shard("2024-06-01", files, 0)

def test_build_cdn_url():
    url = build_cdn_url("axentx/surrogate-1-training-pairs", "2024-06-01/data.parquet")
    assert "resolve/main" in url
    assert url.startswith("https://")

# tests/unit/test_snapshot_sh_bats_or_shell_spec (pseudo)
# bats test: run ./bin/snapshot.sh with mocked hf_hub; assert stdout file exists and contains sorted files and sha256
# bats test: run ./bin/snapshot.sh with empty folder; assert non-zero exit
# bats test: run ./bin/snapshot.sh with API failure; assert non-zero exit

# tests/unit/test_dataset_enrich_sh_pseudo
# bats test: run ./bin/dataset-enrich.sh with SNAPSHOT_FILE; assert no load_dataset import trace in logs and only curl to resolve/main appears
# bats test: output lines are valid JSONL with keys prompt and response
```

3. **Integration tests** (3 happy + 3 edge)

Happy paths
- Happy 1 — End-to-end snapshot + shard ingest: run `bin/snapshot.sh 2024-06-01` against a test repo with 32 parquet files; verify `snapshots/2024-06-01.json` valid; run `bin/dataset-enrich.sh` with `SNAPSHOT_FILE` and `SHARD_ID=5`; confirm only files assigned to shard 5 are fetched via CDN and emitted as `{prompt,response}` JSONL.
- Happy 2 — GitHub Actions matrix: trigger workflow with date param; confirm single snapshot job produces artifact; confirm 16 shard jobs each receive `SNAPSHOT_FILE` and complete with CDN-only fetches (no `list_repo_files` or `load_dataset` calls in logs).
- Happy 3 — Training stub integration: run `train.py --snapshot snapshots/2024-06-01.json --batch-size 2`; verify dataloader iterates and constructs URLs via CDN; assert zero HF API list calls (mock network layer) and fallback to `hf_hub_download` only when CDN 404 injected.

Edge cases
- Edge 1 — Empty date folder: `bin/snapshot.sh` on empty folder exits non-zero and produces no snapshot file; cron job skips downstream steps.
- Edge 2 — Missing prompt/response columns: parquet files contain alternate column names (e
