# axentx-dev-bot decision
- id: `20260503-002237-surrogate-1-frontend-ec0f3c60`
- project: surrogate-1
- focus: frontend
- created_at: 2026-05-03T00:22:37.433092Z

## dev — claude/llm-fallback-chain @ 2026-05-03T00:22:37.433152Z

## Final Implementation Plan — CDN-first snapshot + zero-HF-API ingestion

**Highest-value improvement (≤2h)**  
Add `bin/snapshot.sh` that produces a deterministic file manifest per date folder and update ingestion/training to use CDN URLs exclusively when a snapshot is provided. This:

- Eliminates recursive `list_repo_files`/`list_repo_tree` calls during training (prevents 429s).  
- Enables Lightning training to do CDN-only fetches with zero HF API calls during data load.  
- Keeps the existing 16-shard runner unchanged (it already uses HF API on the Mac orchestrator, which is acceptable).  
- Reuses the existing `bin/dataset-enrich.sh` workflow so no retraining of infra is required.

---

### Concrete steps (order)

1. Add `bin/snapshot.sh`  
   - Accepts `REPO`, `DATE` (YYYY-MM-DD), optional `OUT_JSON`.  
   - Uses `huggingface_hub.list_repo_tree(path=f"{DATE}", recursive=False)` (single non-recursive call).  
   - Emits JSON array of `{ "path": "...", "cdn_url": "https://huggingface.co/datasets/REPO/resolve/main/...", "size": int }`.  
   - Deterministic sort by path.  
   - Shebang `#!/usr/bin/env bash`, `set -euo pipefail`.  
   - Executable (`chmod +x`).  

2. Add `bin/snapshot.py` (optional helper used by snapshot.sh)  
   - Pure Python to call HF Hub and emit JSON.  
   - Shebang `#!/usr/bin/env python3`, `if __name__ == "__main__"`.  
   - Handles pagination safely (non-recursive, single level).  

3. Update training script (`train.py` or equivalent)  
   - Accept `--snapshot JSON_PATH`.  
   - If provided, build a `WebDataset`/`IterableDataset` that streams from CDN URLs directly (no `load_dataset`).  
   - Project to `{prompt, response}` at parse time (preserve existing schema-projection behavior).  
   - Fallback: if no snapshot, keep current behavior but log warning about HF API usage.  

4. Update ingestion runner guidance (README or comment)  
   - Document how to produce snapshot before training.  
   - Note: Mac runs snapshot once per date folder after rate-limit window clears; Lightning training uses snapshot JSON (CDN-only).  

5. Small infra polish  
   - Ensure `requirements.txt` includes `huggingface_hub`, `webdataset` (if using WebDataset), `requests`.  
   - Add `.gitignore` entry for snapshot JSONs if needed.  

---

### Code snippets

#### `bin/snapshot.py`

```python
#!/usr/bin/env python3
"""
Produce a deterministic CDN manifest for a date folder in a HuggingFace dataset repo.

Usage:
  ./bin/snapshot.py --repo axentx/surrogate-1-training-pairs --date 2026-04-29 --out snapshot.json
"""

import argparse
import json
import sys
from pathlib import Path

from huggingface_hub import HfApi

CDN_TEMPLATE = "https://huggingface.co/datasets/{repo}/resolve/main/{path}"

def main() -> None:
    parser = argparse.ArgumentParser(description="Create CDN snapshot for a dataset date folder.")
    parser.add_argument("--repo", required=True, help="HF dataset repo (e.g. axentx/surrogate-1-training-pairs)")
    parser.add_argument("--date", required=True, help="Date folder (YYYY-MM-DD)")
    parser.add_argument("--out", default="snapshot.json", help="Output JSON path")
    args = parser.parse_args()

    api = HfApi()
    prefix = args.date.rstrip("/") + "/"
    entries = api.list_repo_tree(repo_id=args.repo, path=prefix, recursive=False)

    files = []
    for e in entries:
        if getattr(e, "type", None) == "file" or (hasattr(e, "path") and not e.path.endswith("/")):
            path = e.path
            files.append(
                {
                    "path": path,
                    "cdn_url": CDN_TEMPLATE.format(repo=args.repo, path=path),
                    "size": getattr(e, "size", 0),
                }
            )

    files.sort(key=lambda x: x["path"])

    out_path = Path(args.out)
    out_path.write_text(json.dumps(files, indent=2) + "\n")
    print(f"Wrote {len(files)} files to {out_path}", file=sys.stderr)

if __name__ == "__main__":
    main()
```

#### `bin/snapshot.sh`

```bash
#!/usr

## review — reviewer @ 2026-05-03T00:22:42.567834Z

APPROVE: Provides a clear, incremental path to eliminate HF API calls during training with concrete, runnable artifacts and fallback behavior.

Acceptance criteria:
- `bin/snapshot.py` and `bin/snapshot.sh` are added, executable, and produce deterministic JSON sorted by path for a given repo/date.
- Training script accepts `--snapshot JSON_PATH` and, when provided, streams samples from CDN URLs without invoking `load_dataset`/HF API listing calls (keeps existing behavior otherwise with a warning).
- The snapshot JSON schema matches `{path, cdn_url, size}` and uses `https://huggingface.co/datasets/{repo}/resolve/main/{path}` URLs.
- README/runbook documents the snapshot generation step and the intended workflow (Mac creates snapshot after rate-limit window; Lightning training uses snapshot for CDN-only fetches).
- Dependencies (`huggingface_hub`, `webdataset` or chosen streaming loader, `requests`) are listed in `requirements.txt`; snapshot JSONs are gitignored or documented as ephemeral build artifacts.

## perf — axentx-perf @ 2026-05-03T00:22:51.474277Z

{"verdict": "OK", "findings": [{"severity": "med", "class": "unbounded-query", "detail": "Without snapshot, training still falls back to HF API listing calls (load_dataset) which can trigger unbounded metadata queries and rate limits at scale. Snapshot path eliminates this, but fallback remains a perf risk if misconfigured.", "mitigation": "Make fallback opt-in (disabled by default in prod) or require snapshot in non-dev environments; add timeout/retry budget and circuit-breaker around HF API fallback."}, {"severity": "low", "class": "other", "detail": "Streaming from CDN URLs can amplify tail latency (many small HTTP requests). No batching or prefetch hint in criteria.", "mitigation": "Use bounded parallelism, connection pooling, and prefetch buffering in the streaming loader; optionally shard snapshot to enable parallel workers without thundering herd."}, {"severity": "low", "class": "memory-leak", "detail": "Streaming loader may retain open file handles or HTTP sessions across epochs if not closed deterministically.", "mitigation": "Ensure loader lifecycle is scoped per epoch/worker with explicit close/teardown; use context managers and limit keep-alive duration."}], "summary": "Snapshot-driven CDN-only path removes HF API listing and enables deterministic, scalable data ingestion. Fallback to HF API preserves correctness but retains unbounded-query risk; recommend gating fallback in prod. Low-risk tail-latency and resource-cleanup concerns are manageable with standard streaming-loader best practices."}

## qa — perf @ 2026-05-03T00:22:51.474309Z

{"verdict": "OK", "findings": [{"severity": "med", "class": "unbounded-query", "detail": "Without snapshot, training still falls back to HF API listing calls (load_dataset) which can trigger unbounded metadata queries and rate limits at scale. Snapshot path eliminates this, but fallback remains a perf risk if misconfigured.", "mitigation": "Make fallback opt-in (disabled by default in prod) or require snapshot in non-dev environments; add timeout/retry budget and circuit-breaker around HF API fallback."}, {"severity": "low", "class": "other", "detail": "Streaming from CDN URLs can amplify tail latency (many small HTTP requests). No batching or prefetch hint in criteria.", "mitigation": "Use bounded parallelism, connection pooling, and prefetch buffering in the streaming loader; optionally shard snapshot to enable parallel workers without thundering herd."}, {"severity": "low", "class": "memory-leak", "detail": "Streaming loader may retain open file handles or HTTP sessions across epochs if not closed deterministically.", "mitigation": "Ensure loader lifecycle is scoped per epoch/worker with explicit close/teardown; use context managers and limit keep-alive duration."}], "summary": "Snapshot-driven CDN-only path removes HF API listing and enables deterministic, scalable data ingestion. Fallback to HF API preserves correctness but retains unbounded-query risk; recommend gating fallback in prod. Low-risk tail-latency and resource-cleanup concerns are manageable with standard streaming-loader best practices."}
