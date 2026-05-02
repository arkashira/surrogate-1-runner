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

## review — reviewer @ 2026-05-02T13:24:10.003696Z

APPROVE: identifies a real duplicate-ingestion problem and proposes a concrete, low-risk CDN-based cross-run dedup index that can be implemented and tested within the 2-hour window; acceptance criteria below provide a clear path to verify correctness without blocking on style or exhaustive edge cases.

Acceptance criteria (downstream tester can check):
- `bin/cross_run_dedup.py` is executable (`chmod +x`) and runs `python3 bin/cross_run_dedup.py --list` without error (returns 0 and empty output when index missing, or newline-separated slugs when present).
- Cross-run dedup check works via CDN: when `index/processed_slugs.txt` exists in the HF dataset repo, `--list` returns its contents; when absent, returns empty set (404 handled gracefully).
- Append-and-upload path works in a dry-run mode (or with a test repo): `python3 bin/cross_run_dedup.py --append --slug owner/repo --shard 1 --ts test123` creates `index/processed_slugs_shard1-test123.txt` locally and attempts upload (HF_TOKEN required for real upload; CI can gate on token presence).
- `bin/dataset-enrich.sh` (or equivalent ingestion driver) skips already-processed slugs: for a slug present in the CDN index, the ingestion job does not produce a new `batches/public-merged/...` file for that slug in that shard run.
- No regressions in existing SQLite intra-run/source dedup: local dedup still prevents duplicates within the same shard run even when CDN index is empty or unavailable.

## security — axentx-security @ 2026-05-02T13:24:18.618995Z

{"verdict": "OK", "findings": [{"severity": "med", "class": "ssrf", "detail": "CDN-backed index fetch from Hugging Face can be abused via SSRF if URL construction permits attacker-controlled hostnames or redirects.", "mitigation": "Pin the CDN hostname, disable redirects, and validate/whitelist responses to Hugging Face dataset paths only."}, {"severity": "med", "class": "broken-auth", "detail": "HF_TOKEN usage for uploads may leak via logs or environment inspection if not carefully guarded.", "mitigation": "Mask HF_TOKEN in logs, require short-lived tokens where possible, and restrict upload scope to the minimal dataset repo."}, {"severity": "low", "class": "race", "detail": "Concurrent append-and-upload across runners could produce lost updates or duplicate entries in processed_slugs files.", "mitigation": "Use atomic compare-and-swap (ETag/If-Match) or a locking mechanism when updating the remote index file."}], "summary": "No critical or high-severity issues; medium SSRF and auth handling risks plus a low race condition are noted and can be mitigated without blocking the change."}

## qa — security @ 2026-05-02T13:24:18.619049Z

{"verdict": "OK", "findings": [{"severity": "med", "class": "ssrf", "detail": "CDN-backed index fetch from Hugging Face can be abused via SSRF if URL construction permits attacker-controlled hostnames or redirects.", "mitigation": "Pin the CDN hostname, disable redirects, and validate/whitelist responses to Hugging Face dataset paths only."}, {"severity": "med", "class": "broken-auth", "detail": "HF_TOKEN usage for uploads may leak via logs or environment inspection if not carefully guarded.", "mitigation": "Mask HF_TOKEN in logs, require short-lived tokens where possible, and restrict upload scope to the minimal dataset repo."}, {"severity": "low", "class": "race", "detail": "Concurrent append-and-upload across runners could produce lost updates or duplicate entries in processed_slugs files.", "mitigation": "Use atomic compare-and-swap (ETag/If-Match) or a locking mechanism when updating the remote index file."}], "summary": "No critical or high-severity issues; medium SSRF and auth handling risks plus a low race condition are noted and can be mitigated without blocking the change."}
