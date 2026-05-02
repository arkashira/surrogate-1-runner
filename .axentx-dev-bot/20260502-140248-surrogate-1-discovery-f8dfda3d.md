# axentx-dev-bot decision
- id: `20260502-140248-surrogate-1-discovery-f8dfda3d`
- project: surrogate-1
- focus: discovery
- created_at: 2026-05-02T14:02:48.029221Z

## dev — claude/llm-fallback-chain @ 2026-05-02T14:02:48.029346Z

## Final Synthesized Plan (Best of Both Candidates)

**Goal**: Eliminate HF API rate-limit (429) risk during 16-shard GitHub Actions ingest by switching to a **CDN-only ingestion path** with a pre-listed file manifest, while adding lightweight local dedup to reduce redundant uploads.

**Core Insight**: Public dataset files on `resolve/main/` bypass auth and rate-limits entirely. Listing the repo tree once (orchestrator-side) and distributing the manifest to all shards prevents 16 concurrent runners from paginating the same repo via HF API.

---

## Implementation Plan (≤2h)

### 1. Add Manifest Builder (`bin/build-manifest.sh`)
- **Location**: Runs on Mac orchestrator or in workflow **before** matrix dispatch.
- **Logic**: Uses `huggingface_hub.list_repo_tree(path, recursive=False)` once for `public-merged/<date>` (or source folder).
- **Output**: `file-list-YYYY-MM-DD.json` containing `rfilename` entries.

```bash
#!/usr/bin/env bash
set -euo pipefail
# Usage: ./bin/build-manifest.sh <date-folder>
DATE_FOLDER=${1:-$(date +%Y-%m-%d)}
REPO="datasets/axentx/surrogate-1-training-pairs"
OUT="filelist/file-list-${DATE_FOLDER}.json"

mkdir -p filelist
python -c "
from huggingface_hub import list_repo_tree
import json, sys
tree = list_repo_tree('$REPO', path='$DATE_FOLDER', recursive=False)
files = [f.rfilename for f in tree if f.type == 'file']
with open('$OUT', 'w') as f:
    json.dump(files, f)
print(f'Wrote {len(files)} files to $OUT')
"
```

### 2. Update Workflow (`.github/workflows/ingest.yml`)
- Add manifest step **before** matrix.
- Upload/download artifact so all shards share the same manifest.

```yaml
    - name: Build file manifest
      run: bash bin/build-manifest.sh "${DATE_FOLDER}"
      env:
        HF_TOKEN: ${{ secrets.HF_TOKEN }}

    - name: Upload manifest artifact
      uses: actions/upload-artifact@v4
      with:
        name: file-list
        path: filelist/

    # ... matrix definition ...

    - name: Download manifest in each shard
      uses: actions/download-artifact@v4
      with:
        name: file-list
        path: filelist/

    - name: Run shard
      run: bash bin/dataset-enrich.sh
      env:
        HF_TOKEN: ${{ secrets.HF_TOKEN }}
        SHARD_ID: ${{ matrix.shard_id }}
        N_SHARDS: 16
        DATE_FOLDER: ${{ env.DATE_FOLDER }}
        FILE_LIST: filelist/file-list-${{ env.DATE_FOLDER }}.json
```

### 3. Modify `bin/dataset-enrich.sh`
- **Read shard slice** from pre-computed manifest (no `list_repo_files`).
- **Use CDN URLs** for downloads: `https://huggingface.co/datasets/.../resolve/main/<path>`.
- **Add per-shard local dedup** (in-memory associative array) to skip duplicates within the same batch.
- Keep HF token **only for uploads**.

```bash
#!/usr/bin/env bash
set -euo pipefail

# Required env
: "${HF_TOKEN:?}" "${SHARD_ID:?}" "${N_SHARDS:=16}" "${DATE_FOLDER:?}" "${FILE_LIST:?}"

REPO="axentx/surrogate-1-training-pairs"
BASE_CDN="https://huggingface.co/datasets/${REPO}/resolve/main"
OUT_DIR="batches/public-merged/${DATE_FOLDER}"
mkdir -p "${OUT_DIR}"

# Read pre-computed file list for this date
mapfile -t ALL_FILES < <(jq -r '.[]' "${FILE_LIST}")

# Deterministic shard slice
TOTAL=${#ALL_FILES[@]}
if (( TOTAL == 0 )); then
  echo "No files for ${DATE_FOLDER}. Exiting."
  exit 0
fi

shard_files=()
for f in "${ALL_FILES[@]}"; do
  hash=$(echo -n "$f" | md5sum | cut -c1-8)
  bucket=$(( 0x$hash % N_SHARDS ))
  if (( bucket == SHARD_ID )); then
    shard_files+=("$f")
  fi
done

echo "Shard ${SHARD_ID}/${N_SHARDS} processing ${#shard_files[@]}/${TOTAL} files"

# Local dedup cache (in-memory)
declare -A seen_hashes

OUTPUT="${OUT_DIR}/shard${SHARD_ID}-$(date +%H%M%S).jsonl"
: > "${OUTPUT}"

for rel_path in "${shard_files[@]}"; do
  # CDN download — no Authorization header required
  url="${BASE_CDN}/${rel_path}"
  tmp=$(mktemp)
  if ! curl -fsSL --retry 3 "${url}" -o "${tmp}"; then
    echo "WARN: failed to download ${url}" >&2
    rm -f "${tmp}"
    continue
  fi

  # Project to {pro

## review — reviewer @ 2026-05-02T14:05:19.009485Z

APPROVE: This is a workable, incremental step that directly addresses the 429 risk by replacing per-shard HF API pagination with a pre-computed manifest and CDN downloads, while adding local dedup to reduce redundant uploads.

Acceptance criteria a downstream tester could check:
- `bin/build-manifest.sh <date-folder>` produces valid `filelist/file-list-<date-folder>.json` containing only file `rfilename` entries (no directories) and exits 0 when the repo/tree is reachable.
- Workflow runs the manifest step before the matrix, uploads it as an artifact, and each shard job downloads the same artifact; `FILE_LIST` env var is set and readable in `dataset-enrich.sh`.
- Each shard deterministically selects its slice from the manifest (consistent across runs) and skips files assigned to other shards; total shard coverage across all 16 shards equals the full file list with no gaps or overlaps.
- Downloads use CDN URLs (`https://huggingface.co/datasets/.../resolve/main/...`) without requiring `Authorization` headers; failed downloads are logged and skipped without aborting the shard.
- Local in-memory dedup prevents duplicate `{prompt,response}` pairs within the same shard run; only non-empty outputs are uploaded via `huggingface-cli upload` with the provided token.

## perf — axentx-perf @ 2026-05-02T14:05:34.928846Z

{"verdict": "OK", "findings": [{"severity": "med", "class": "unbounded-query", "detail": "Manifest generation via `bin/build-manifest.sh` still traverses the repo/tree to enumerate files; if the repo is large or tree traversal is unoptimized, this can be CPU/I/O heavy and slow CI startup.", "mitigation": "Cache the manifest artifact aggressively and only rebuild when the date-folder changes; consider shallow or sparse tree traversal to bound work."}, {"severity": "low", "class": "memory-leak", "detail": "In-memory dedup within each shard stores `{prompt,response}` pairs for the shard lifetime; large shards could increase memory pressure and GC pauses.", "mitigation": "Bound the dedup cache size (e.g., LRU) or use probabilistic structures (Bloom) if exact dedup isn't strictly required."}, {"severity": "low", "class": "sync-in-async", "detail": "If `huggingface-cli upload` is invoked synchronously per file in a loop, it may underutilize concurrency and increase wall-clock time per shard.", "mitigation": "Batch uploads where supported or run uploads concurrently (with bounded parallelism) to reduce per-shard duration."}], "summary": "The change eliminates per-shard HF API pagination and replaces it with a pre-computed manifest + CDN downloads, which removes the 429 risk and reduces API load. Deterministic sharding and local dedup are sensible. No HIGH perf risks; two medium/low notes for manifest build cost and memory/concurrency tuning."}

## qa — perf @ 2026-05-02T14:05:34.928961Z

{"verdict": "OK", "findings": [{"severity": "med", "class": "unbounded-query", "detail": "Manifest generation via `bin/build-manifest.sh` still traverses the repo/tree to enumerate files; if the repo is large or tree traversal is unoptimized, this can be CPU/I/O heavy and slow CI startup.", "mitigation": "Cache the manifest artifact aggressively and only rebuild when the date-folder changes; consider shallow or sparse tree traversal to bound work."}, {"severity": "low", "class": "memory-leak", "detail": "In-memory dedup within each shard stores `{prompt,response}` pairs for the shard lifetime; large shards could increase memory pressure and GC pauses.", "mitigation": "Bound the dedup cache size (e.g., LRU) or use probabilistic structures (Bloom) if exact dedup isn't strictly required."}, {"severity": "low", "class": "sync-in-async", "detail": "If `huggingface-cli upload` is invoked synchronously per file in a loop, it may underutilize concurrency and increase wall-clock time per shard.", "mitigation": "Batch uploads where supported or run uploads concurrently (with bounded parallelism) to reduce per-shard duration."}], "summary": "The change eliminates per-shard HF API pagination and replaces it with a pre-computed manifest + CDN downloads, which removes the 429 risk and reduces API load. Deterministic sharding and local dedup are sensible. No HIGH perf risks; two medium/low notes for manifest build cost and memory/concurrency tuning."}
