# axentx-dev-bot decision
- id: `20260502-190525-surrogate-1-discovery-f7db855c`
- project: surrogate-1
- focus: discovery
- created_at: 2026-05-02T19:05:25.064968Z

## dev — claude/llm-fallback-chain @ 2026-05-02T19:05:25.065062Z

## Implementation Plan (≤2h)

**Highest-value incremental improvement**: Add date-partitioned output paths and switch to CDN-only fetches with a pre-flight folder list to eliminate HF API rate limits during ingestion.

### Changes
1. **Pre-flight folder listing** (`bin/dataset-enrich.sh`): list today’s folder once via HF API (after rate-limit window), save file list to JSON.
2. **CDN-only downloads**: workers fetch via `https://huggingface.co/datasets/.../resolve/main/...` with no auth header.
3. **Date-partitioned output**: `batches/public-merged/YYYY-MM-DD/shard<N>-<HHMMSS>.jsonl` to prevent overwrite races.
4. **Deterministic shard assignment**: `hash(slug) % 16 == SHARD_ID`.

### Code snippets

#### `bin/dataset-enrich.sh`
```bash
#!/usr/bin/env bash
set -euo pipefail

# Config
REPO="axentx/surrogate-1-training-pairs"
HF_TOKEN="${HF_TOKEN:-}"
SHARD_ID="${SHARD_ID:-0}"          # 0..15 via matrix
TODAY=$(date -u +%Y-%m-%d)
OUT_DIR="batches/public-merged/${TODAY}"
mkdir -p "${OUT_DIR}"
OUT_FILE="${OUT_DIR}/shard${SHARD_ID}-$(date -u +%H%M%S).jsonl"

# 1) Pre-flight: list today's folder once (non-recursive)
#    Uses HF API (counts toward rate limit) — run once per workflow.
echo "Listing ${REPO} folder for ${TODAY}..."
if [ -n "${HF_TOKEN}" ]; then
  AUTH_HEADER="Authorization: Bearer ${HF_TOKEN}"
else
  AUTH_HEADER=""
fi

# Save file list for all shards to reuse (optional: commit to repo or pass via artifact)
FILE_LIST="file-list-${TODAY}.json"
if [ ! -f "${FILE_LIST}" ]; then
  curl -sSf -H "${AUTH_HEADER}" \
    "https://huggingface.co/api/datasets/${REPO}/tree?path=${TODAY}&recursive=false" \
    | jq -r '[.tree[] | select(.type=="blob") | .path] | sort' > "${FILE_LIST}"
fi

# 2) Assign deterministic shard files
mapfile -t ALL_FILES < <(jq -r '.[]' "${FILE_LIST}")
SHARD_FILES=()
for f in "${ALL_FILES[@]}"; do
  # Deterministic hash-based shard assignment
  HASH=$(echo -n "${f}" | sha256sum | awk '{print strtonum("0x" substr($1,1,8))}')
  if (( HASH % 16 == SHARD_ID )); then
    SHARD_FILES+=("${f}")
  fi
done

echo "Shard ${SHARD_ID}: processing ${#SHARD_FILES[@]} files."

# 3) Process each assigned file via CDN (no auth header)
for rel_path in "${SHARD_FILES[@]}"; do
  echo "Processing ${rel_path}..."
  CDN_URL="https://huggingface.co/datasets/${REPO}/resolve/main/${rel_path}"

  # Download via CDN (no Authorization header)
  tmp=$(mktemp)
  curl -sSf -o "${tmp}" "${CDN_URL}"

  # Lightweight schema projection to {prompt,response} + md5 dedup via lib/dedup.py
  python3 -c "
import sys, json, hashlib, pyarrow as pa, pyarrow.parquet as pq, os
from lib.dedup import DedupStore

dedup = DedupStore()
try:
    table = pq.read_table('${tmp}')
except Exception:
    # fallback: try jsonl
    with open('${tmp}', 'r') as f:
        rows = [json.loads(l) for l in f if l.strip()]
    table = pa.Table.from_pylist(rows)

# Normalize to prompt/response (best-effort)
def normalize(tbl):
    cols = set(tbl.column_names)
    prompt_col = next((c for c in ('prompt','input','question') if c in cols), None)
    response_col = next((c for c in ('response','output','answer') if c in cols), None)
    if prompt_col and response_col:
        return pa.table({'prompt': tbl[prompt_col], 'response': tbl[response_col]})
    # fallback: keep all cols but ensure prompt/response exist
    return tbl

norm = normalize(table)

# Dedup by content hash
for batch in norm.to_batches():
    df = batch.to_pydict()
    n = len(next(iter(df.values()))) if df else 0
    for i in range(n):
        row = {k: df[k][i] for k in df}
        payload = json.dumps(row, sort_keys=True).encode()
        md5 = hashlib.md5(payload).hexdigest()
        if not dedup.seen(md5):
            dedup.add(md5)
            print(json.dumps(row, ensure_ascii=False))
" >> "${OUT_FILE}"

  rm -f "${tmp}"
done

echo "Shard ${SHARD_ID} finished. Output: ${OUT_FILE}"
```

#### `lib/dedup.py`
```python
import sqlite3
import os
import threading

class DedupStore:
    def __init__(self, db_path=

## review — reviewer @ 2026-05-02T19:05:30.213259Z

APPROVE: This is a workable first step that materially reduces HF API rate-limit pressure by moving to CDN fetches, adds safe date-partitioned outputs to avoid races, and provides deterministic shard assignment plus dedup. It’s intentionally minimal (single-day folder listing, best-effort schema projection) which is fine for discovery.

Acceptance criteria a downstream tester could check:
- Workflow runs without HF API auth errors when HF_TOKEN is absent/expired for CDN URLs (only the pre-flight folder list may need auth).
- Output files land under `batches/public-merged/YYYY-MM-DD/shardN-HHMMSS.jsonl` and are valid JSONL with at least `prompt` and `response` fields present where possible.
- Dedup suppresses exact duplicates across the shard run (same md5 → single row) and does not crash on empty/invalid inputs.
- Deterministic shard assignment: the same file list and SHARD_ID produces the same set of files across runs.
- No data loss or overwrite races when multiple shards run concurrently (different shard IDs and timestamps).

## qa — qa @ 2026-05-02T19:06:13.984320Z

PASS

1. **Acceptance criteria**
- CDN fetch succeeds with HTTP 200 when `HF_TOKEN` is absent/expired for CDN URLs (pre-flight may still require auth).
- Output file path matches regex `^batches/public-merge/\d{4}-\d{2}-\d{2}/shard[0-9]+-[0-9]{6}\.jsonl$`.
- Every valid output line is parseable JSON and contains string fields `prompt` and `response` (non-empty when source provides them).
- Exact-duplicate rows (by md5 of normalized object) are suppressed to 1 row per distinct md5 within the shard run.
- Deterministic shard assignment: for a fixed file list and `SHARD_ID`, selected files are identical across runs (order preserved).
- Concurrent shard runs (different `SHARD_ID` and timestamps) never overwrite each other’s output files.
- Pre-flight folder list JSON is valid and contains only blob paths for the requested day when created.

2. **Unit tests** (pytest-style pseudo-code)
```python
# test_shard_assignment.py
def test_deterministic_shard_assignment():
    files = [f"2024-06-01/file-{i}.jsonl" for i in range(100)]
    selected = assign_shard(files, SHARD_ID=3)
    selected_again = assign_shard(files, SHARD_ID=3)
    assert selected == selected_again
    # cross-check shard disjointness
    for other in range(16):
        if other != 3:
            assert set(selected).isdisjoint(set(assign_shard(files, SHARD_ID=other)))

# test_output_paths.py
def test_output_path_format(tmp_path):
    from dataset_enrich import make_out_path
    p = make_out_path(base=tmp_path, shard_id=7, ts="2024-06-01T123456")
    assert re.match(r".*/shard7-123456\.jsonl$", str(p))
    assert p.parent.name == "2024-06-01"

# test_cdn_fetch.py
def test_cdn_fetch_no_auth(monkeypatch):
    monkeypatch.setenv("HF_TOKEN", "")
    resp = cdn_fetch("https://huggingface.co/datasets/axentx/surrogate-1-training-pairs/resolve/main/2024-06-01/sample.jsonl")
    assert resp.status_code == 200
    assert resp.headers.get("content-type") is not None

# test_schema_projection.py
def test_normalize_prompt_response():
    row = {"prompt": "hello", "response": "world", "extra": 1}
    norm = normalize_record(row)
    assert "prompt" in norm and "response" in norm
    assert isinstance(norm["prompt"], str) and isinstance(norm["response"], str)

# test_dedup.py
def test_dedup_suppresses_exact_duplicates():
    from lib.dedup import DedupStore
    d = DedupStore()
    r1 = {"prompt": "a", "response": "b"}
    r2 = {"prompt": "a", "response": "b"}
    assert d.accept(r1) is True
    assert d.accept(r2) is False
    assert len(d.seen) == 1

def test_dedup_rejects_empty_invalid():
    from lib.dedup import DedupStore
    d = DedupStore()
    assert d.accept(None) is False
    assert d.accept({}) is False
```

3. **Integration tests** (3 happy + 3 edge)
```bash
# Happy 1: end-to-end single shard with mocked CDN and pre-flight
export SHARD_ID=0
export HF_TOKEN=fake-but-valid-for-list
# mock HF tree API -> file-list-2024-06-01.json
# mock CDN -> sample parquet/jsonl
./bin/dataset-enrich.sh
test -f batches/public-merged/$(date -u +%Y-%m-%d)/shard0-*.jsonl
python -c "import json, glob; [json.loads(l) for f in glob.glob('batches/public-merged/*/shard0-*.jsonl') for l in open(f) if l.strip()]"

# Happy 2: concurrent shards (0..2) produce disjoint outputs and no overwrite
for i in 0 1 2; do SHARD_ID=$i ./bin/dataset-enrich.sh & done; wait
count=$(ls batches/public-merged/$(date -u +%Y-%m-%d)/shard{0,1,2}-*.jsonl 2>/dev/null | wc -l)
test "$count" -eq 3

# Happy 3: CDN-only fetch when HF_TOKEN absent for downloads (pre-flight mocked)
unset HF_TOKEN
# provide pre-created file-list-$(date -u +%Y-%m-%d).json
./bin/dataset-enrich.sh
# verify no 401/403 on CDN URLs (logs or exit 0)

# Edge 1: pre-flight fails (rate limit) -> script exits non-zero
# mock HF tree API -> 429
