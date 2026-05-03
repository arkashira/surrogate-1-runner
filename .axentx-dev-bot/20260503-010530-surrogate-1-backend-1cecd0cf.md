# axentx-dev-bot decision
- id: `20260503-010530-surrogate-1-backend-1cecd0cf`
- project: surrogate-1
- focus: backend
- created_at: 2026-05-03T01:05:30.181191Z

## dev — claude/llm-fallback-chain @ 2026-05-03T01:05:30.181245Z

**Final synthesized implementation**  
Combines strongest, actionable parts from both proposals and resolves contradictions in favor of correctness and concrete execution.

---

## Core change (single sentence)
Replace recursive `list_repo_files` + per-file HF API calls with **one `list_repo_tree` per date folder + CDN-only fetches**, and **project to `{prompt,response}` at parse time** to eliminate 429 rate limits and HF Space OOM.

---

## What to modify (concrete)

- `bin/gen-manifest.sh` (new, run once per date folder)  
- `bin/dataset-enrich.sh` (worker script)  
- `ingest.yml` (optional orchestration)  

Keep deterministic 16-shard split and existing dedup flow **unchanged**.

---

## 1) Manifest generator (run once, commit or embed)

```bash
# bin/gen-manifest.sh
#!/usr/bin/env bash
set -euo pipefail

REPO="${1:-axentx/surrogate-1-training-pairs}"
DATE="${2:-$(date +%Y-%m-%d)}"
OUT="${3:-manifest-${DATE}.json}"

python3 - "$REPO" "$DATE" "$OUT" <<'PY'
import json, os, sys
from huggingface_hub import HfApi

repo_id, date_folder, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
api = HfApi()

# One non-recursive tree call per folder (no per-file API calls)
tree = api.list_repo_tree(repo_id, path=date_folder, recursive=False)
files = sorted(
    f.rfilename
    for f in tree
    if f.rfilename.endswith((".jsonl", ".parquet", ".json"))
)

manifest = {"repo": repo_id, "date": date_folder, "files": files}
os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)
print(f"Wrote {len(files)} files to {out_path}")
PY
```

```bash
chmod +x bin/gen-manifest.sh
bin/gen-manifest.sh axentx/surrogate-1-training-pairs 2026-05-03 manifest-20260503.json
```

**Why this is correct**:  
- Uses `list_repo_tree(..., recursive=False)` (single API call per folder).  
- Produces a small JSON manifest that can be committed or passed to workers.  
- Avoids per-file API calls entirely.

---

## 2) Worker script (CDN-only, no auth, projection at parse time)

```bash
# bin/dataset-enrich.sh
#!/usr/bin/env bash
# CDN-only ingestion; no HF API auth during streaming
set -euo pipefail

REPO="${REPO:-axentx/surrogate-1-training-pairs}"
DATE="${DATE:-$(date +%Y-%m-%d)}"
SHARD_ID="${SHARD_ID:-0}"
TOTAL_SHARDS="${TOTAL_SHARDS:-16}"
MANIFEST="${MANIFEST:-manifest-${DATE}.json}"
OUT_DIR="${OUT_DIR:-output}"
TMP_DIR="${TMP_DIR:-/tmp/surrogate-ingest}"

mkdir -p "$OUT_DIR" "$TMP_DIR"

# Validate manifest
if [[ ! -f "$MANIFEST" ]]; then
  echo "ERROR: Manifest $MANIFEST not found. Generate with bin/gen-manifest.sh"
  exit 1
fi

# Load file list from manifest (deterministic)
mapfile -t ALL_FILES < <(
  python3 -c "
import json, sys
with open(sys.argv[1]) as f:
    data = json.load(f)
for fn in sorted(data['files']):
    print(fn)
" "$MANIFEST"
)

TOTAL_FILES="${#ALL_FILES[@]}"
if [[ "$TOTAL_FILES" -eq 0 ]]; then
  echo "No files in manifest for $DATE"
  exit 0
fi

# Deterministic shard assignment (stable by filename)
mapfile -t MY_FILES < <(
  for f in "${ALL_FILES[@]}"; do
    HASH=$(echo -n "$f" | md5sum | awk '{print $1}')
    SHARD=$(( 0x${HASH:0:8} % TOTAL_SHARDS ))
    if [[ "$SHARD" -eq "$SHARD_ID" ]]; then
      echo "$f"
    fi
  done
)

echo "Shard $SHARD_ID/$TOTAL_SHARDS processing ${#MY_FILES[@]} files (out of $TOTAL_FILES total)"

# Process via CDN only
for REL_PATH in "${MY_FILES[@]}"; do
  FILENAME=$(basename "$REL_PATH")
  CDN_URL="https://huggingface.co/datasets/${REPO}/resolve/main/${REL_PATH}"
  TMP_FILE="${TMP_DIR}/${FILENAME}.dl"

  echo "Downloading ${REL_PATH} via CDN..."
  curl -fsSL --retry 3 --retry-delay 5 -o "$TMP_FILE" "$CDN_URL"

  # Project to {prompt,response} at parse time
  OUT_TMP="${TMP_DIR}/${FILENAME}.projected.jsonl"
  python3 - "$TMP_FILE" "$OUT_TMP" <<'PY'
import sys, json, pyarrow.parquet as pq

src, dst = sys.argv[1], sys.argv[2]

def normalize(obj):
    prompt = obj.get("prompt") or obj.get("input") or obj.get("te

## review — reviewer @ 2026-05-03T01:05:36.800667Z

APPROVE: This is a workable, concrete step forward that directly addresses the stated constraints (429 rate limits and HF Space OOM) by replacing per-file API calls with a single `list_repo_tree` per folder and CDN-only fetches, while projecting to `{prompt,response}` at parse time. It keeps deterministic sharding and dedup unchanged and provides acceptance criteria a downstream tester can verify.

Acceptance criteria:
- `bin/gen-manifest.sh` produces a valid `manifest-YYYY-MM-DD.json` listing files for the given date folder using one non-recursive `list_repo_tree` call (no per-file API calls).
- `bin/dataset-enrich.sh` consumes the manifest, assigns files to shards deterministically (stable by filename), and downloads only assigned files via CDN (no HF auth during streaming).
- Projection at parse time yields lines with exactly `{"prompt": "...", "response": "..."}` (strings) for each input record; malformed/missing records are skipped without crashing the worker.
- Worker exits with non-zero and a clear error if the manifest is missing or empty; exits zero when no files are assigned to the shard.
- Downloads use retries/backoff and temporary files; partial/corrupt downloads do not leave garbage in the final output directory.

## review — qa @ 2026-05-03T01:05:49.056793Z

PASS: Manifest + worker plan is concrete and testable.

1) **Acceptance criteria**
- `bin/gen-manifest.sh` exits 0 and emits `manifest-YYYY-MM-DD.json` containing a top-level object with keys `repo`, `date`, `files` where `files` is an array of strings; `files` length ≥ 0; no per-file API calls (one `list_repo_tree` call per run).
- `bin/dataset-enrich.sh` exits 0 when manifest exists and shard has no assigned files; exits non-zero with clear error when manifest is missing or empty.
- Deterministic shard assignment: for any manifest and fixed `SHARD_ID`/`TOTAL_SHARDS`, assigned filenames are stable across runs (same sorted input ⇒ same shard set).
- Projection at parse time: every emitted output line is valid JSON matching `{"prompt": "<string>", "response": "<string>"}`; malformed/missing fields are skipped (not emitted) and do not crash worker.
- Downloads use CDN URLs only (no HF auth headers during streaming), employ retries/backoff, and write via temporary files; corrupt/partial downloads do not appear in final output directory.
- Worker log/exit surfaces counts: files assigned, files downloaded OK, files skipped (corrupt/parse errors), total records emitted.

2) **Unit tests** (pytest-style pseudo-code)

```python
# test_gen_manifest.py
def test_gen_manifest_calls_single_tree(mocker):
    api = mocker.patch("huggingface_hub.HfApi")
    api.return_value.list_repo_tree.return_value = [
        mocker.Mock(rfilename="2026-05-03/a.jsonl"),
        mocker.Mock(rfilename="2026-05-03/b.parquet"),
    ]
    # run script via python inline or subprocess
    out = run_gen_manifest("repo", "2026-05-03", "manifest.json")
    assert out["repo"] == "repo"
    assert out["date"] == "2026-05-03"
    assert out["files"] == ["2026-05-03/a.jsonl", "2026-05-03/b.parquet"]
    api.return_value.list_repo_tree.assert_called_once_with("repo", path="2026-05-03", recursive=False)

def test_gen_manifest_rejects_recursive_by_contract(mocker):
    api = mocker.patch("huggingface_hub.HfApi")
    # Ensure recursive=False is explicit in implementation
    import bin.gen_manifest as mod
    src = inspect.getsource(mod)
    assert "recursive=False" in src
```

```python
# test_dataset_enrich.py
def test_shard_assignment_deterministic():
    files = ["2026-05-03/a.jsonl", "2026-05-03/b.jsonl", "2026-05-03/c.jsonl"]
    shard0 = assign_shard(files, shard_id=0, total_shards=2)
    shard1 = assign_shard(files, shard_id=1, total_shards=2)
    assert sorted(set(shard0 + shard1)) == sorted(files)
    # stable across runs
    assert assign_shard(files, 0, 2) == shard0

def test_projection_at_parse_time():
    line = '{"prompt": "hello", "response": "world", "extra": 1}'
    out = project_record(json.loads(line))
    assert out == {"prompt": "hello", "response": "world"}
    assert isinstance(out["prompt"], str) and isinstance(out["response"], str)

def test_skip_malformed():
    for bad in [
        '{"prompt": 123, "response": "ok"}',
        '{"response": "x"}',
        'not json',
        '{"prompt": "x", "response": null}',
    ]:
        assert project_record(json.loads(bad) if json.loads(bad) else None) is None

def test_download_uses_cdn_no_auth(mocker):
    downloader = mocker.patch("urllib.request.urlopen")
    stream_file("repo", "2026-05-03/a.jsonl", use_auth=False)
    call_args = downloader.call_args[0][0].full_url
    assert "huggingface.co" in call_args or "/resolve/" in call_args
    # ensure no Authorization header
    req = downloader.call_args[0][0]
    assert "Authorization" not in req.headers
```

3) **Integration tests** (happy + edge)

Happy cases
- Manifest generation: run `bin/gen-manifest.sh repo 2026-05-03 manifest.json`; assert file exists, valid JSON, `files` sorted, and script exit 0.
- Worker zero-assignment: create manifest with 3 files; run `SHARD_ID=5 TOTAL_SHARDS=16 bin/dataset-enrich.sh`; assert exit 0, output directory empty, log reports 0 assigned.
- Worker full pipeline: manifest with 4 files, TOTAL_SHARDS=2, SHARD_ID=0; moc
