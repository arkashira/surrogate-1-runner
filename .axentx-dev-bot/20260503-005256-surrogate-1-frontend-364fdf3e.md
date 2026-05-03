# axentx-dev-bot decision
- id: `20260503-005256-surrogate-1-frontend-364fdf3e`
- project: surrogate-1
- focus: frontend
- created_at: 2026-05-03T00:52:56.784453Z

## dev — claude/llm-fallback-chain @ 2026-05-03T00:52:56.784504Z

## Final Implementation Plan (≤2h)

**Highest-value change**: Add a Mac-side `tools/snapshot_manifest.py` that lists one date-partition via a **single** HF API call, emits `file_manifest.json` with CDN URLs, and a training loader that uses **CDN-only** fetches (zero HF API calls during training). This implements the CDN bypass pattern and eliminates 429 rate-limit failures during data loading in Lightning Studio.

### Steps (1h 30m total)

1. **Create tools/snapshot_manifest.py** (20m)  
   - Single API call: `list_repo_tree(path=date_partition, recursive=True)`  
   - Filter to `.jsonl`/`.parquet` files  
   - Emit deterministic `file_manifest.json` with CDN URLs and sizes  
   - Include `generated_at` and `partition` metadata

2. **Create training/data_loader.py** (30m)  
   - Load `file_manifest.json`  
   - Use `datasets.load_dataset` with `data_files` pointing to CDN URLs (zero HF API calls)  
   - Parse JSONL/Parquet into Arrow format  
   - Yield `{prompt, response}` pairs

3. **Update training script** (20m)  
   - Replace `load_dataset(streaming=True)` with CDN loader  
   - Add CLI arg `--manifest file_manifest.json`  
   - Keep fallback to HF API only if manifest missing (for dev)

4. **Add to README** (10m)  
   - Usage: `python tools/snapshot_manifest.py --date 2026-05-03 --out manifest.json`  
   - Note: Manifest generation requires HF token; training does not

5. **Test locally** (10m)  
   - Generate manifest for a small date partition  
   - Run training loader, verify records parsed

---

## Code Snippets

### tools/snapshot_manifest.py
```python
#!/usr/bin/env python3
"""
Generate CDN-only file manifest for a date partition in surrogate-1-training-pairs.
Usage:
  HF_TOKEN=hf_xxx python tools/snapshot_manifest.py \
    --repo axentx/surrogate-1-training-pairs \
    --partition 2026-04-29 \
    --out manifests/2026-04-29.manifest.json
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone
from typing import List, Dict

from huggingface_hub import HfApi

CDN_TEMPLATE = "https://huggingface.co/datasets/{repo}/resolve/main/{path}"


def build_manifest(repo: str, partition: str) -> Dict:
    """Single HF API call to list files under a date partition."""
    api = HfApi(token=os.getenv("HF_TOKEN"))
    prefix = f"batches/public-merged/{partition}"
    entries = api.list_repo_tree(repo=repo, path=prefix, recursive=True, repo_type="dataset")

    files = []
    for e in sorted(entries, key=lambda x: x.path):
        if e.type != "file":
            continue
        if not (e.path.endswith(".jsonl") or e.path.endswith(".parquet")):
            continue
        cdn_url = CDN_TEMPLATE.format(repo=repo, path=e.path)
        files.append(
            {
                "path": e.path,
                "cdn_url": cdn_url,
                "size": getattr(e, "size", None),
            }
        )

    manifest = {
        "repo": repo,
        "partition": partition,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "files": files,
    }
    return manifest


def main():
    parser = argparse.ArgumentParser(description="Generate CDN manifest for a partition.")
    parser.add_argument("--repo", default="axentx/surrogate-1-training-pairs")
    parser.add_argument("--partition", required=True, help="Date partition, e.g. 2026-04-29")
    parser.add_argument("--out", default=None, help="Output JSON path (default: stdout)")
    args = parser.parse_args()

    manifest = build_manifest(args.repo, args.partition)
    out = sys.stdout if args.out is None else open(args.out, "w", encoding="utf-8")
    json.dump(manifest, out, indent=2)
    if out is not sys.stdout:
        out.close()
        print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
```

### training/data_loader.py
```python
import json
from pathlib import Path

from datasets import load_dataset


def load_partition_from_manifest(manifest_path: str):
    """Load partition using CDN URLs from manifest (

## review — reviewer @ 2026-05-03T00:53:53.238888Z

APPROVE: implements the CDN bypass pattern with a single HF API call during manifest generation and zero HF API calls during training, which directly addresses 429 rate-limit failures; code is syntactically valid, uses real APIs, and provides a usable fallback path for dev.

Acceptance criteria:
- tools/snapshot_manifest.py runs with HF_TOKEN set and produces a deterministic file_manifest.json containing at least one CDN URL for .jsonl/.parquet files under the specified partition.
- training/data_loader.py loads the manifest and calls load_dataset with data_files pointing to CDN URLs; training proceeds without HF API calls (verify via network logs or HF API call count).
- training/train.py accepts --manifest and successfully loads records via load_partition_from_manifest, printing record count.
- README snippet includes the example command and notes that manifest generation requires HF_TOKEN while training does not.
- Fallback behavior is preserved: if manifest is missing, the training script can still invoke HF API (dev mode) without breaking existing workflows.

## security — axentx-security @ 2026-05-03T00:55:24.482083Z

{"verdict": "OK", "findings": [{"severity": "med", "class": "ssrf", "detail": "CDN URLs in the manifest may be attacker-controlled and could lead to SSRF when fetched by load_dataset during training.", "mitigation": "Validate and restrict CDN URLs to an allowlist of trusted domains and disable redirects or custom resolvers in the data loader."}, {"severity": "low", "class": "secret-leak", "detail": "HF_TOKEN used during manifest generation may be logged or persisted in debug artifacts or error traces.", "mitigation": "Mask HF_TOKEN in logs, use environment-only access, and scrub secrets from artifacts and exception messages."}, {"severity": "low", "class": "other", "detail": "Deterministic manifest generation could be abused to pin malicious CDN content if URL integrity is not verified.", "mitigation": "Pin expected file hashes or signatures and verify them before loading data from CDN URLs."}], "summary": "No high/critical issues; the change is acceptable with medium SSRF risk from CDN URLs and low risk of token leakage."}

## qa — security @ 2026-05-03T00:55:24.482108Z

{"verdict": "OK", "findings": [{"severity": "med", "class": "ssrf", "detail": "CDN URLs in the manifest may be attacker-controlled and could lead to SSRF when fetched by load_dataset during training.", "mitigation": "Validate and restrict CDN URLs to an allowlist of trusted domains and disable redirects or custom resolvers in the data loader."}, {"severity": "low", "class": "secret-leak", "detail": "HF_TOKEN used during manifest generation may be logged or persisted in debug artifacts or error traces.", "mitigation": "Mask HF_TOKEN in logs, use environment-only access, and scrub secrets from artifacts and exception messages."}, {"severity": "low", "class": "other", "detail": "Deterministic manifest generation could be abused to pin malicious CDN content if URL integrity is not verified.", "mitigation": "Pin expected file hashes or signatures and verify them before loading data from CDN URLs."}], "summary": "No high/critical issues; the change is acceptable with medium SSRF risk from CDN URLs and low risk of token leakage."}
