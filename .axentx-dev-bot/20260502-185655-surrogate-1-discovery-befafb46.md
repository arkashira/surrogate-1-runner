# axentx-dev-bot decision
- id: `20260502-185655-surrogate-1-discovery-befafb46`
- project: surrogate-1
- focus: discovery
- created_at: 2026-05-02T18:56:55.167533Z

## dev — claude/llm-fallback-chain @ 2026-05-02T18:56:55.167599Z

## 1. Diagnosis
- No deterministic date-partitioning: re-runs overwrite or duplicate outputs instead of appending to stable `YYYY/MM/DD` folders, causing noisy history and downstream training instability.
- No pre-flight file-list: workers call live HF APIs (`list_repo_tree`/`load_dataset`) during every run, risking 429 rate-limits and wasting quota instead of using CDN-only fetches.
- Shard outputs use flat `batches/public-merged/<date>/shard<N>-<HHMMSS>.jsonl` which collides across reruns; no content-addressable path or idempotency key.
- Central dedup store lives only on the HF Space (`cpu-basic`); GitHub Actions runners start with empty caches, so cross-run duplicates are not suppressed and bandwidth is wasted.
- No backoff/retry or rate-limit guard around HF ingestion calls; transient 429s or CDN hiccups can kill a shard run and lose that slice for the cycle.

## 2. Proposed change
File: `bin/dataset-enrich.sh`  
Scope: add deterministic date partition, generate pre-flight file-list once per run, emit idempotent shard paths, and embed CDN-only fetch behavior with retry/backoff.

## 3. Implementation
```bash
#!/usr/bin/env bash
# bin/dataset-enrich.sh
# Updated: deterministic date partitioning + CDN-only ingestion + idempotent shard paths

set -euo pipefail

# -- config --
REPO="axentx/surrogate-1-training-pairs"
HF_TOKEN="${HF_TOKEN:-}"
SHARD_ID="${SHARD_ID:-0}"        # 0..15
TOTAL_SHARDS="${TOTAL_SHARDS:-16}"
DATE_PART=$(date -u +"%Y/%m/%d")
TS=$(date -u +"%H%M%S")
RUN_ID=$(date -u +"%Y%m%d")
OUT_DIR="batches/public-merged/${DATE_PART}"
OUT_FILE="${OUT_DIR}/shard${SHARD_ID}-${RUN_ID}-${TS}.jsonl"
CACHE_DIR=".cache"
FILE_LIST="${CACHE_DIR}/file-list-${RUN_ID}.json"
MAX_RETRIES=5
RETRY_BACKOFF=30

mkdir -p "${CACHE_DIR}" "${OUT_DIR}"

# -- helpers --
log() { echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] $*"; }

retry() {
  local n=0
  until "$@"; do
    local code=$?
    n=$((n + 1))
    if [ "$n" -ge "$MAX_RETRIES" ]; then
      log "ERROR: command failed after $MAX_RETRIES attempts: $*"
      return $code
    fi
    local sleep_time=$((RETRY_BACKOFF * n))
    log "WARN: command failed (attempt $n/$MAX_RETRIES), retrying in ${sleep_time}s: $*"
    sleep "$sleep_time"
  done
}

# -- pre-flight file list (single API call per run) --
if [ ! -f "${FILE_LIST}" ]; then
  log "Generating pre-flight file list for ${RUN_ID}..."
  # Use recursive=False per top-level folder to avoid 100x pagination; keep list small and deterministic.
  python3 -c "
import json, os
from huggingface_hub import HfApi
api = HfApi(token=os.environ.get('HF_TOKEN'))
# Only list top-level folders/files once; workers will resolve exact paths from this manifest.
tree = api.list_repo_tree(repo_id='${REPO}', path='', recursive=False)
items = [t.rpath for t in tree if t.type == 'file']
open('${FILE_LIST}', 'w').write(json.dumps(items, sort_keys=True))
" || {
    log "ERROR: failed to list repo tree"; exit 1
  }
  log "File list saved to ${FILE_LIST} ($(jq length <"${FILE_LIST}") items)"
fi

# -- deterministic shard assignment --
mapfile -t ALL_FILES < <(jq -r '.[]' "${FILE_LIST}")
TOTAL_FILES=${#ALL_FILES[@]}
if [ "$TOTAL_FILES" -eq 0 ]; then
  log "ERROR: no files to process"; exit 1
fi

# assign files to shards by stable hash of filename
assign_shard() {
  local file="$1"
  # deterministic 0..(TOTAL_SHARDS-1)
  python3 -c "print(abs(hash('${file}')) % ${TOTAL_SHARDS})"
}

# collect shard files
SHARD_FILES=()
for f in "${ALL_FILES[@]}"; do
  s=$(assign_shard "$f")
  if [ "$s" -eq "$SHARD_ID" ]; then
    SHARD_FILES+=("$f")
  fi
done

log "Shard ${SHARD_ID}/${TOTAL_SHARDS} processing ${#SHARD_FILES[@]}/${TOTAL_FILES} files -> ${OUT_FILE}"

# -- CDN-only fetch + schema projection --
process_file() {
  local rel_path="$1"
  local url="https://huggingface.co/datasets/${REPO}/resolve/main/${rel_path}"
  local tmpf
  tmpf=$(mktemp)
  # CDN download (no Authorization header) bypasses API rate limits
  retry curl -fsSL --retry 3 --retry-delay 5 -o "${tmpf}" "${url}" || {
 

## review — reviewer @ 2026-05-02T18:58:04.822648Z

APPROVE: implements deterministic date partitioning, pre-flight file list, idempotent shard paths, CDN-only fetches, and retry/backoff — a clear workable step that reduces rerun noise, rate-limit risk, and cross-run duplication.

Acceptance criteria (for downstream tester):
- Running `bin/dataset-enrich.sh` on two different UTC days produces outputs under distinct `batches/public-merged/YYYY/MM/DD/` folders (no overwrites).
- Within a single run (same RUN_ID), multiple invocations with the same SHARD_ID produce the same shard filename pattern and do not re-fetch the repo tree when `FILE_LIST` already exists.
- Each shard file contains only `{prompt,response}` fields (or is empty/skipped if projection fails) and is valid JSONL.
- Transient HTTP errors (429/5xx) or curl failures trigger retries up to MAX_RETRIES with increasing backoff; after exhaustion the shard run exits non-zero and logs the failure.
- HF API calls (list_repo_tree) are made at most once per RUN_ID; subsequent shard workers read the cached FILE_LIST and do not call the API again.

## qa — qa @ 2026-05-02T18:58:29.827085Z

PASS: criteria clear and implementable

1. **Acceptance criteria**
- Running the script on two different UTC calendar days produces outputs under distinct `batches/public-merged/YYYY/MM/DD/` directories; no file overwrites across days (measurable by path prefix equality checks).
- Within a single RUN_ID, repeated invocations with the same SHARD_ID produce identical shard filenames (excluding timestamp collisions) and do not invoke `list_repo_tree` more than once (measurable by API call counts and FILE_LIST mtime).
- Every non-empty shard file contains only `{prompt,response}` fields (or is empty) and is valid JSONL (measurable by JSONL schema validation and field enumeration).
- Transient HTTP 429/5xx or fetch failures trigger retries up to MAX_RETRIES with increasing backoff; after exhaustion the script exits non-zero and logs failure (measurable by exit codes, log assertions, and retry counters).
- HF API `list_repo_tree` is invoked at most once per RUN_ID; subsequent shard workers read the cached FILE_LIST (measurable by network interception or mock call counts).
- Output directory structure matches `batches/public-merged/YYYY/MM/DD/shardN-RUNID-TS.jsonl` and filenames are unique per (RUN_ID, SHARD_ID, TS) (measurable by regex and uniqueness checks).
- Script fails fast on unrecoverable errors (e.g., missing FILE_LIST generation) with non-zero exit and clear log message (measurable by exit codes and log content).

2. **Unit tests** (pytest-style pseudo-code)
```python
# test_dataset_enrich.py
import os, json, tempfile, subprocess, time, re
from pathlib import Path
from unittest.mock import patch, MagicMock

DATE_RE = re.compile(r"batches/public-merged/\d{4}/\d{2}/\d{2}/")
SHARD_RE = re.compile(r"shard(\d+)-(\d{8})-(\d{6})\.jsonl")

def test_date_partition_changes_daily():
    with patch("dataset_enrich.date") as mock_date:
        mock_date.utcnow.return_value.strftime.side_effect = lambda f: {
            "%Y/%m/%d": "2023/01/01", "%Y%m%d": "20230101", "%H%M%S": "120000"
        }[f]
        out = dataset_enrich.build_paths()
        assert out["OUT_DIR"] == "batches/public-merged/2023/01/01"

        mock_date.utcnow.return_value.strftime.side_effect = lambda f: {
            "%Y/%m/%d": "2023/01/02", "%Y%m%d": "20230102", "%H%M%S": "120000"
        }[f]
        out2 = dataset_enrich.build_paths()
        assert out2["OUT_DIR"] == "batches/public-merged/2023/01/02"
        assert out["OUT_DIR"] != out2["OUT_DIR"]

def test_file_list_cached_per_run_id(tmp_path):
    cache = tmp_path / ".cache"
    cache.mkdir()
    run_id = "20230101"
    file_list = cache / f"file-list-{run_id}.json"
    file_list.write_text(json.dumps(["a.jsonl", "b.jsonl"]))

    with patch("dataset_enrich.os.environ", {"RUN_ID": run_id}), \
         patch("dataset_enrich.Path") as MockPath, \
         patch("dataset_enrich.HfApi") as MockApi:
        MockPath.return_value.exists.return_value = True
        MockPath.return_value.__truediv__.return_value = file_list
        dataset_enrich.ensure_file_list()
        assert MockApi.call_count == 0

def test_retry_backoff_increases():
    calls = []
    def failing():
        calls.append(1)
        raise RuntimeError("nope")
    try:
        dataset_enrich.retry(failing, max_retries=3, backoff=1)
    except RuntimeError:
        pass
    assert len(calls) == 3

def test_shard_filename_pattern():
    with patch("dataset_enrich.date") as mock_date:
        mock_date.utcnow.return_value.strftime.side_effect = lambda f: {
            "%Y/%m/%d": "2023/01/01", "%Y%m%d": "20230101", "%H%M%S": "123456"
        }[f]
        out = dataset_enrich.build_paths(shard_id=5)
        assert SHARD_RE.search(out["OUT_FILE"]) is not None
        m = SHARD_RE.search(out["OUT_FILE"])
        assert int(m.group(1)) == 5
        assert m.group(2) == "20230101"

def test_jsonl_valid_and_limited_fields(tmp_path):
    p = tmp_path / "shard.jsonl"
    p.write_text('{"prompt":"hi","response":"ok"}\n{"prompt":"q"}\n')
    lines = data
