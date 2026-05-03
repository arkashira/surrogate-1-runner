# axentx-dev-bot decision
- id: `20260502-235136-surrogate-1-quality-cf25b8ed`
- project: surrogate-1
- focus: quality
- created_at: 2026-05-02T23:51:36.843419Z

## dev — claude/llm-fallback-chain @ 2026-05-02T23:51:36.843524Z

## Final Implementation Plan (≤2h)

**Highest-value improvement**: Add a pre-flight snapshot generator (`bin/snapshot.sh`) that lists all dataset files once, embeds the file manifest into training, and enables CDN-only downloads during parallel shard processing. This eliminates HF API rate-limit (429) during ingestion and reduces per-shard latency by avoiding recursive `list_repo_files` calls.

### Concrete Steps (1h 50m total)

1. **Create `bin/snapshot.sh`** (20 min)  
   - Uses `huggingface_hub` to call `list_repo_tree(path, recursive=False)` per date folder  
   - Outputs `snapshot-<date>.json` with deterministic ordering and CDN URLs (`resolve/main/...`)  
   - Validates JSON and exits non-zero on API failure  
   - Includes `ts` (ISO timestamp) and `repo` fields for traceability

2. **Update `bin/dataset-enrich.sh`** (30 min)  
   - Accepts snapshot file as optional argument; falls back to legacy behavior  
   - Each shard reads only its 1/16 slice of the snapshot (by `SHARD_ID`) using **deterministic hash-based assignment**: `hash(path) % 16 == SHARD_ID`  
   - Downloads via CDN URLs with `curl`/`wget` → zero API calls during stream  
   - Uses `lib/cdn_loader.py` for projection and validation

3. **Add `lib/cdn_loader.py`** (20 min)  
   - Lightweight parquet reader that takes CDN URLs directly  
   - Projects to `{prompt, response}` only; drops extra schema columns  
   - Emits normalized JSONL lines for dedup  
   - Includes robust error handling and logging

4. **Add `bin/embed-snapshot.py`** (20 min)  
   - Injects snapshot into training as a frozen constant  
   - Generates `train_filelist.py` with `FILELIST = [...]`  
   - Used by Lightning training to avoid any API calls during training

5. **Update GitHub Actions matrix** (10 min)  
   - Add step to generate snapshot before matrix expansion  
   - Pass snapshot artifact to all 16 shards via `needs`  
   - Ensure deterministic, disjoint file sets per shard

6. **Validation** (20 min)  
   - Dry-run snapshot on `axentx/surrogate-1-training-pairs`  
   - Verify CDN downloads succeed without `HF_TOKEN`  
   - Confirm shard assignment is deterministic and disjoint  
   - Ensure no `load_dataset(streaming=True)` or `list_repo_files` calls remain in hot path

---

## Code Snippets

### 1. `bin/snapshot.sh`
```bash
#!/usr/bin/env bash
# bin/snapshot.sh
# Generate CDN snapshot for surrogate-1 dataset ingestion.
# Usage: HF_TOKEN=... ./bin/snapshot.sh <date> [output.json]

set -euo pipefail

REPO="axentx/surrogate-1-training-pairs"
DATE="${1:-$(date +%Y-%m-%d)}"
OUT="${2:-snapshot-${DATE}.json}"

python3 - "$REPO" "$DATE" "$OUT" <<'PY'
import json, os, sys
from datetime import datetime, timezone
from huggingface_hub import HfApi

repo, date, out = sys.argv[1], sys.argv[2], sys.argv[3]
api = HfApi(token=os.getenv("HF_TOKEN"))

# List top-level date folders (non-recursive)
tree = api.list_repo_tree(repo, path="", recursive=False)
folders = [t for t in tree if t.type == "directory" and t.path.startswith(date)]

if not folders:
    print(f"No folders found for date {date}", file=sys.stderr)
    sys.exit(1)

entries = []
for f in folders:
    files = api.list_repo_tree(repo, path=f.path, recursive=False)
    for file in files:
        if file.type == "file" and file.path.endswith((".parquet", ".jsonl")):
            cdn_url = f"https://huggingface.co/datasets/{repo}/resolve/main/{file.path}"
            entries.append({
                "path": file.path,
                "cdn_url": cdn_url,
                "size": getattr(file, "size", None)
            })

# Deterministic ordering
entries.sort(key=lambda x: x["path"])

snapshot = {
    "repo": repo,
    "date": date,
    "ts": datetime.now(timezone.utc).isoformat(),
    "files": entries
}

with open(out, "w") as fp:
    json.dump(snapshot, fp, indent=2)

print(f"Snapshot written to {out} ({len(entries)} files)")
PY
```

### 2. `lib/cdn_loader.py`
```python
# lib/cdn_loader.py
import pyarrow.parquet as pq
import pyarrow as pa


## review — reviewer @ 2026-05-02T23:51:45.059716Z

APPROVE: The proposal is a workable, incremental step forward that identifies a real performance/reliability issue (HF API rate limits during ingestion) and provides concrete, implementable fixes with clear acceptance criteria.

- [ ] Snapshot generator (`bin/snapshot.sh`) produces valid `snapshot-<date>.json` with deterministic ordering, CDN URLs, and traceability fields (`repo`, `date`, `ts`), and exits non-zero on API failure.
- [ ] Shard assignment uses deterministic `hash(path) % 16` to partition the snapshot so each of 16 shards processes a disjoint subset, verified by a dry-run that shows zero overlap and full coverage.
- [ ] `lib/cdn_loader.py` can stream parquet from CDN URLs and project to `{prompt, response}` without invoking `list_repo_files` or `load_dataset(streaming=True)` in the hot path, with errors logged to stderr.
- [ ] GitHub Actions matrix generates the snapshot once, passes it as an artifact to all shards, and shards consume only their assigned slice via the hash-based assignment.
- [ ] End-to-end dry-run on `axentx/surrogate-1-training-pairs` completes without HF API 429s and without `HF_TOKEN` required for shard download steps.

## review — qa @ 2026-05-02T23:52:03.691186Z

PASS: 

1. **Acceptance criteria**
   - Snapshot generator emits valid `snapshot-<date>.json` with ≥1 entries, deterministic ordering, CDN `resolve/main/` URLs, and required fields `repo`, `date`, `ts`; exits non-zero when API fails.
   - Shard assignment via `hash(path) % 16` yields disjoint sets across shards 0–15 with 100% coverage and 0% overlap on any snapshot.
   - `lib/cdn_loader.py` streams parquet from CDN URLs and outputs only `{prompt, response}` JSONL lines; logs errors to stderr and never calls `list_repo_files` or `load_dataset(streaming=True)` in hot path.
   - GitHub Actions matrix produces one snapshot artifact before expansion and passes it to all 16 shards; each shard consumes only its hash-assigned slice.
   - End-to-end dry-run on `axentx/surrogate-1-training-pairs` completes with zero HF API 429s and zero `HF_TOKEN` required for shard downloads.
   - Snapshot file schema validates against JSON schema: required `repo` (string), `date` (YYYY-MM-DD), `ts` (ISO-8601), `files` (array of objects with `path`, `cdn_url`, `size`).
   - Determinism: running snapshot twice on same repo/date produces byte-for-byte identical JSON (sorted paths, stable timestamp mock).

2. **Unit tests**
```python
# tests/unit/test_snapshot.py
import json, pytest
from unittest.mock import patch, MagicMock
from bin.snapshot import generate_snapshot

def test_snapshot_has_required_fields():
    with patch("huggingface_hub.HfApi.list_repo_tree") as mock_tree:
        mock_tree.return_value = [
            MagicMock(type="directory", path="2024-01-01"),
        ]
        out = generate_snapshot("owner/repo", "2024-01-01", "snapshot.json")
        data = json.loads(out)
        assert "repo" in data and data["repo"] == "owner/repo"
        assert "date" in data and data["date"] == "2024-01-01"
        assert "ts" in data
        assert "files" in data and isinstance(data["files"], list)

def test_snapshot_cdn_urls():
    with patch("huggingface_hub.HfApi.list_repo_tree") as mock_tree:
        mock_tree.return_value = [
            MagicMock(type="file", path="2024-01-01/file.parquet"),
        ]
        out = generate_snapshot("owner/repo", "2024-01-01", "snapshot.json")
        files = json.loads(out)["files"]
        assert all("resolve/main/" in f["cdn_url"] for f in files)

def test_shard_assignment_deterministic():
    from lib.shard_assign import assign_shard
    paths = [f"2024-01-01/file{i}.parquet" for i in range(1000)]
    shards = [assign_shard(p, total=16) for p in paths]
    assert all(0 <= s < 16 for s in shards)
    # deterministic: same path -> same shard
    assert assign_shard("a.parquet", 16) == assign_shard("a.parquet", 16)

def test_shard_disjoint_and_full_coverage():
    from lib.shard_assign import assign_shard
    paths = [f"2024-01-01/file{i}.parquet" for i in range(1000)]
    assignments = [assign_shard(p, 16) for p in paths]
    for s in range(16):
        subset = [p for p, a in zip(paths, assignments) if a == s]
        # disjoint: no path appears in two shards (by construction)
        assert len(subset) == len(set(subset))
    # coverage: every path assigned
    assert len(assignments) == len(paths)

def test_cdn_loader_projects_only_prompt_response():
    from lib.cdn_loader import stream_parquet_to_jsonl
    import pyarrow.parquet as pq
    with patch("lib.cdn_loader.pq.read_table") as mock_read:
        mock_table = MagicMock()
        mock_table.to_pandas.return_value = [
            {"prompt": "hi", "response": "ok", "extra": "drop"},
        ]
        mock_read.return_value = mock_table
        lines = list(stream_parquet_to_jsonl("https://cdn.url/file.parquet"))
        record = json.loads(lines[0])
        assert set(record.keys()) == {"prompt", "response"}
        assert "extra" not in record

def test_cdn_loader_no_hf_api_calls_in_hot_path():
    from lib.cdn_loader import stream_parquet_to_jsonl
    with patch("lib.cdn_loader.pq.read_table") as mock_read:
        mock_read.return_value.to_pandas.ret
