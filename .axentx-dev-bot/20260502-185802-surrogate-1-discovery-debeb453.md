# axentx-dev-bot decision
- id: `20260502-185802-surrogate-1-discovery-debeb453`
- project: surrogate-1
- focus: discovery
- created_at: 2026-05-02T18:58:02.917969Z

## dev — claude/llm-fallback-chain @ 2026-05-02T18:58:02.918047Z

## Highest-value incremental improvement (≤2h)
Ship deterministic date-partitioned ingestion with CDN-bypass and a pre-flight file list to eliminate redundant API calls, overwrite races, and rate-limit pressure.

### Why this first
- Fixes noisy history and training instability (deterministic `YYYY/MM/DD` outputs).
- Cuts HF API traffic during ingestion (single Mac-side `list_repo_tree` → JSON; workers use CDN URLs).
- Enables safe re-runs and shard isolation without collisions.
- Fits existing 16-shard matrix; minimal code change, high leverage.

---

## Implementation plan

1. Add `YYYY/MM/DD` partition logic to output path
   - Use UTC date of run: `batches/public-merged/2026/05/02/shard03-142311.jsonl`
   - Include shard id + HHMMSS to keep filenames unique and monotonic.

2. Pre-flight file list (Mac orchestrator)
   - One-time (or cron-start) call: `list_repo_tree(recursive=False)` per date folder on upstream dataset repo.
   - Save to `file-list-YYYYMMDD.json` (array of `{"path":..., "sha256":...}`).
   - Commit or upload as workflow artifact; workers consume it instead of listing repos.

3. CDN-only downloads in workers
   - Replace `hf_hub_download`/`load_dataset` calls with direct CDN fetch:
     `https://huggingface.co/datasets/axentx/surrogate-1-training-pairs/resolve/main/<path>`
   - No Authorization header; avoids API rate limits during streaming.

4. Deterministic shard assignment
   - Keep existing `slug-hash % 16 == SHARD_ID` logic.
   - Map each file from the pre-flight list to a shard; workers process only assigned paths.

5. Idempotent uploads
   - Target path includes date+shard+timestamp; never overwrite previous runs.
   - Workers skip upload if target file already exists (optional guard via `hf_hub_file_exists`).

6. Workflow changes
   - Add optional `file_list` input (artifact or repo path) to `ingest.yml`.
   - If absent, fall back to legacy live list (backwards compatible).
   - Pass `RUN_DATE` and `SHARD_ID` via matrix; compose output path in `dataset-enrich.sh`.

7. Validation & rollout
   - Dry-run one shard locally with mocked file list.
   - Check output path format and CDN fetch success.
   - Trigger full 16-shard run; confirm no 429s and date folders appear.

---

## Code snippets

### bin/dataset-enrich.sh (excerpt)
```bash
#!/usr/bin/env bash
set -euo pipefail

# Inputs
: "${HF_TOKEN:?required}"
: "${SHARD_ID:?required (0-15)}"
: "${RUN_DATE:?YYYY-MM-DD, e.g. 2026-05-02}"
: "${FILE_LIST:?path to file-list-YYYYMMDD.json (or 'live')}"

export HF_HOME="${HF_HOME:-$HOME/.cache/huggingface}"
export HF_ENDPOINT="${HF_ENDPOINT:-https://huggingface.co}"

REPO="axentx/surrogate-1-training-pairs"
DATE_PART=$(echo "$RUN_DATE" | tr -d '-')
YEAR=$(echo "$RUN_DATE" | cut -d- -f1)
MONTH=$(echo "$RUN_DATE" | cut -d- -f2)
DAY=$(echo "$RUN_DATE" | cut -d- -f3)
TS=$(date -u +"%H%M%S")
OUT_NAME="shard$(printf '%02d' "$SHARD_ID")-${TS}.jsonl"
OUT_PATH="batches/public-merged/${YEAR}/${MONTH}/${DAY}/${OUT_NAME}"

log() { echo "[$(date -u -Iseconds)] $*"; }

# Resolve files to process
resolve_files() {
  if [ "$FILE_LIST" = "live" ]; then
    log "WARN: using live HF API (slow, rate-limited)"
    python -c "
import json, os
from huggingface_hub import list_repo_tree
files = [f.rfilename for f in list_repo_tree(repo_id='$REPO', recursive=False)]
print(json.dumps(files))
"
  else
    # Expect file-list-YYYYMMDD.json as array of objects with .path
    python -c "import json,sys; d=json.load(open('$FILE_LIST')); print(json.dumps([x['path'] for x in d]))"
  fi
}

# Deterministic shard assignment by filename slug
assign_shard() {
  local file="$1"
  # stable hash -> 0..15
  local hash
  hash=$(echo -n "$file" | sha256sum | tr -d ' -' | xxd -r -p | od -An -t u8 | tr -d ' ')
  echo $(( hash % 16 ))
}

# CDN download (no auth)
cdn_download() {
  local src_path="$1"
  local out_file="$2"
  local url="https://huggingface.co/datasets/${REPO}/resolve/main/${src_path}"
  curl -fsSL --retry 3 --retry-delay 5 -o "$out_file" "$ur

## review — reviewer @ 2026-05-02T18:58:21.499432Z

APPROVE: Deterministic date-partitioned ingestion with CDN-bypass and pre-flight file list is a workable, incremental improvement that reduces HF API pressure, eliminates overwrite races, and fits the existing 16-shard matrix.

Acceptance criteria:
- Output paths follow `batches/public-merged/YYYY/MM/DD/shardXX-HHMMSS.jsonl` and are unique per run.
- Pre-flight file list (`file-list-YYYYMMDD.json`) can be produced and consumed by workers; workers fall back to live listing when absent.
- Workers use CDN URLs (`https://huggingface.co/datasets/.../resolve/main/...`) without auth and tolerate 429/retry with backoff.
- Deterministic shard assignment (`sha256(path) % 16`) maps each file to exactly one shard and workers skip non-assigned files.
- Uploads are idempotent: target path includes date+shard+timestamp and workers skip when file already exists; no overwrites of prior runs.

## qa — qa @ 2026-05-02T18:58:37.615387Z

PASS: deterministic date-partitioned ingestion with CDN-bypass and pre-flight file list is approved.

1. **Acceptance criteria**
- Output path format: `batches/public-merged/YYYY/MM/DD/shardXX-HHMMSS.jsonl` with UTC date and unique timestamp; pattern matches exactly and directory depth = 5.
- Pre-flight file list: `file-list-YYYYMMDD.json` exists and is valid JSON array of objects with `path` (string) and `sha256` (64-char hex); workers consume it when present and fall back to live listing when absent.
- CDN fetch: workers request `https://huggingface.co/datasets/axentx/surrogate-1-training-pairs/resolve/main/<path>` without Authorization header; retry on 429 with exponential backoff (max 3 retries) and succeed (2xx).
- Deterministic shard assignment: for every file path, `sha256(path) % 16` equals exactly one SHARD_ID (0–15); workers skip files not assigned to their SHARD_ID.
- Idempotent uploads: target path includes date+shard+timestamp; repeated run with same inputs does not overwrite existing file (upload skipped if file exists).
- No overwrite races: concurrent workers writing to different shards/paths never produce partial/corrupt outputs; file-level write atomicity is preserved.
- Rate-limit pressure: total HF API list calls per run ≤ 1 (preflight) + 0 during worker streaming; CDN-only downloads produce zero 429s under normal operation.

2. **Unit tests** (pytest-style pseudo-code)
```python
# test_paths.py
def test_output_path_format():
    path = make_output_path(run_date="2026-05-02", shard_id=3, ts="142311")
    assert path == "batches/public-merged/2026/05/02/shard03-142311.jsonl"
    assert re.match(r"^batches/public-merged/\d{4}/\d{2}/\d{2}/shard\d{2}-\d{6}\.jsonl$", path)

def test_output_path_utc_date():
    with freeze_time("2026-05-02 23:00:00", tz_offset=0):
        path = make_output_path_now(shard_id=0)
        assert "2026/05/02" in path

# test_preflight.py
def test_preflight_file_list_valid(tmp_path):
    items = [{"path": "2026/05/02/file1.jsonl", "sha256": "a"*64}]
    p = tmp_path / "file-list-20260502.json"
    p.write_text(json.dumps(items))
    loaded = load_preflight_list(p)
    assert len(loaded) == 1
    assert loaded[0]["path"] == "2026/05/02/file1.jsonl"
    assert is_sha256_hex(loaded[0]["sha256"])

def test_preflight_missing_fallback(monkeypatch):
    monkeypatch.setattr("os.path.exists", lambda x: False)
    result = get_file_list("live", "20260502")
    assert result["source"] == "live"
    assert isinstance(result["items"], list)

# test_shard_assignment.py
def test_deterministic_shard():
    assert shard_for_path("2026/05/02/a.jsonl") == shard_for_path("2026/05/02/a.jsonl")
    assert 0 <= shard_for_path("x") <= 15

def test_worker_skips_non_assigned():
    assigned = shard_for_path("2026/05/02/a.jsonl")
    assert should_process("2026/05/02/a.jsonl", shard_id=(assigned + 1) % 16) is False
    assert should_process("2026/05/02/a.jsonl", shard_id=assigned) is True

# test_cdn_fetch.py
def test_cdn_url():
    assert to_cdn_url("2026/05/02/file.jsonl") == \
        "https://huggingface.co/datasets/axentx/surrogate-1-training-pairs/resolve/main/2026/05/02/file.jsonl"

def test_no_auth_header(requests_mock):
    requests_mock.get(contains("resolve/main/"), status_code=200, text="{}")
    resp = fetch_cdn("2026/05/02/file.jsonl")
    assert "Authorization" not in resp.request.headers

def test_retry_on_429(requests_mock):
    rs = [{"status_code": 429, "headers": {"Retry-After": "0"}}, {"status_code": 200, "text": "{}"}]
    requests_mock.get(contains("resolve/main/"), rs)
    resp = fetch_cdn("2026/05/02/file.jsonl")
    assert resp.status_code == 
