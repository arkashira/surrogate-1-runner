# axentx-dev-bot decision
- id: `20260502-233121-surrogate-1-discovery-b2a9da59`
- project: surrogate-1
- focus: discovery
- created_at: 2026-05-02T23:31:21.362103Z

## dev — claude/llm-fallback-chain @ 2026-05-02T23:31:21.362206Z

## Final Implementation (merged & hardened)

**Core change**: Replace all runtime `datasets.load_dataset(streaming=True)` and recursive `list_repo_files` calls in `bin/dataset-enrich.sh` with a deterministic, pre-flight snapshot + CDN-only ingestion.  
This eliminates HF API rate limits (429), pyarrow `CastError` from mixed schemas, and keeps the 16-shard parallelism intact.

---

### 1) Snapshot generator (single source of truth)

`bin/make-snapshot.py`

- Runs once per date folder (cron or manual) from orchestrator/Mac.
- Uses **one non-recursive** `list_repo_tree` per folder to avoid pagination storms.
- Emits `snapshot/<date>/snapshot.json` containing `{repo, date, files:[{path, cdn_url, size, sha}]}`.
- Commits snapshot to repo **or** passes via workflow artifact so every shard sees identical file list.

```python
#!/usr/bin/env python3
"""
Generate snapshot.json for a date folder in axentx/surrogate-1-training-pairs.

Usage:
  HF_TOKEN=<token> python bin/make-snapshot.py \
    --repo axentx/surrogate-1-training-pairs \
    --date 2026-05-02 \
    --out snapshot/2026-05-02/snapshot.json
"""
import argparse
import json
import os
import sys
from huggingface_hub import HfApi

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default="axentx/surrogate-1-training-pairs")
    parser.add_argument("--date", required=True, help="Date folder, e.g. 2026-05-02")
    parser.add_argument("--out", required=True, help="Output snapshot.json path")
    args = parser.parse_args()

    token = os.environ.get("HF_TOKEN")
    api = HfApi(token=token) if token else HfApi()

    folder = f"batches/public-merged/{args.date}"
    entries = api.list_repo_tree(
        repo_id=args.repo,
        path=folder,
        repo_type="dataset",
        recursive=False,
    )

    snapshot = {
        "repo": args.repo,
        "date": args.date,
        "folder": folder,
        "files": [],
    }

    for entry in entries:
        if getattr(entry, "type", None) != "file":
            continue
        cdn_url = (
            f"https://huggingface.co/datasets/{args.repo}/resolve/main/"
            f"{folder}/{entry.path}"
        )
        snapshot["files"].append(
            {
                "path": entry.path,
                "cdn_url": cdn_url,
                "size": getattr(entry, "size", None),
                "sha": getattr(entry, "sha", None),
            }
        )

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2)

    print(f"Wrote {len(snapshot['files'])} files to {args.out}", file=sys.stderr)

if __name__ == "__main__":
    main()
```

```bash
chmod +x bin/make-snapshot.py
```

---

### 2) Lightweight CDN fetcher (retry + idempotent)

`bin/lib/fetch-cdn.sh`

```bash
#!/usr/bin/env bash
# Lightweight CDN fetcher with retries.
# Usage: fetch-cdn.sh <cdn_url> <output_path>
set -euo pipefail

cdn_url="$1"
out="$2"

curl --fail --silent --show-error \
  --retry 5 --retry-delay 5 \
  --max-time 300 \
  --output "${out}" \
  "${cdn_url}"
```

```bash
chmod +x bin/lib/fetch-cdn.sh
```

---

### 3) Updated ingestion script (CDN-only mode)

Key changes to `bin/dataset-enrich.sh`:

- Accept `SNAPSHOT` path (default: `snapshot/latest/snapshot.json`).
- If snapshot provided → **CDN-only mode** (no `datasets` API calls).
- Deterministic shard assignment by file index (stable across runners).
- Per-shard isolation preserved (7 GB each).
- Project to `{prompt, response}` only at parse time (avoids schema mixing).
- Keep legacy fallback for compatibility (avoid in production).

```bash
#!/usr/bin/env bash
# ... existing header ...

SNAPSHOT="${SNAPSHOT:-snapshot/latest/snapshot.json}"   # optional
DATE_DIR="${DATE_DIR:-}"                               # required if no snapshot
WORK_DIR="${WORK_DIR:-$(mktemp -d)}"
TOTAL_SHARDS="${TOTAL_SHARDS:-16}"
SHARD_ID="${SHARD_ID:-0}"

# CDN-only mode (preferred)
if [[ -n "${SN

## review — reviewer @ 2026-05-02T23:31:50.801252Z

APPROVE: The snapshot + CDN-only ingestion is a workable, incremental step that directly addresses the stated discovery goals (eliminates HF API rate limits and pyarrow CastError) while preserving parallelism and providing a clear path for deterministic, reproducible runs.

Acceptance criteria:
- `bin/make-snapshot.py` can be run locally/CI with `HF_TOKEN` and produces a valid `snapshot/<date>/snapshot.json` containing repo/date/folder/files entries with cdn_url, size, sha.
- `bin/lib/fetch-cdn.sh` succeeds on valid CDN URLs with retries and writes content to the specified output path; non-zero exit on unrecoverable failures.
- `bin/dataset-enrich.sh` in CDN-only mode (SNAPSHOT provided) assigns files to shards deterministically by index, fetches via CDN, parses only `{prompt,response}`, and emits `shard-<id>.jsonl` without invoking `datasets.load_dataset` or recursive repo calls.
- Legacy fallback in `bin/dataset-enrich.sh` remains present but is clearly marked as not for production and can be disabled by default.
- Snapshot file or workflow artifact is propagated to all shard runners so every shard sees an identical file list; snapshot generation can be wired into cron or manual pre-flight step.

## qa — perf @ 2026-05-02T23:31:56.964939Z

[perf-pass-failed]
