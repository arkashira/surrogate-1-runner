# axentx-dev-bot decision
- id: `20260502-235855-surrogate-1-backend-7c6ef3a3`
- project: surrogate-1
- focus: backend
- created_at: 2026-05-02T23:58:55.559543Z

## dev — claude/llm-fallback-chain @ 2026-05-02T23:58:55.559593Z

## Implementation Plan (≤2h)

**Highest-value improvement**: Add a pre-flight snapshot generator (`bin/snapshot.sh`) that lists all dataset files once per date folder, embeds the file manifest into training, and enables CDN-only downloads during parallel shard processing. This eliminates HF API rate-limit (429) during ingestion and reduces per-shard overhead by replacing recursive `list_repo_files` with a single tree call + CDN fetches.

### Concrete steps (1h 45m total)

1. **Create `bin/snapshot.sh`** (20m)  
   - Accept `DATE` (YYYY-MM-DD) or default to today.  
   - Call `huggingface_hub` Python helper to run `list_repo_tree(path=f"public-merged/{DATE}", recursive=False)` once.  
   - Save JSON to `snapshots/public-merged-{DATE}.json` containing `{ "date": "...", "files": [...], "generated_at": "...", "repo": "axentx/surrogate-1-training-pairs" }`.  
   - Make executable (`chmod +x`).

2. **Create `bin/lib/snapshot.py`** (20m)  
   - Small reusable module: `list_date_folder(date)` → list of filenames; `save_snapshot(date, files)`; `load_snapshot(date)`.  
   - Use `HF_TOKEN` optional (public repo doesn’t require auth for tree/list).  
   - Handle pagination (tree is non-paginated for folders; fallback to `list_repo_tree` recursive=False).

3. **Update `bin/dataset-enrich.sh`** (30m)  
   - Add pre-flight: if snapshot for target date exists and is <1h old, reuse; else run `snapshot.sh`.  
   - Replace per-shard recursive listing with deterministic shard-slicing over the snapshot file list:  
     - Sort files lexicographically, assign each file to `hash(filename) % 16` → `SHARD_ID`.  
     - Each runner processes only its shard’s subset.  
   - Downloads use CDN URLs: `https://huggingface.co/datasets/axentx/surrogate-1-training-pairs/resolve/main/public-merged/${DATE}/${file}` (no auth, bypasses API rate limits).  
   - Keep existing schema normalization and dedup via `lib/dedup.py`.

4. **Update GitHub Actions matrix** (15m)  
   - No change to 16-shard matrix.  
   - Add a single “snapshot” job (or step) that runs before the matrix, generates snapshot, and uploads it as an artifact for all shards to download.  
   - Alternatively, each shard can run snapshot locally if missing (idempotent, cheap).

5. **Add training integration stub** (20m)  
   - Create `bin/train-file-list.sh` that outputs newline-separated CDN URLs for a given date (for embedding into Lightning training).  
   - Document pattern: Mac runs snapshot once, embeds file list into `train.py`; Lightning Studio uses CDN-only `open(url)` via `datasets` or custom `IterableDataset` that never calls HF API.

6. **Tests & safety** (20m)  
   - Add dry-run flag to snapshot (`--dry-run`) to validate tree access.  
   - Validate shard assignment is deterministic (unit test in `bin/lib/test_shard.py`).  
   - Ensure script exits non-zero on tree/list failures.

7. **Documentation** (10m)  
   - Update README with snapshot usage and CDN bypass rationale.  
   - Add note about HF rate limits and the 360s backoff if 429 still occurs on tree call.

---

## Code snippets

### `bin/lib/snapshot.py`

```python
#!/usr/bin/env python3
"""
Snapshot utilities for surrogate-1 dataset folders.
"""
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from huggingface_hub import HfApi, list_repo_tree

REPO = "axentx/surrogate-1-training-pairs"
SNAPSHOT_DIR = Path(__file__).parents[2] / "snapshots"
SNAPSHOT_DIR.mkdir(exist_ok=True, parents=True)

api = HfApi()

def list_date_folder(date: str):
    """
    List files in public-merged/{date}/ (non-recursive).
    Returns list of filenames (relative to repo root).
    """
    prefix = f"public-merged/{date}/"
    try:
        files = list_repo_tree(repo_id=REPO, path=prefix, repo_type="dataset", recursive=False)
    except Exception as e:
        raise RuntimeError(f"Failed to list repo tree for {prefix}: {e}") from e
    # items are dicts with 'path'
    paths = [item["path"] for item in fil

## review — reviewer @ 2026-05-02T23:59:10.133040Z

APPROVE: The change is a workable, incremental improvement that directly targets HF API rate-limit pain (429) and replaces recursive per-shard listing with a deterministic snapshot + CDN fetches. It provides clear acceptance criteria a downstream tester can validate and keeps existing dedup/schema behavior intact.

Acceptance criteria:
- `bin/lib/snapshot.py` can list a date folder via `list_repo_tree` (non-recursive) and produce valid `snapshots/public-merged-YYYY-MM-DD.json` with the expected schema (`repo`, `date`, `generated_at`, `files`).
- `bin/snapshot.sh` accepts an optional `DATE` (YYYY-MM-DD, defaults to today), runs the snapshot generator, and exits non-zero on tree/list failures.
- `bin/dataset-enrich.sh` uses the snapshot when present and <1h old; shard assignment is deterministic (sort filenames, `hash(filename) % 16`) and each shard only processes its subset; downloads use CDN URLs without HF API calls.
- GitHub Actions runs a snapshot step (or job) before the 16-shard matrix and makes the snapshot artifact available to shards (or shards can generate locally if missing) — matrix behavior remains unchanged.
- Dry-run flag (`--dry-run`) on snapshot validates tree access without writing; unit test in `bin/lib/test_shard.py` confirms deterministic shard assignment; scripts exit non-zero on tree/list failures.
- README documents snapshot usage, CDN bypass rationale, and notes HF rate-limit handling (including 360s backoff if 429 occurs).

## security — axentx-security @ 2026-05-02T23:59:15.900685Z

{"verdict": "OK", "findings": [{"severity": "med", "class": "ssrf", "detail": "CDN URL construction from repo/tree data without strict allowlist/validation could let an attacker pivot internal fetches via malicious repo filenames or redirect targets.", "mitigation": "Validate and allowlist CDN hostnames and path patterns; reject unexpected schemes/hosts and use network egress controls."}, {"severity": "low", "class": "race", "detail": "Snapshot file freshness check (<1h) and use across concurrent shard processes may race with snapshot generation or updates, leading to inconsistent shard subsets.", "mitigation": "Use atomic writes and file locks or a single authoritative snapshot artifact passed to shards to ensure consistency."}, {"severity": "low", "class": "other", "detail": "Deterministic shard assignment via hash(filename) % 16 may leak filename distribution and enable targeted shard DoS if attackers control filenames.", "mitigation": "Consider salting the hash or using a stronger stable assignment and monitor shard load skew."}], "summary": "No critical or high issues; medium SSRF risk from CDN URL handling and low risks around snapshot races and shard targeting remain."}

## qa — security @ 2026-05-02T23:59:15.900713Z

{"verdict": "OK", "findings": [{"severity": "med", "class": "ssrf", "detail": "CDN URL construction from repo/tree data without strict allowlist/validation could let an attacker pivot internal fetches via malicious repo filenames or redirect targets.", "mitigation": "Validate and allowlist CDN hostnames and path patterns; reject unexpected schemes/hosts and use network egress controls."}, {"severity": "low", "class": "race", "detail": "Snapshot file freshness check (<1h) and use across concurrent shard processes may race with snapshot generation or updates, leading to inconsistent shard subsets.", "mitigation": "Use atomic writes and file locks or a single authoritative snapshot artifact passed to shards to ensure consistency."}, {"severity": "low", "class": "other", "detail": "Deterministic shard assignment via hash(filename) % 16 may leak filename distribution and enable targeted shard DoS if attackers control filenames.", "mitigation": "Consider salting the hash or using a stronger stable assignment and monitor shard load skew."}], "summary": "No critical or high issues; medium SSRF risk from CDN URL handling and low risks around snapshot races and shard targeting remain."}
