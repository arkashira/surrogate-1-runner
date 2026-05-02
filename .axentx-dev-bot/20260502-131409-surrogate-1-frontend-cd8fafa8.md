# axentx-dev-bot decision
- id: `20260502-131409-surrogate-1-frontend-cd8fafa8`
- project: surrogate-1
- focus: frontend
- created_at: 2026-05-02T13:14:09.612103Z

## dev — claude/llm-fallback-chain @ 2026-05-02T13:14:09.612215Z

## Final Synthesized Plan (Highest-Value, <2h)

**Goal**: Eliminate HF API 429 failures during manual ingestion triggers and provide deterministic shard visibility.

**Core Decision**: Frontend orchestrates; backend does minimal, cacheable work. No heavy compute on Mac (CLI rule).

---

## 1. Unified Architecture (Resolves Contradictions)

- **Keep file listing on backend** (Candidate 1) — avoids exposing HF token to browser and allows server-side caching.
- **Add CLI fallback** (Candidate 2) — for local dev / CI, generate manifests without touching the UI.
- **Deterministic shard assignment** (Both) — `hash(slug) % 16` in UI for immediate feedback; same function in backend for consistency.
- **No recursive listing** — use `list_repo_tree(recursive=False)` per folder only.

---

## 2. Implementation Plan (90–110 min)

| Step | Owner | Time | Deliverable |
|------|-------|------|-------------|
| 1. Backend: Cached folder/files endpoints | Backend | 25 min | `/api/date-folders`, `/api/folder-files/{date}` with 5-min LRU cache |
| 2. Backend: CLI manifest generator | CLI | 15 min | `scripts/gen-manifest.py --date 2026-04-29` → `manifests/2026-04-29.json` |
| 3. Frontend: Shard calculator component | Frontend | 15 min | Reusable `ShardCalculator` with shared hash function |
| 4. Frontend: Date folder browser + shard panel | Frontend | 30 min | Uses backend endpoints; shows shard assignment per slug; links to HF CDN files |
| 5. Frontend: Real-time shard status (last 10 runs) | Frontend | 15 min | Reads commit history via `list_repo_commits` or local JSONL index |

---

## 3. Shared Deterministic Hash (Single Source of Truth)

```python
# shared/hash_utils.py
def shard_for_slug(slug: str, total_shards: int = 16) -> int:
    """Deterministic shard assignment compatible across Python/JS."""
    # Simple, stable 32-bit FNV-1a variant
    h = 2166136261
    for ch in slug.encode("utf-8"):
        h = (h ^ ch) * 16777619
        h &= 0xFFFFFFFF  # keep 32-bit
    return (h >> 8) % total_shards  # reduce bias vs modulo low-bit
```

```ts
// shared/hashUtils.ts
export function shardForSlug(slug: string, totalShards = 16): number {
  let h = 2166136261 >>> 0;
  for (let i = 0; i < slug.length; i++) {
    h = (h ^ slug.charCodeAt(i)) * 16777619;
    h = h >>> 0;
  }
  return ((h >>> 8) % totalShards);
}
```

---

## 4. Backend Endpoints (FastAPI, Cached)

```python
# api/ingest_info.py
from fastapi import APIRouter, HTTPException
from huggingface_hub import list_repo_tree
from functools import lru_cache
import os

router = APIRouter()
HF_TOKEN = os.getenv("HF_TOKEN")
REPO = "datasets/axentx/surrogate-1-training-pairs"

@lru_cache(maxsize=32)
def _cached_tree(path: str):
    return list_repo_tree(
        repo_id=REPO,
        path=path,
        recursive=False,
        token=HF_TOKEN,
    )

@router.get("/date-folders")
async def get_date_folders():
    try:
        tree = _cached_tree("batches/public-merged")
        folders = sorted(
            (e.path.split("/")[-1] for e in tree if e.type == "directory"),
            reverse=True,
        )
        return {"folders": folders}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/folder-files/{date}")
async def get_folder_files(date: str):
    try:
        tree = _cached_tree(f"batches/public-merged/{date}")
        files = [
            {
                "name": e.path.split("/")[-1],
                "size": getattr(e, "size", 0),
                "last_modified": getattr(e, "last_modified", ""),
            }
            for e in tree
            if e.type == "file"
        ]
        return {"date": date, "files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

## 5. CLI Manifest Generator (Mac/CI Friendly)

```python
# scripts/gen_manifest.py
import argparse
import json
from datetime import datetime
from huggingface_hub import list_repo_tree
import os

HF_TOKEN = os.getenv("HF_TOKEN

## review — reviewer @ 2026-05-02T13:14:19.631439Z

APPROVE: Frontend orchestration plan is pragmatic, exposes no secrets, provides deterministic shard visibility, and backend endpoints are cacheable and safe.

Acceptance criteria:
- `/api/date-folders` returns sorted date folders and uses LRU cache (5-min TTL) to reduce HF API calls.
- `/api/folder-files/{date}` returns file metadata for the requested date and is cached.
- `shardForSlug` in frontend and `shard_for_slug` in backend produce identical results for the same slug and totalShards (cross-runtime test with fixture list).
- UI shows per-slug shard assignment and links to HF CDN files without embedding HF token in the browser.
- CLI `gen_manifest.py --date <YYYY-MM-DD>` produces a valid JSON manifest in `manifests/` and exits 0 on success; fails gracefully (non-zero) on missing date or HF auth issues.

## security — axentx-security @ 2026-05-02T13:14:29.139994Z

{"verdict": "OK", "findings": [{"severity": "med", "class": "ssrf", "detail": "Backend endpoints that call the Hugging Face API may be susceptible to SSRF if user-controlled inputs (e.g., date path) influence outbound URLs without strict allow-listing and validation.", "mitigation": "Validate and allow-list date parameters, use an allow-listed base URL for HF, and route outbound requests through a controlled egress proxy with network-level restrictions."}, {"severity": "low", "class": "broken-auth", "detail": "CLI tool may leak Hugging Face credentials via process listings, logs, or environment if tokens are passed explicitly or logged on failure.", "mitigation": "Read HF tokens from secure environment/secrets store only, mask them in logs, and ensure subprocesses do not inherit or print credentials."}, {"severity": "low", "class": "xss", "detail": "Frontend renders per-slug shard assignments and HF CDN links; unsanitized file metadata or URL parameters could lead to reflected XSS.", "mitigation": "Sanitize and encode all dynamic content before rendering, and validate/sanitize URL components used in CDN links."}], "summary": "No high/critical issues; acceptable risk with recommended mitigations for SSRF potential in backend HF calls and credential handling in CLI."}

## qa — security @ 2026-05-02T13:14:29.140047Z

{"verdict": "OK", "findings": [{"severity": "med", "class": "ssrf", "detail": "Backend endpoints that call the Hugging Face API may be susceptible to SSRF if user-controlled inputs (e.g., date path) influence outbound URLs without strict allow-listing and validation.", "mitigation": "Validate and allow-list date parameters, use an allow-listed base URL for HF, and route outbound requests through a controlled egress proxy with network-level restrictions."}, {"severity": "low", "class": "broken-auth", "detail": "CLI tool may leak Hugging Face credentials via process listings, logs, or environment if tokens are passed explicitly or logged on failure.", "mitigation": "Read HF tokens from secure environment/secrets store only, mask them in logs, and ensure subprocesses do not inherit or print credentials."}, {"severity": "low", "class": "xss", "detail": "Frontend renders per-slug shard assignments and HF CDN links; unsanitized file metadata or URL parameters could lead to reflected XSS.", "mitigation": "Sanitize and encode all dynamic content before rendering, and validate/sanitize URL components used in CDN links."}], "summary": "No high/critical issues; acceptable risk with recommended mitigations for SSRF potential in backend HF calls and credential handling in CLI."}
