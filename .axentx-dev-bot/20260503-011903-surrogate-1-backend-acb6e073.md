# axentx-dev-bot decision
- id: `20260503-011903-surrogate-1-backend-acb6e073`
- project: surrogate-1
- focus: backend
- created_at: 2026-05-03T01:19:03.127542Z

## dev — claude/llm-fallback-chain @ 2026-05-03T01:19:03.127623Z

## Final synthesis (chosen parts + resolved conflicts)

**Core decision**: Use a **single non-recursive `list_repo_tree` per date folder**, then **CDN-only fetches** with **deterministic sharding** and **strict `{prompt,response}` projection**. This removes per-file auth, avoids 429s, and keeps memory bounded.

**Resolved conflicts**:
- Use **CDN as primary** (fast, no auth), **authenticated HF API only as fallback** (correctness when CDN unavailable).
- **Dedup is authoritative**: skip rows already present (bandwidth vs correctness → correctness wins).
- **Shard assignment**: deterministic (`hash(slug) % SHARD_TOTAL`) and stable across runs.
- **Output**: one `jsonl` per shard per date; single commit per shard; no partial commits.
- **Parquet handling**: stream via temp file (parquet requires seekable source) and project columns early.

---

## Implementation plan (≤2h)

1. **Generate file list once per date**  
   - Orchestrator or first runner calls `list_repo_tree` (non-recursive) for `public-raw/{DATE}/`.  
   - Save `file-list-{DATE}.json` and make it available to all runners (artifact or commit).

2. **Shard assignment**  
   - Deterministic: `int(md5(path)) % SHARD_TOTAL == SHARD_ID`.  
   - Ensures no overlap and stable across reruns.

3. **CDN fetch with authenticated fallback**  
   - Primary: `https://huggingface.co/datasets/{HF_REPO}/resolve/main/{path}` (no auth).  
   - On failure (non-200 or integrity error), fallback to authenticated `curl`/`requests` with token.

4. **Parse + project + dedup**  
   - For each file: stream parse (gzip/jsonl/parquet), keep only `prompt` and `response`.  
   - Compute per-row md5; check `dedup.db` (`hash_md5` primary key).  
   - `INSERT OR IGNORE`; skip if already present.

5. **Write and commit**  
   - Accumulate new rows into `batches/public-merged/{DATE}/shard{SHARD_ID}-{HHMMSS}.jsonl`.  
   - Single commit per shard; push to repo.

6. **Retry/backoff for 429**  
   - If CDN or API returns 429: exponential backoff with jitter; cap wait ~360s; retry up to N times.

7. **Validation & rollback**  
   - Dry-run one date + one shard; verify row counts, no 429s, dedup behavior.  
   - If CDN consistently fails, switch to authenticated fetch for that run and alert.

---

## Code artifacts

### `bin/dataset-enrich.sh` (updated)
```bash
#!/usr/bin/env bash
set -euo pipefail

HF_TOKEN=${HF_TOKEN:?missing}
HF_REPO=${HF_REPO:-axentx/surrogate-1-training-pairs}
DATE=${DATE:?missing}
SHARD_ID=${SHARD_ID:?missing}
SHARD_TOTAL=${SHARD_TOTAL:-16}
RUN_TS=$(date -u +%Y%m%d-%H%M%S)

OUT_DIR="batches/public-merged/${DATE}"
OUT_FILE="${OUT_DIR}/shard${SHARD_ID}-${RUN_TS}.jsonl"
TMP_DIR=$(mktemp -d)
cleanup() { rm -rf "${TMP_DIR}"; }
trap cleanup EXIT

mkdir -p "$(dirname "${OUT_FILE}")"

# File list: prefer pre-generated artifact; else one API call
FILE_LIST="${TMP_DIR}/file-list.json"
if [[ -f "file-list-${DATE}.json" ]]; then
  cp "file-list-${DATE}.json" "${FILE_LIST}"
else
  echo "Fetching file list for ${DATE}..."
  curl -sSf -H "Authorization: Bearer ${HF_TOKEN}" \
    "https://huggingface.co/api/datasets/${HF_REPO}/tree/public-raw/${DATE}?recursive=false" \
    > "${FILE_LIST}"
fi

mapfile -t FILES < <(jq -r '.[] | select(.type=="file") | .path' < "${FILE_LIST}")

# Deterministic shard assignment
assign_shard() {
  python3 -c "import hashlib; print(int(hashlib.md5(b'$1').hexdigest(), 16) % ${SHARD_TOTAL})"
}

# Process file via CDN (fallback to auth)
process_file() {
  local rel_path=$1
  local cdn_url="https://huggingface.co/datasets/${HF_REPO}/resolve/main/${rel_path}"
  local ext="${rel_path##*.}"
  python3 parse_and_project.py \
    --url "${cdn_url}" \
    --auth-url "https://huggingface.co/datasets/${HF_REPO}/resolve/main/${rel_path}" \
    --token "${HF_TOKEN}" \
    --ext "${ext}" \
    --shard-id "${SHARD_ID}" \
    --shard-total "${SHARD_TOTAL}" \
    --out "${TMP_DIR}/rows.jsonl" \
    --dedup-db "./lib/dedup.db"
}

> "${TMP_DIR}/rows.jsonl"
for f in "${FILES[@]}"; do
  s=$(ass

## review — reviewer @ 2026-05-03T01:19:10.401671Z

APPROVE: The proposal is a clear, workable step forward — it replaces per-file auth with deterministic CDN-first fetching, bounds memory, and provides dedup/commit semantics a downstream tester can verify.

Acceptance criteria:
- A dry-run on one date + one shard completes without 429s and produces `batches/public-merged/{DATE}/shard{N}-{TS}.jsonl` containing only `prompt`/`response` fields.
- Dedup is enforced: inserting an already-seen row (by md5) into `dedup.db` is ignored and not emitted to the shard output.
- Deterministic sharding: for a given `path`, `int(md5(path)) % SHARD_TOTAL` consistently assigns the same shard across runs.
- Fallback behavior: when CDN fetch fails (non-200 or integrity error), authenticated request is attempted and succeeds if credentials are valid.
- Single commit per shard: each run produces at most one commit for `shard{N}-{TS}.jsonl` and pushes to the repo; empty shard runs produce an empty file and no commit (or a no-op commit as implemented).

## qa — qa @ 2026-05-03T01:19:55.137450Z

PASS: criteria clear and implementable

1. **Acceptance criteria**
- Dry-run on one date + one shard completes with zero 429 responses and produces `batches/public-merged/{DATE}/shard{N}-{TS}.jsonl` containing only `prompt` and `response` fields.
- Dedup enforced: inserting a row whose md5 already exists in `dedup.db` is ignored and not emitted to the shard output file.
- Deterministic sharding: for any `path`, `int(md5(path)) % SHARD_TOTAL` assigns the same `SHARD_ID` across multiple runs.
- Fallback behavior: when CDN fetch returns non-200 or integrity error, an authenticated request is attempted and succeeds when credentials are valid.
- Single commit per shard: each non-empty run produces exactly one commit for `shard{N}-{TS}.jsonl`; empty runs produce no commit (or a no-op commit) and push is invoked only when there are new rows.
- Memory bounded: peak in-memory rows for a file do not exceed configurable `BATCH_SIZE` (streaming enforced).
- Parquet handling: parquet files are streamed via a seekable temp file and columns are projected to `prompt`/`response` before full materialization.

2. **Unit tests** (pytest-style pseudo-code)
```python
# shard_assignment.py
def test_shard_assignment_is_deterministic():
    for path in ["/a.jsonl", "/b.jsonl.gz", "/c.parquet"]:
        assert shard_for(path, total=16) == shard_for(path, total=16)

def test_shard_assignment_covers_all_shards():
    paths = [f"/file-{i}.jsonl" for i in range(1000)]
    assigned = {shard_for(p, 16) for p in paths}
    assert assigned == set(range(16))

# cdn_fetch.py
async def test_cdn_fetch_returns_bytes_on_200(mock_httpx):
    mock_httpx.get.return_value.status_code = 200
    mock_httpx.get.return_value.content = b"data"
    data = await cdn_fetch("https://cdn/file.jsonl")
    assert data == b"data"

async def test_cdn_fetch_falls_back_on_non_200(mock_httpx, mock_auth_fetch):
    mock_httpx.get.return_value.status_code = 404
    mock_auth_fetch.return_value = b"auth-data"
    data = await fetch_with_fallback("path", token="x")
    assert data == b"auth-data"
    assert mock_auth_fetch.called

async def test_cdn_fetch_retries_on_429_with_backoff(mock_httpx, clock):
    mock_httpx.get.side_effect = [
        httpx.Response(429),
        httpx.Response(429),
        httpx.Response(200, content=b"ok"),
    ]
    data = await cdn_fetch_with_retry("url", max_retries=5)
    assert data == b"ok"
    assert mock_httpx.get.call_count == 3

# dedup.py
def test_dedup_insert_ignores_existing_md5(tmp_path):
    db = tmp_path / "dedup.db"
    conn = sqlite3.connect(db)
    conn.execute("CREATE TABLE dedup (hash_md5 TEXT PRIMARY KEY)")
    conn.execute("INSERT INTO dedup VALUES ('abc123')")
    conn.commit()
    assert try_insert(conn, "abc123") is False   # ignored
    assert try_insert(conn, "def456") is True    # inserted
    conn.close()

# projection.py
def test_project_only_prompt_response_jsonl(tmp_path):
    src = tmp_path / "src.jsonl"
    src.write_text('{"prompt":"p","response":"r","extra":"x"}\n')
    rows = list(stream_project(src, fmt="jsonl", columns={"prompt","response"}))
    assert rows == [{"prompt":"p","response":"r"}]

def test_project_parquet_via_tempfile(tmp_path):
    import pyarrow as pa, pyarrow.parquet as pq
    tbl = pa.table({"prompt": ["p"], "response": ["r"], "extra": ["x"]})
    p = tmp_path / "x.parquet"
    pq.write_table(tbl, p)
    rows = list(stream_project(p, fmt="parquet", columns={"prompt","response"}))
    assert rows == [{"prompt":"p","response":"r"}]

# writer.py
def test_write_shard_only_when_rows(tmp_path):
    out = tmp_path / "shard0-120000.jsonl"
    commit = write_shard([], out)
    assert out.exists() is False or out.read_text() == ""
    assert commit is None or commit.is_empty

def test_write_shard_creates_single_commit(tmp_path):
    out = tmp_path / "shard0-120000.jsonl"
    rows = [{"prompt":"p","response":"r"}]
    commit = write_shard(rows, out)
    assert json.loads(out.read_text()) == rows[0]
    assert commit
