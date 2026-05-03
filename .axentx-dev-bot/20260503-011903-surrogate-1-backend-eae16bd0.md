# axentx-dev-bot decision
- id: `20260503-011903-surrogate-1-backend-eae16bd0`
- project: surrogate-1
- focus: backend
- created_at: 2026-05-03T01:19:03.453693Z

## dev — claude/llm-fallback-chain @ 2026-05-03T01:19:03.453756Z

## Final synthesized plan (highest-value, <2h)

**Core fix**  
Replace recursive HF API ingestion and per-file authenticated fetches with:

1. One non-recursive `list_repo_tree(path=DATE, recursive=False)` per date folder.  
2. Deterministic shard assignment from the file list (hash-based).  
3. CDN-only downloads (`resolve/main/...`) with strict column projection (`prompt`, `response`).  
4. Lightweight dedup (in-process set + optional SQLite) and per-shard unique output files.

This removes 429 risk, eliminates per-file auth overhead, and keeps memory bounded.

---

## Concrete implementation plan (≤2h)

### 1) Update `bin/dataset-enrich.sh`
- Accept `DATE`, `SHARD_ID`, `SHARD_TOTAL`, `HF_REPO`, `HF_TOKEN` (already provided by matrix).  
- Run `list_repo_tree` once per runner (or pre-compute on Mac/CI and embed `file-list.json`).  
- Deterministic shard assignment by filename hash so workers never overlap.  
- Process only assigned files; stream with column projection; write `shard<SHARD_ID>-<HHMMSS>.jsonl`.  
- Upload each shard to `batches/public-merged/<DATE>/` with unique filename.

### 2) Worker logic (inline Python)
- Download via CDN:  
  `https://huggingface.co/datasets/<HF_REPO>/resolve/main/<path>` (no auth header).  
- Use `pyarrow.parquet.ParquetFile` with column projection to avoid mixed-schema `CastError`.  
- Normalize to `{prompt: str, response: str}`; skip empty rows.  
- Dedup by `md5(json.dumps(row, sort_keys=True))` (in-process set; optional SQLite for cross-runner dedup).  
- Write newline-delimited JSON.

### 3) Commit/upload strategy
- Each runner writes to a unique filename including `shard<SHARD_ID>-<TS>.jsonl`.  
- Keep only `{prompt, response}`; move attribution to filename/path (no extra columns).

### 4) Lightning Studio reuse (if used for downstream training)
- Before `.run()`, list `Teamspace.studios` and reuse a running studio to save quota.  
- If stopped, restart with `target.start(machine=Machine.L40S)` (prefer L40S on free tier; H200 only on paid clouds).

### 5) Validation (dry-run)
- Run on a single date folder and confirm:  
  - No recursive `list_repo_files`.  
  - No 429 during ingestion.  
  - Output schema is exactly `{prompt, response}`.

---

## Final code snippets

### `bin/dataset-enrich.sh`
```bash
#!/usr/bin/env bash
set -euo pipefail

: "${DATE:?Need DATE}"
: "${SHARD_ID:?Need SHARD_ID}"
: "${SHARD_TOTAL:?Need SHARD_TOTAL}"
: "${HF_REPO:?Need HF_REPO, e.g. axentx/surrogate-1-training-pairs}"
: "${HF_TOKEN:?Need HF_TOKEN}"

WORKDIR=$(mktemp -d)
cd "$WORKDIR"

# 1) Non-recursive tree listing for the date folder
python3 - <<PY
import os, json
from huggingface_hub import HfApi
api = HfApi(token=os.environ["HF_TOKEN"])
tree = api.list_repo_tree(
    repo_id=os.environ["HF_REPO"],
    path=f"public-merged/${DATE}",
    recursive=False
)
files = [f.rfilename for f in tree if f.rfilename.endswith(".parquet")]
with open("file-list.json", "w") as f:
    json.dump(files, f)
PY

# 2) Deterministic shard assignment by filename hash
mapfile -t ALL_FILES < <(jq -r '.[]' file-list.json)
if (( ${#ALL_FILES[@]} == 0 )); then
  echo "No parquet files for ${DATE}"
  exit 0
fi

declare -a MY_FILES
for f in "${ALL_FILES[@]}"; do
  h=$(echo -n "$f" | cksum | awk '{print $1}')
  b=$(( h % SHARD_TOTAL ))
  if (( b == SHARD_ID )); then
    MY_FILES+=("$f")
  fi
done

echo "Shard ${SHARD_ID}/${SHARD_TOTAL} processing ${#MY_FILES[@]}/${#ALL_FILES[@]} files"

# 3) Process via CDN + column projection
TS=$(date -u +%H%M%S)
OUT="shard${SHARD_ID}-${TS}.jsonl"

python3 - <<PY
import os, json, hashlib, sys
import pyarrow.parquet as pq
import requests
from tqdm import tqdm

HF_REPO = os.environ["HF_REPO"]
OUT = sys.argv[1]
FILES = sys.argv[2:]

def download_parquet(path):
    url = f"https://huggingface.co/datasets/{HF_REPO}/resolve/main/{path}"
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    return r.content

def normalize_record(rec):
    prompt = str(rec.get("prompt", rec.get("input", ""))

## review — reviewer @ 2026-05-03T01:19:11.849324Z

APPROVE: The plan and script are a workable, incremental improvement that directly addresses the stated risks (429s, per-file auth, unbounded memory) and can be validated by a downstream tester. It replaces recursive/expensive ingestion with a single non-recursive tree list, deterministic sharding, CDN-only downloads, column projection, and bounded dedup — all of which are reasonable and implementable within the 2-hour scope.

Acceptance criteria:
- `bin/dataset-enrich.sh` accepts DATE, SHARD_ID, SHARD_TOTAL, HF_REPO, HF_TOKEN and exits 0 when no parquet files exist for the date.
- A single non-recursive `list_repo_tree(path=DATE, recursive=False)` is used per runner (no recursive listing).
- Shard assignment is deterministic by filename hash (mod SHARD_TOTAL) so workers do not overlap.
- Downloads use CDN URLs (`resolve/main/...`) with column projection limited to `prompt`/`response` (or acceptable fallbacks) and produce `{prompt: str, response: str}` rows.
- Output is written to a unique file `shard<SHARD_ID>-<TS>.jsonl` and contains newline-delimited JSON with no extra columns; dedup is performed in-process (md5 of normalized row).

## qa — qa @ 2026-05-03T01:19:40.069685Z

PASS: criteria clear and implementable within scope

1. **Acceptance criteria**
- Script exits 0 when `list_repo_tree` returns zero parquet files for the given DATE.
- Exactly one non-recursive `list_repo_tree(path=DATE, recursive=False)` call is made per runner (no recursive listing).
- Deterministic shard assignment: filename hash mod SHARD_TOTAL equals SHARD_ID for assigned files; no overlap across SHARD_TOTAL runners for the same file list.
- Downloads use CDN URLs (`resolve/main/...`) with column projection limited to `prompt`/`response`; produced rows are exactly `{prompt: str, response: str}` (non-null strings, empty rows skipped).
- Output file name matches `shard<SHARD_ID>-<TS>.jsonl` (TS format `HHMMSS` or ISO-ish) and contains newline-delimited JSON with no extra columns; in-process dedup ensures no duplicate rows within the shard.

2. **Unit tests** (pytest-style pseudo-code)
```python
# test_shard_assignment.py
def test_deterministic_shard_assignment():
    files = ["public-merged/2024-01-01/a.parquet", "public-merged/2024-01-01/b.parquet"]
    total = 3
    assignments = {f: shard_id_for_file(f, total) for f in files}
    assert len(set(assignments.values())) <= total
    for f, sid in assignments.items():
        assert 0 <= sid < total
        assert shard_id_for_file(f, total) == sid  # deterministic

def test_no_overlap_across_shards():
    files = [f"public-merged/2024-01-01/{i}.parquet" for i in range(100)]
    total = 7
    by_shard = {s: [] for s in range(total)}
    for f in files:
        by_shard[shard_id_for_file(f, total)].append(f)
    # every file assigned exactly once across shards
    assigned = sum(by_shard.values(), [])
    assert sorted(assigned) == sorted(files)

# test_cdn_download_and_projection.py
def test_cdn_url_format():
    url = cdn_url("owner/repo", "public-merged/2024-01-01/a.parquet")
    assert url.startswith("https://huggingface.co/datasets/")
    assert "/resolve/main/" in url
    assert "token" not in url.lower()

def test_column_projection():
    # mock ParquetFile with extra columns
    rows = list(stream_parquet_with_projection(mock_parquet_with_extra_cols(), {"prompt", "response"}))
    for r in rows:
        assert set(r.keys()) == {"prompt", "response"}
        assert isinstance(r["prompt"], str) and isinstance(r["response"], str)

# test_dedup.py
def test_inprocess_dedup():
    rows = [
        {"prompt": "hi", "response": "hello"},
        {"prompt": "hi", "response": "hello"},
        {"prompt": "bye", "response": "good"},
    ]
    out = list(dedup_rows(rows))
    assert len(out) == 2
    assert {"hi", "bye"} == {r["prompt"] for r in out}

# test_script_exit_codes.py
def test_exit_zero_when_no_parquet(tmp_path, monkeypatch):
    monkeypatch.setenv("DATE", "2024-01-01")
    monkeypatch.setenv("SHARD_ID", "0")
    monkeypatch.setenv("SHARD_TOTAL", "1")
    monkeypatch.setenv("HF_REPO", "owner/repo")
    monkeypatch.setenv("HF_TOKEN", "x")
    # mock list_repo_tree to return []
    result = run_script()
    assert result.exit_code == 0
```

3. **Integration tests**
- Happy: Single shard (SHARD_TOTAL=1) on a date folder with 3 parquet files → one `shard0-*.jsonl` produced with expected rows and schema `{prompt, response}`.
- Happy: Multiple shards (SHARD_TOTAL=3) on same date folder → three output files; union of rows equals full deduped dataset; no row appears in more than one shard.
- Happy: CDN download with column projection on mixed-schema parquet (extra columns, nested) → script completes and outputs only `{prompt, response}` strings.
- Edge: DATE folder contains zero parquet files → script exits 0 and produces no output shards.
- Edge: Duplicate rows across parquet files → output shard contains no duplicates (in-process dedup effective).
- Edge: Malformed row (non-string prompt/response or missing key) → row is skipped and does not appear in output.

4. **Risk register**
- Risk: HF API 429 on `list_repo_tree` (single call) could block ingestion.  
  Detect: Monitor
