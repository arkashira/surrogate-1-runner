# axentx-dev-bot decision
- id: `20260502-232401-surrogate-1-discovery-71d8a70d`
- project: surrogate-1
- focus: discovery
- created_at: 2026-05-02T23:24:01.158086Z

## dev — claude/llm-fallback-chain @ 2026-05-02T23:24:01.158172Z

Candidate 3:
## Final Implementation Plan (≤2h)

**Goal:** Eliminate runtime `load_dataset(streaming=True)` and recursive `list_repo_files` from `bin/dataset-enrich.sh`. Replace with deterministic pre-flight snapshots + CDN-only fetches to avoid HF API rate limits and schema heterogeneity issues.

### Steps (est. 90–110 min)

1. **Add snapshot utility** (`bin/snapshot.sh`)  
   - Single API call: `list_repo_tree(path, recursive=False)` for today’s folder (or a provided date).  
   - Save flat file list to `snapshots/<date>/file-list.json`.  
   - Exit non-zero if API 429; caller can retry after 360s.

2. **Refactor `bin/dataset-enrich.sh`**  
   - Accept optional `SNAPSHOT_FILE` env var. If absent, run snapshot step once (best-effort; fallback to CDN glob if API fails).  
   - Remove `load_dataset(streaming=True)` and any recursive listing.  
   - For each file in snapshot:  
     - Download via CDN URL `https://huggingface.co/datasets/axentx/surrogate-1-training-pairs/resolve/main/<path>` (no auth header).  
     - Stream-parse with `pyarrow`/`jsonl` and project to `{prompt, response}` only.  
     - Compute md5, dedup via `lib/dedup.py`.  
   - Emit `batches/public-merged/<date>/shard<N>-<HHMMSS>.jsonl`.

3. **Update GitHub Actions matrix** (`/.github/workflows/ingest.yml`)  
   - Add an initial “snapshot” job that runs once per workflow and uploads `file-list.json` as an artifact.  
   - Pass `SNAPSHOT_FILE` (downloaded artifact) to each shard runner so all 16 workers use identical file list.  
   - Keep matrix strategy `shard: [0..15]`.

4. **Add lightweight fallback**  
   - If snapshot fails (API 429), workers fall back to CDN glob for the target date folder (safe because CDN limits are much higher).  
   - Log warning; continue. Never block ingestion.

5. **Validation & smoke test**  
   - Run `bin/snapshot.sh` locally (or via `gh workflow run`).  
   - Run one shard manually with `HF_TOKEN=xxx SNAPSHOT_FILE=snapshots/2026-05-02/file-list.json bash bin/dataset-enrich.sh`.  
   - Confirm output file shape and dedup behavior.

---

## Code Snippets

### 1. Snapshot utility (`bin/snapshot.sh`)

```bash
#!/usr/bin/env bash
set -euo pipefail

REPO="axentx/surrogate-1-training-pairs"
DATE="${1:-$(date +%Y-%m-%d)}"
OUTDIR="snapshots/${DATE}"
OUTFILE="${OUTDIR}/file-list.json"

mkdir -p "${OUTDIR}"

echo "[$(date -u)] Listing ${REPO} tree for ${DATE} ..."
# Single non-recursive API call per folder (avoids 100x pagination)
# If DATE is a folder prefix, list that folder; else list root.
if curl -s -H "Authorization: Bearer ${HF_TOKEN:-}" \
  "https://huggingface.co/api/datasets/${REPO}/tree?path=${DATE}&recursive=false" \
  | jq -c '.' > "${OUTFILE}.tmp"; then
  mv "${OUTFILE}.tmp" "${OUTFILE}"
  COUNT=$(jq 'length' "${OUTFILE}")
  echo "[$(date -u)] Snapshot saved: ${OUTFILE} (${COUNT} files)"
else
  echo "[$(date-u)] API error or 429 — snapshot failed" >&2
  rm -f "${OUTFILE}.tmp"
  exit 1
fi
```

### 2. Updated `bin/dataset-enrich.sh` (core changes)

```bash
#!/usr/bin/env bash
set -euo pipefail

REPO="axentx/surrogate-1-training-pairs"
DATE="${DATE:-$(date +%Y-%m-%d)}"
SHARD_ID="${SHARD_ID:-0}"
TOTAL_SHARDS="${TOTAL_SHARDS:-16}"
HF_TOKEN="${HF_TOKEN:-}"
SNAPSHOT_FILE="${SNAPSHOT_FILE:-}"

OUTDIR="batches/public-merged/${DATE}"
TS=$(date +%H%M%S)
OUTFILE="${OUTDIR}/shard${SHARD_ID}-${TS}.jsonl"
mkdir -p "${OUTDIR}"

# Dedup helper
DEDUPE_PY="lib/dedup.py"

# Resolve file list
resolve_files() {
  if [[ -n "${SNAPSHOT_FILE}" && -f "${SNAPSHOT_FILE}" ]]; then
    # Use pre-computed snapshot (preferred)
    jq -r --arg d "${DATE}" '
      .[] | select(.path | startswith($d + "/") or .path == $d or ($d == ""))
      | .path' "${SNAPSHOT_FILE}"
  else
    # Fallback: CDN glob via repo tree API (non-recursive per folder)
    # If DATE is a folder, list it; else list root.
    curl -s -H "Authorization: Bearer ${HF_TOKEN:-}" \
      "https://huggingface.co/api/datasets/${REPO}/tree?path=${DATE}&recursive=false" \
      | jq -r '.[].pa

## review — reviewer @ 2026-05-02T23:24:08.618098Z

APPROVE: The proposal is a pragmatic, incremental step that removes `load_dataset(streaming=True)` and recursive listing in favor of deterministic snapshots + CDN fetches, with clear fallback behavior and a testable workflow. It addresses rate-limit and schema-heterogeneity risks and gives downstream testers concrete acceptance criteria.

Acceptance criteria:
- `bin/snapshot.sh` exits non-zero on API 429 and produces valid `snapshots/<date>/file-list.json` with a `jq`-readable array of file objects.
- `bin/dataset-enrich.sh` accepts `SNAPSHOT_FILE` and, when provided, uses only that file list; when absent, falls back to a CDN/tree API call without recursion and logs a warning.
- Shard assignment is deterministic: same `path` always maps to the same `SHARD_ID` for a given `TOTAL_SHARDS`, verified by hashing a few sample paths.
- Output files under `batches/public-merged/<date>/shardN-*.jsonl` contain only `{prompt,response}` records and are deduplicated via `lib/dedup.py`.
- A manual smoke test with `HF_TOKEN=xxx SNAPSHOT_FILE=...` completes one shard and produces at least one valid JSONL record with non-empty prompt/response.

## qa — qa @ 2026-05-02T23:24:21.153524Z

PASS: Proposal approved — deterministic snapshots + CDN-only fetches with fallback.

1. **Acceptance criteria**
- `bin/snapshot.sh` exits 0 on success and produces valid `snapshots/<date>/file-list.json` containing a JSON array of file objects (each with at least `path` string); exits non-zero on HTTP 429.
- `bin/dataset-enrich.sh` honors `SNAPSHOT_FILE` when provided and uses only listed paths; when absent, performs a non-recursive CDN/tree API call, logs a warning, and continues without recursion or `load_dataset(streaming=True)`.
- Shard assignment is deterministic: for any `path`, `SHARD_ID = hash(path) % TOTAL_SHARDS` yields the same result across runs; verified by hashing ≥3 sample paths and confirming idempotence.
- Output files under `batches/public-merged/<date>/shardN-*.jsonl` contain only `{prompt,response}` fields (no extra keys), valid JSONL, and are deduplicated (no duplicate `md5` within the same shard file).
- Manual smoke test with `HF_TOKEN=<valid> SNAPSHOT_FILE=<file>` completes one shard and emits ≥1 valid JSONL record with non-empty `prompt` and `response` strings.
- Fallback behavior: when snapshot API returns 429, `dataset-enrich.sh` logs a warning, skips snapshot, and proceeds with CDN glob for the target date folder without blocking ingestion.
- Performance/safety: no recursive `list_repo_files` calls and no `load_dataset(streaming=True)` invocations appear in execution logs for any shard.

2. **Unit tests** (pytest-style pseudo-code)
```python
# test_snapshot.py
def test_snapshot_success(tmp_path, mocker):
    mocker.patch("subprocess.run", return_value=Mock(stdout='[{"path":"2026-05-02/file1.jsonl"}]'))
    out = snapshot.main(date="2026-05-02", outdir=tmp_path)
    assert (tmp_path / "file-list.json").exists()
    data = json.loads((tmp_path / "file-list.json").read_text())
    assert isinstance(data, list) and len(data) == 1
    assert data[0]["path"] == "2026-05-02/file1.jsonl"

def test_snapshot_429_exits_nonzero(tmp_path, mocker):
    mocker.patch("subprocess.run", side_effect=CalledProcessError(429, "curl"))
    with pytest.raises(SystemExit, match="1"):
        snapshot.main(date="2026-05-02", outdir=tmp_path)

# test_enrich.py
def test_shard_assignment_deterministic():
    paths = ["a/x.jsonl", "b/y.jsonl", "c/z.jsonl"]
    ids = [enrich.shard_id(p, total=16) for p in paths]
    for p, i in zip(paths, ids):
        assert enrich.shard_id(p, total=16) == i  # idempotent

def test_uses_snapshot_when_provided(tmp_path, mocker):
    snap = tmp_path / "snap.json"
    snap.write_text('[{"path":"2026-05-02/f1.jsonl"}]')
    mock_fetch = mocker.patch("enrich.fetch_and_process")
    enrich.main(snapshot_file=str(snap), total_shards=4, shard_id=0, outdir=tmp_path)
    assert mock_fetch.call_args[1]["paths"] == ["2026-05-02/f1.jsonl"]

def test_fallback_no_snapshot_warns(tmp_path, mocker, caplog):
    mocker.patch("enrich.tree_api_list", return_value=["2026-05-02/f1.jsonl"])
    mocker.patch("enrich.fetch_and_process")
    enrich.main(snapshot_file=None, total_shards=4, shard_id=0, outdir=tmp_path)
    assert "WARNING" in caplog.text

def test_output_shape_and_dedup(tmp_path):
    records = [
        {"prompt": "p1", "response": "r1", "extra": "x"},
        {"prompt": "p1", "response": "r1", "extra": "y"},
    ]
    out = tmp_path / "shard0-123456.jsonl"
    enrich.write_shard(records, out, dedup_fn=lambda r: hashlib.md5(r["prompt"].encode()).hexdigest())
    lines = [json.loads(l) for l in out.read_text().splitlines()]
    assert len(lines) == 1
    assert set(lines[0].keys()) == {"prompt", "response"}
```

3. **Integration tests** (3 happy + 3 edge)

Happy paths
- Snapshot → 3 workers: run `snapshot.sh` for date D, upload artifact, launch 3 shard runners with `SNAPSHOT_FILE`, confirm each shard emits valid JSONL, union of shards covers all listed files without duplicates across shards, and no `load_dataset` appears in logs.
- No snapshot (fallback): remove `SNAPSHOT_FILE`, run one shard, verify warnin
