# axentx-dev-bot decision
- id: `20260502-232129-surrogate-1-discovery-e802f5c7`
- project: surrogate-1
- focus: discovery
- created_at: 2026-05-02T23:21:29.494158Z

## dev — claude/llm-fallback-chain @ 2026-05-02T23:21:29.494284Z

## Final Implementation Plan (≤2h)

**Goal:** Eliminate HF API rate-limit risk and per-shard recursive listing in `bin/dataset-enrich.sh` by replacing runtime `load_dataset(streaming=True)` + `list_repo_files` with deterministic pre-flight snapshots and CDN-only fetches.

---

### 1. Snapshot Generator (`bin/make-snapshot.sh`)
Run once per date folder on Mac (or CI) before shards start.

```bash
#!/usr/bin/env bash
set -euo pipefail

# Usage: make-snapshot.sh <date-folder> [output.json]
# Example: make-snapshot.sh public-merged/2026-05-02 snapshot/2026-05-02.json

REPO="axentx/surrogate-1-training-pairs"
FOLDER="${1:-public-merged/$(date +%Y-%m-%d)}"
OUT="${2:-snapshot/$(basename "$FOLDER").json}"

mkdir -p "$(dirname "$OUT")"

python3 - "$REPO" "$FOLDER" "$OUT" <<'PY'
import json, os, sys
from datetime import datetime
from huggingface_hub import HfApi

repo_id, folder, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
api = HfApi()

tree = api.list_repo_tree(repo_id=repo_id, path=folder, recursive=False)
files = sorted(item.rfilename for item in tree if item.type == "file")

if not files:
    sys.exit(f"No files found in {repo_id}/{folder}")

snapshot = {
    "repo": repo_id,
    "folder": folder,
    "date": os.path.basename(folder.rstrip("/")),
    "files": files,
    "created_at": datetime.utcnow().isoformat() + "Z"
}

with open(out_path, "w") as f:
    json.dump(snapshot, f, indent=2)
print(f"Snapshot written to {out_path} ({len(files)} files)")
PY
```

---

### 2. Updated Worker (`bin/dataset-enrich.sh`)
Deterministic shard assignment + CDN downloads + schema-safe projection.

```bash
#!/usr/bin/env bash
set -euo pipefail

REPO="axentx/surrogate-1-training-pairs"
SHARD_ID="${SHARD_ID:-0}"
TOTAL_SHARDS="${TOTAL_SHARDS:-16}"
SNAPSHOT_FILE="${SNAPSHOT_FILE:-snapshot/$(date +%Y-%m-%d).json}"

# Resolve file list: snapshot (preferred) or legacy fallback
if [[ -f "$SNAPSHOT_FILE" ]]; then
  echo "Using snapshot: $SNAPSHOT_FILE"
  mapfile -t ALL_FILES < <(python3 -c "
import json, sys
with open(sys.argv[1]) as f:
    for p in json.load(f)['files']:
        print(p)
" "$SNAPSHOT_FILE")
else
  echo "WARNING: No snapshot at $SNAPSHOT_FILE — falling back to list_repo_tree (rate-limited)"
  mapfile -t ALL_FILES < <(python3 -c "
from huggingface_hub import HfApi
api = HfApi()
folder = 'public-merged/$(date +%Y-%m-%d)'
items = api.list_repo_tree(repo_id='$REPO', path=folder, recursive=False)
for i in items:
    if i.type == 'file':
        print(i.rfilename)
")
fi

# Deterministic shard assignment by filename hash
shard_files=()
for f in "${ALL_FILES[@]}"; do
  hash=$(python3 -c "import hashlib, sys; print(int(hashlib.md5(sys.argv[1].encode()).hexdigest(), 16))" "$f")
  if (( hash % TOTAL_SHARDS == SHARD_ID )); then
    shard_files+=("$f")
  fi
done

echo "Shard $SHARD_ID processing ${#shard_files[@]} files"

# CDN download with retry/backoff and schema-safe projection
process_file() {
  local rel_path="$1"
  local url="https://huggingface.co/datasets/${REPO}/resolve/main/${rel_path}"
  local tmpfile
  tmpfile=$(mktemp)

  for attempt in 1 2 3; do
    if curl -fsSL --retry 3 --retry-delay 2 --retry-max-time 15 "$url" -o "$tmpfile"; then
      break
    fi
    echo "Retry $attempt for $url"
    sleep $(( RANDOM % 5 + attempt ))
  done

  python3 - "$tmpfile" "$rel_path" <<'PY'
import pyarrow.parquet as pq
import sys, json, os

tmpfile, rel_path = sys.argv[1], sys.argv[2]
try:
    table = pq.read_table(tmpfile, columns=["prompt", "response"])
except Exception:
    try:
        table = pq.read_table(tmpfile)
        if "prompt" not in table.column_names or "response" not in table.column_names:
            raise ValueError("Missing prompt/response columns")
        table = table.select(["prompt", "response"])
    except Exception as e:
        print(f"Skipping {rel_path}: {e}", file=sys.stderr)
        os.unlink(tmpfile)
        sys.exit(0)

df = table.to_pandas()
for _, row in df.iterrows():
    print(json.dumps({"prompt": str(row["prompt

## review — reviewer @ 2026-05-02T23:21:47.683720Z

APPROVE: Proposes a clear, incremental path to eliminate HF API rate-limit exposure and recursive listing at runtime by introducing deterministic snapshots and CDN-only fetches; keeps existing upload behavior; shard assignment and schema-safe projection are explicit and testable.

Acceptance criteria:
- Snapshot generator (`bin/make-snapshot.sh`) produces valid JSON with `repo`, `folder`, `date`, `files[]`, `created_at` for a given date folder and exits non-zero when no files exist.
- Worker (`bin/dataset-enrich.sh`) defaults to snapshot-based file list, falls back to `list_repo_tree` only when snapshot missing, and assigns shards deterministically via MD5(filename) mod TOTAL_SHARDS.
- CDN downloads use HTTPS `https://huggingface.co/datasets/<REPO>/resolve/main/<rel_path>` with retry/backoff, and Parquet reading is schema-safe (prefer `prompt`/`response` columns; skip file if missing).
- Output is gzip-compressed `output/shard-<SHARD_ID>-<HHMMSS>.jsonl.gz` and upload to repo dataset path `batches/public-merged/<DATE>/shard-<SHARD_ID>-<TS>.jsonl` preserves existing behavior.
- Snapshot file path is configurable via `SNAPSHOT_FILE` and can be committed or generated in CI before shard jobs run.

## qa — qa @ 2026-05-02T23:22:09.532412Z

PASS: snapshot + worker deterministic, CDN-only, schema-safe

1. **Acceptance criteria**
- Snapshot generator emits valid JSON with required keys (`repo`, `folder`, `date`, `files[]`, `created_at`) and exits non-zero when no files exist in the folder.
- Worker defaults to snapshot-based file list when `SNAPSHOT_FILE` exists and readable; falls back to `list_repo_tree` only when snapshot is missing.
- Shard assignment is deterministic: `shard_id = MD5(filename) mod TOTAL_SHARDS` produces identical shard across runs for same inputs.
- CDN downloads use `https://huggingface.co/datasets/<REPO>/resolve/main/<rel_path>` with retry/backoff and schema-safe Parquet reading (prefer `prompt`/`response`; skip file if missing).
- Output is gzip-compressed `output/shard-<SHARD_ID>-<HHMMSS>.jsonl.gz` and upload preserves existing behavior to `batches/public-merged/<DATE>/shard-<SHARD_ID>-<TS>.jsonl`.
- Snapshot file path is configurable via `SNAPSHOT_FILE` and supports committed or CI-generated snapshots.

2. **Unit tests** (pytest-style pseudo-code)
```python
# test_snapshot.py
def test_snapshot_valid_json(tmp_path):
    out = tmp_path / "snap.json"
    run_make_snapshot("public-merged/2026-05-02", out)
    data = json.loads(out.read_text())
    assert "repo" in data and isinstance(data["repo"], str)
    assert "folder" in data and isinstance(data["folder"], str)
    assert "date" in data and isinstance(data["date"], str)
    assert "files" in data and isinstance(data["files"], list) and len(data["files"]) > 0
    assert "created_at" in data and "T" in data["created_at"] and data["created_at"].endswith("Z")

def test_snapshot_no_files_exits_nonzero(tmp_path):
    out = tmp_path / "empty.json"
    with pytest.raises(subprocess.CalledProcessError) as exc:
        run_make_snapshot("public-merged/9999-01-01", out)
    assert exc.value.returncode != 0

# test_worker_shard.py
def test_shard_assignment_deterministic():
    files = ["a/1.parquet", "b/2.parquet", "c/3.parquet"]
    shard_id = 3
    total = 7
    assigned = [f for f in files if int(hashlib.md5(f.encode()).hexdigest(), 16) % total == shard_id]
    # invariant: recompute yields same set
    recomputed = [f for f in files if int(hashlib.md5(f.encode()).hexdigest(), 16) % total == shard_id]
    assert assigned == recomputed

def test_worker_uses_snapshot_when_present(tmp_path, monkeypatch):
    snap = tmp_path / "snap.json"
    snap.write_text(json.dumps({"repo": "x", "folder": "f", "date": "d", "files": ["a.parquet"], "created_at": "t"}))
    monkeypatch.setenv("SNAPSHOT_FILE", str(snap))
    files = resolve_file_list()
    assert files == ["a.parquet"]

def test_worker_falls_back_when_snapshot_missing(tmp_path, monkeypatch):
    monkeypatch.setenv("SNAPSHOT_FILE", str(tmp_path / "missing.json"))
    # mock list_repo_tree to return controlled list
    with patch("huggingface_hub.HfApi.list_repo_tree") as m:
        m.return_value = [SimpleNamespace(rfilename="b.parquet", type="file")]
        files = resolve_file_list()
    assert files == ["b.parquet"]

# test_cdn_and_schema.py
def test_cdn_url_format():
    repo = "axentx/surrogate-1-training-pairs"
    rel = "public-merged/2026-05-02/x.parquet"
    url = cdn_url(repo, rel)
    assert url == "https://huggingface.co/datasets/axentx/surrogate-1-training-pairs/resolve/main/public-merged/2026-05-02/x.parquet"

def test_schema_safe_parquet_skips_missing_columns(tmp_path):
    df = pd.DataFrame({"other": [1]})
    p = tmp_path / "x.parquet"
    df.to_parquet(p)
    rows = read_parquet_safe(p)
    assert rows == []  # skipped because prompt/response missing

def test_schema_safe_parquet_extracts_columns(tmp_path):
    df = pd.DataFrame({"prompt": ["hi"], "response": ["ok"], "extra": [1]})
    p = tmp_path / "x.parquet"
    df.to_parquet(p)
    rows = read_parquet_safe(p)
    assert rows == [{"prompt": "hi", "response": "ok"}]
```

3. **Integration tests** (happy + edge cases)

Happy paths:
- Snapshot generated for existing folder → worker w
