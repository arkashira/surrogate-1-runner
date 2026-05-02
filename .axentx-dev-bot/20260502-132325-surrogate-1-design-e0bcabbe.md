# axentx-dev-bot decision
- id: `20260502-132325-surrogate-1-design-e0bcabbe`
- project: surrogate-1
- focus: design
- created_at: 2026-05-02T13:23:25.883015Z

## dev — claude/llm-fallback-chain @ 2026-05-02T13:23:25.883107Z

## Final Synthesized Implementation Plan (≤2h)

**Chosen problem**: eliminate cross-run duplicate ingestion in the 16-shard GitHub Actions pipeline.  
**Why**: Candidate 1 correctly identifies the concrete waste (bandwidth, dataset bloat, repeated `batches/public-merged/...` files) and proposes a CDN-only, zero-auth-check mechanism that is safe, fast to implement, and Mac-compatible. Candidate 2’s CDN advice is useful generally but mis-targeted here (it optimizes downloads, not duplicate suppression) and would require larger refactors to be actionable in <2h.

We adopt Candidate 1’s cross-run dedup index as the primary improvement and incorporate Candidate 2’s low-cost CDN usage pattern where it aligns (lightweight, no-auth fetches). We drop Candidate 2’s `list_repo_tree`/JSON pre-listing because it is redundant and adds complexity without solving the stated duplicate problem.

---

## 1) Core design (correctness + actionability)

- **Cross-run dedup index**: `index/processed_slugs.txt` in the HF dataset repo.
- **Check via CDN only**: `https://huggingface.co/datasets/{HF_DATASET}/resolve/main/index/processed_slugs.txt` (no auth, no rate-limit).
- **Append per shard**: each shard writes `index/processed_slugs_shard{N}-{TS}.txt` and uploads once at end of run. No coordination or locking required.
- **Keep SQLite dedup**: remains source of truth for intra-run/source dedup.
- **No changes to HF Space or training code**.
- **Mac/local unchanged**: ingestion still runs in Actions; orchestration only.

---

## 2) Implementation (≤2h)

### 2.1 `bin/cross_run_dedup.py`

```python
#!/usr/bin/env python3
"""
Cross-run dedup index for surrogate-1 public ingest.
Uses HF CDN (no auth/API) to check prior processed slugs.
"""
import os
import sys
import requests
from pathlib import Path
from typing import Set, Optional

HF_DATASET = os.getenv("HF_DATASET", "axentx/surrogate-1-training-pairs")
CDN_ROOT = f"https://huggingface.co/datasets/{HF_DATASET}/resolve/main"
INDEX_DIR = Path(__file__).parent.parent / "index"
INDEX_DIR.mkdir(exist_ok=True, parents=True)

def _cdn_get(path: str) -> requests.Response:
    url = f"{CDN_ROOT}/{path.lstrip('/')}"
    r = requests.get(url, timeout=10)
    return r

def list_processed_slugs(index_file: str = "index/processed_slugs.txt") -> Set[str]:
    r = _cdn_get(index_file)
    if r.status_code == 404:
        return set()
    r.raise_for_status()
    return {line.strip() for line in r.text.splitlines() if line.strip()}

def is_processed(slug: str, processed: Optional[Set[str]] = None) -> bool:
    if processed is None:
        processed = list_processed_slugs()
    return slug in processed

def append_processed_local(slug: str, shard_id: int, ts: str, out_dir: Path = INDEX_DIR) -> Path:
    out_dir.mkdir(exist_ok=True, parents=True)
    p = out_dir / f"processed_slugs_shard{shard_id}-{ts}.txt"
    with open(p, "a", encoding="utf-8") as f:
        f.write(f"{slug}\n")
    return p

def upload_index_file(local_path: Path, repo_path: str):
    from huggingface_hub import upload_file
    upload_file(
        path_or_fileobj=str(local_path),
        path_in_repo=repo_path,
        repo_id=HF_DATASET,
        repo_type="dataset",
        token=os.environ["HF_TOKEN"],
    )

def main_cli():
    import argparse
    parser = argparse.ArgumentParser(description="Cross-run dedup helpers")
    parser.add_argument("--list", action="store_true", help="List processed slugs (one per line)")
    parser.add_argument("--append", action="store_true", help="Append a slug")
    parser.add_argument("--slug", help="Slug to append")
    parser.add_argument("--shard", type=int, default=int(os.getenv("SHARD_ID", 0)), help="Shard ID")
    parser.add_argument("--ts", default=os.getenv("RUN_TS", ""), help="Timestamp string")
    args = parser.parse_args()

    if args.list:
        for s in sorted(list_processed_slugs()):
            print(s)
        return

    if args.append:
        if not args.slug:
            parser.error("--appe

## review — reviewer @ 2026-05-02T13:23:51.504801Z

APPROVE: implements a clear, low-risk cross-run dedup mechanism using CDN reads and per-shard append-only files; provides a functional CLI and integration hook that a downstream tester can validate without touching auth/Space/training code.

Acceptance criteria:
- `python3 bin/cross_run_dedup.py --list` returns 0 and prints slugs (or nothing) when the CDN file exists or 404s; non-404 failures exit non-zero.
- `python3 bin/cross_run_dedup.py --append --slug owner/repo --shard 1 --ts 20240101-000000` appends locally and uploads `index/processed_slugs_shard1-20240101-000000.txt` to HF_DATASET using HF_TOKEN.
- `bin/dataset-enrich.sh` skips slugs present in the preloaded `PROCESSED` list (exact match) before enrichment steps.
- No regressions in existing SQLite intra-run/source dedup behavior (same output row count for unique slugs within a shard).
- HF_TOKEN is only used for uploads (not required for `--list`), and CDN URLs remain publicly readable without tokens.

## security — axentx-security @ 2026-05-02T13:23:59.042746Z

{"verdict": "OK", "findings": [{"severity": "med", "class": "secret-leak", "detail": "CLI arguments (e.g., --slug, --shard, --ts) may leak into process listings or shell history and could expose repo names or shard topology.", "mitigation": "Avoid passing sensitive identifiers on the command line; use environment variables or stdin, and scrub shell history where feasible."}, {"severity": "low", "class": "ssrf", "detail": "CDN reads and HF_DATASET uploads may follow redirects to internal endpoints if URL validation is weak.", "mitigation": "Restrict redirects and validate hostnames against an allowlist for CDN and HF_DATASET endpoints."}, {"severity": "low", "class": "race", "detail": "Per-shard append-only files may allow TOCTOU or interleaved writes if concurrent instances run without coordination.", "mitigation": "Use atomic append (O_APPEND) and file locking or an external coordinator to serialize shard writes."}], "summary": "No high/crit issues; design is low-risk with acceptable mitigations for medium secret-leak and low SSRF/race concerns."}

## qa — security @ 2026-05-02T13:23:59.042791Z

{"verdict": "OK", "findings": [{"severity": "med", "class": "secret-leak", "detail": "CLI arguments (e.g., --slug, --shard, --ts) may leak into process listings or shell history and could expose repo names or shard topology.", "mitigation": "Avoid passing sensitive identifiers on the command line; use environment variables or stdin, and scrub shell history where feasible."}, {"severity": "low", "class": "ssrf", "detail": "CDN reads and HF_DATASET uploads may follow redirects to internal endpoints if URL validation is weak.", "mitigation": "Restrict redirects and validate hostnames against an allowlist for CDN and HF_DATASET endpoints."}, {"severity": "low", "class": "race", "detail": "Per-shard append-only files may allow TOCTOU or interleaved writes if concurrent instances run without coordination.", "mitigation": "Use atomic append (O_APPEND) and file locking or an external coordinator to serialize shard writes."}], "summary": "No high/crit issues; design is low-risk with acceptable mitigations for medium secret-leak and low SSRF/race concerns."}
