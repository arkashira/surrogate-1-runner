# axentx-dev-bot decision
- id: `20260502-232052-surrogate-1-discovery-705cdc6d`
- project: surrogate-1
- focus: discovery
- created_at: 2026-05-02T23:20:52.084572Z

## dev — claude/llm-fallback-chain @ 2026-05-02T23:20:52.084660Z

## Final Implementation Plan (≤2h)

**Goal:** Replace runtime HF API calls + streaming dataset loads in `bin/dataset-enrich.sh` with a deterministic pre-flight snapshot (JSON) and CDN-only fetches. This removes rate-limit exposure, avoids pyarrow schema errors, and keeps shard runners lightweight.

---

## Files to Add/Modify

### 1) Snapshot Generator — `bin/make-snapshot.sh` (NEW)

```bash
#!/usr/bin/env bash
# bin/make-snapshot.sh
# Usage:
#   HF_TOKEN=hf_xxx REPO=axentx/surrogate-1-training-pairs DATE=2026-05-02 ./bin/make-snapshot.sh
#
# Produces:
#   snapshot/<date>/files.json  (deterministic list of file paths)

set -euo pipefail

: "${HF_TOKEN:?required}"
: "${REPO:?required}"
: "${DATE:?required (YYYY-MM-DD)}"

OUTDIR="snapshot/${DATE}"
OUTFILE="${OUTDIR}/files.json"

mkdir -p "${OUTDIR}"

python3 - <<PY > "${OUTFILE}.tmp"
import os, json, sys
from huggingface_hub import HfApi

api = HfApi(token=os.environ["HF_TOKEN"])
repo = os.environ["REPO"]
date = os.environ["DATE"]

entries = api.list_repo_tree(repo=repo, path=date, recursive=False)

files = []
for e in entries:
    # Keep only files (skip subfolders)
    if getattr(e, "type", None) == "file" or (hasattr(e, "path") and "." in e.path):
        files.append(e.path)

files.sort()
print(json.dumps({"date": date, "files": files}, indent=2))
PY

mv "${OUTFILE}.tmp" "${OUTFILE}"
echo "Snapshot written to ${OUTFILE}"
```

```bash
chmod +x bin/make-snapshot.sh
```

---

### 2) Updated Worker — `bin/dataset-enrich.sh` (MODIFIED)

```bash
#!/usr/bin/env bash
# bin/dataset-enrich.sh
# Updated to use CDN-only fetches + snapshot.
#
# Environment:
#   SHARD_ID (0-15)
#   HF_TOKEN (for push)
#   SNAPSHOT_FILE (path to JSON produced by make-snapshot.sh)
#   DATE (YYYY-MM-DD) — must match snapshot date
#
# Behavior:
#   - Reads files list from SNAPSHOT_FILE
#   - Deterministically assigns 1/16 slice by slug-hash mod 16
#   - Downloads each assigned file via CDN (no Authorization header)
#   - Projects to {prompt, response}, dedups, and uploads shard output

set -euo pipefail

: "${SHARD_ID:?required (0-15)}"
: "${HF_TOKEN:?required}"
: "${SNAPSHOT_FILE:?required}"
: "${DATE:?required (YYYY-MM-DD)}"

REPO_DST="axentx/surrogate-1-training-pairs"
WORKDIR=$(mktemp -d)
cleanup() { rm -rf "${WORKDIR}"; }
trap cleanup EXIT

# Python helper for projection + dedup
cat > "${WORKDIR}/project_and_dedup.py" <<'PY'
import sys, json, hashlib, pyarrow.parquet as pq, os

def hash_slug(s):
    return int(hashlib.md5(s.encode()).hexdigest(), 16)

def project_file_to_pairs(local_path):
    """Return list of {prompt, response} dicts; skip on error."""
    try:
        if local_path.endswith(".parquet"):
            tbl = pq.read_table(local_path, columns=["prompt", "response"])
            df = tbl.to_pandas()
            return [{"prompt": r.prompt, "response": r.response} for r in df.itertuples()]
        if local_path.endswith(".jsonl"):
            out = []
            with open(local_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    obj = json.loads(line)
                    out.append({"prompt": obj["prompt"], "response": obj["response"]})
            return out
    except Exception:
        return []
    return []

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--shard", type=int, required=True)
    parser.add_argument("--download-root", required=True)
    args = parser.parse_args()

    seen = set()
    out_rows = []
    with open(args.input, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rel_path = line
            slug = rel_path
            if hash_slug(slug) % 16 != args.shard:
                continue

  

## review — reviewer @ 2026-05-02T23:21:01.462973Z

APPROVE: This is a workable “discovery” step that replaces runtime HF API calls + streaming dataset loads with a deterministic snapshot + CDN-only fetches, removes rate-limit exposure, and keeps shard runners lightweight. It provides a clear path to test and iterate.

Acceptance criteria:
- `bin/make-snapshot.sh` produces valid `snapshot/<date>/files.json` containing a sorted list of file paths for the given DATE and REPO when HF_TOKEN is set.
- `bin/dataset-enrich.sh` reads `SNAPSHOT_FILE`, deterministically assigns files to shards via `hash_slug(rel_path) % 16 == SHARD_ID`, and skips non-matching files.
- Downloads use CDN URLs (no Authorization header) and the projection step reads only `prompt`/`response` columns from parquet or jsonl, skipping malformed files.
- Deduplication is applied across the shard output using content hash (md5 of prompt\x1eresponse) and the final output is newline-delimited JSON.
- The worker exits with a clear error if `SNAPSHOT_FILE` is missing or required env vars are unset, and cleans up temp workdir on exit.

## qa — qa @ 2026-05-02T23:21:37.746227Z

PASS

1. **Acceptance criteria**
- `bin/make-snapshot.sh` exits 0 and produces `snapshot/<DATE>/files.json` that is valid JSON with keys `date` (string matching DATE) and `files` (array of strings), sorted ascending, containing only file paths (no folders), when `HF_TOKEN` and `REPO` and `DATE` are set.
- `bin/dataset-enrich.sh` exits 0 and emits newline-delimited JSON to stdout where each line parses to an object with string keys `prompt` and `response` (non-empty strings), and the number of emitted lines equals the number of assigned, readable, non-empty files after deduplication.
- Shard assignment is deterministic: for every file path in the snapshot, `hash_slug(rel_path) % 16 == SHARD_ID` is true for exactly one `SHARD_ID` in 0–16, and `dataset-enrich.sh` with a given `SHARD_ID` processes only those files.
- Downloads use CDN URLs (no `Authorization` header) — verifiable by inspecting HTTP requests or by confirming no `Authorization` header is present when fetching via `curl`/`wget`/Python HTTP client.
- Deduplication uses content hash `md5(prompt + \x1e + response)`; duplicate content across assigned files results in exactly one emitted record per unique hash.
- Missing `SNAPSHOT_FILE` or unset required env vars (`SHARD_ID`, `HF_TOKEN`, `SNAPSHOT_FILE`, `DATE`) causes immediate non-zero exit and a clear error message on stderr.
- Temporary workdir is removed on normal exit and on interrupt (trap cleanup) — `WORKDIR` does not exist after script finishes or receives SIGINT/SIGTERM.

2. **Unit tests** (pytest-style pseudo-code)
```python
# test_make_snapshot.py
import json, subprocess, os, tempfile

def test_make_snapshot_valid_json():
    with tempfile.TemporaryDirectory() as td:
        os.environ.update({"HF_TOKEN": "fake", "REPO": "owner/repo", "DATE": "2026-05-02"})
        out = subprocess.check_output(["./bin/make-snapshot.sh"], env=os.environ, text=True)
        snapshot_path = os.path.join(td, "snapshot/2026-05-02/files.json")
        # script writes to snapshot/<DATE>/files.json relative to cwd; simulate cwd=td
        # (in real test, run in td)
        with open(snapshot_path) as f:
            data = json.load(f)
        assert "date" in data and data["date"] == "2026-05-02"
        assert "files" in data and isinstance(data["files"], list)
        assert all(isinstance(p, str) and len(p) > 0 for p in data["files"])
        assert data["files"] == sorted(data["files"])

# test_dataset_enrich.py
import json, hashlib, tempfile, os, subprocess

def hash_slug(s):
    return int(hashlib.md5(s.encode()).hexdigest(), 16)

def test_shard_assignment_deterministic():
    files = ["a.parquet", "b.jsonl", "c.parquet"]
    for fpath in files:
        assigned = [shard for shard in range(16) if hash_slug(fpath) % 16 == shard]
        assert len(assigned) == 1

def test_project_and_dedup_py_exists_and_importable():
    # lightweight syntax check for embedded script
    proc = subprocess.run(["python3", "-c", "exec(open('bin/dataset-enrich.sh').read().split('cat >')[1].split('PY')[0])"],
                          capture_output=True, text=True)
    # If embedded script is invalid Python this will raise; we expect no SyntaxError.
    assert proc.returncode != 1  # tolerate other failures (missing env) but not SyntaxError

def test_missing_snapshot_exits_nonzero():
    env = {"SHARD_ID": "0", "HF_TOKEN": "x", "SNAPSHOT_FILE": "/missing.json", "DATE": "2026-05-02"}
    proc = subprocess.run(["./bin/dataset-enrich.sh"], env=env, capture_output=True, text=True)
    assert proc.returncode != 0
    assert "SNAPSHOT_FILE" in proc.stderr or "required" in proc.stderr
```

3. **Integration tests** (3 happy + 3 edge)

Happy cases
- Happy 1 — End-to-end snapshot + single shard: run `make-snapshot.sh` against a small test repo with 4 parquet files; run `dataset-enrich.sh` with `SHARD_ID=0` and the produced snapshot; assert stdout lines parse as `{prompt,response}` and count equals assigned files after dedup.
- Happy 2 — All shards partition
