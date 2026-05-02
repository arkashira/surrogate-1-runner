# axentx-dev-bot decision
- id: `20260502-130858-surrogate-1-discovery-b6d04a0f`
- project: surrogate-1
- focus: discovery
- created_at: 2026-05-02T13:08:58.755396Z

## dev — claude/llm-fallback-chain @ 2026-05-02T13:08:58.755478Z

## Final Synthesis (Best Parts + Correctness + Actionability)

I merged the strongest, non-redundant insights from both candidates and resolved contradictions in favor of correctness and immediate actionability.

### Key decisions
- **Keep Candidate 1’s discovery UI** (FastAPI + local JSON) because it gives immediate operator visibility without extra infra.
- **Adopt Candidate 2’s CDN-only training script** (`train_cdn.py`) because manifests are useless if training still hits the HF API and fails on schema heterogeneity.
- **Fix Candidate 1’s manifest generator**: use a single Python script (not Bash wrapper) and make date-scoped listing robust (handle both `date/` prefix folders and flat repos).
- **Fix Candidate 2’s manifest scope**: use non-recursive per-date listing to minimize API calls and avoid 429s.
- **Add deterministic schema projection** in the training script (select only `{prompt,response}` and coerce types) to prevent `pyarrow.CastError`.
- **Keep `.gitignore` and requirements** from Candidate 1; add `pyarrow` to training requirements.

---

### File-by-file final implementation

```bash
# /opt/axentx/surrogate-1/requirements-discovery.txt
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
huggingface-hub>=0.22.0
```

```bash
# /opt/axentx/surrogate-1/requirements-training.txt
huggingface-hub>=0.22.0
datasets>=2.18.0
pyarrow>=14.0.0
tqdm>=4.66.0
```

```bash
# /opt/axentx/surrogate-1/.gitignore
# generated manifests (do not commit)
manifests/
```

```python
# /opt/axentx/surrogate-1/scripts/build_manifest.py
#!/usr/bin/env python3
"""
Generate a date-scoped manifest for a HF dataset repo to avoid API 429 during training.
Usage:
  python build_manifest.py <repo> <date> [out_dir]
Example:
  python build_manifest.py axentx/surrogate-data 2026-04-29
"""
import json
import hashlib
import sys
from pathlib import Path
from huggingface_hub import list_repo_tree

def build_manifest(repo: str, date: str, out_dir: Path):
    # List top-level once (non-recursive) to minimize API calls
    top_items = list_repo_tree(repo=repo, path="", recursive=False)

    # Accept either date-as-folder (date/file.parquet) or flat repo with date prefix in filenames
    date_prefix = f"{date}/"
    date_folders = [it for it in top_items if it.type == "directory" and it.path.startswith(date_prefix)]

    files = []
    if date_folders:
        # Prefer date-scoped folders: list each folder non-recursively
        for folder in date_folders:
            for item in list_repo_tree(repo=repo, path=folder.path, recursive=False):
                if item.type == "file":
                    files.append(item)
    else:
        # Fallback: include only items whose names start with the date (e.g., 2026-04-29-*.parquet)
        for item in top_items:
            if item.type == "file" and item.path.startswith(date):
                files.append(item)

    entries = []
    for f in files:
        cdn_url = f"https://huggingface.co/datasets/{repo}/resolve/main/{f.path}"
        # Best-effort size; sha256 omitted (requires extra fetch). Manifest is for deterministic file list + CDN.
        entries.append({
            "path": f.path,
            "cdn_url": cdn_url,
            "size": getattr(f, "size", None),
        })

    manifest = {
        "repo": repo,
        "date": date,
        "generated_by": "build_manifest.py",
        "file_count": len(entries),
        "files": entries,
    }

    out_path = out_dir / repo / f"{date}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(manifest, indent=2))
    print(f"Wrote {len(entries)} files to {out_path}")
    return out_path

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    repo = sys.argv[1]
    date = sys.argv[2]
    out_dir = Path(sys.argv[3]) if len(sys.argv) > 3 else Path(__file__).parent.parent / "manifests"
    build_manifest(repo, date, out_dir)
```

```python
# /opt/axentx/surrogate-1/training/train_cdn.py


## review — reviewer @ 2026-05-02T13:17:32.664251Z

APPROVE: The change is a clear, workable step forward — it merges the strongest parts from both candidates, fixes manifest generation to be robust and CDN-only for training, adds deterministic schema projection to avoid pyarrow.CastError, and provides operator-facing discovery via FastAPI + local manifests. It reduces API 429 risk and removes HF API reliance during training while keeping infra minimal.

Acceptance criteria a downstream tester could check:
- `build_manifest.py` produces a valid JSON manifest for a given repo/date, listing files with `cdn_url` and `size`, and handles both date-scoped folders and flat date-prefixed filenames without recursive listing.
- `train_cdn.py` loads parquet files via CDN URLs from the manifest, projects to `{prompt,response}` with explicit string coercion, and completes at least one training epoch without pyarrow.CastError or HF API calls.
- The discovery UI (FastAPI) serves the generated manifests from `manifests/` and allows an operator to select repo/date and view file counts/URLs.
- `.gitignore` excludes `manifests/` and requirements files include `pyarrow` for training and `fastapi`, `uvicorn`, `huggingface-hub` for discovery.
- No HF dataset enumeration or authentication is required during training when using a pre-built manifest; all dataset access goes through CDN URLs.

## security — axentx-security @ 2026-05-02T13:17:41.992188Z

{"verdict": "OK", "findings": [{"severity": "med", "class": "ssrf", "detail": "CDN URLs from a manifest can be attacker-controlled and may trigger SSRF when fetched by training/discovery services.", "mitigation": "Restrict CDN fetches to an allowlist of domains and validate/normalize URLs before use; avoid following redirects to internal endpoints."}, {"severity": "low", "class": "other", "detail": "Operator-facing FastUI may expose manifest metadata (URLs, sizes, repo/date) that can aid reconnaissance.", "mitigation": "Require authentication/authorization on the discovery UI and rate-limit endpoints to prevent scraping."}, {"severity": "low", "class": "other", "detail": "Deterministic schema projection with string coercion could allow injection of malformed content into downstream training pipelines.", "mitigation": "Sanitize and validate prompt/response fields (length, encoding) before ingestion and log coercion events for audit."}], "summary": "No critical or high-severity issues; medium SSRF risk from CDN URL usage and low risks around information disclosure and data injection remain."}

## qa — security @ 2026-05-02T13:17:41.992226Z

{"verdict": "OK", "findings": [{"severity": "med", "class": "ssrf", "detail": "CDN URLs from a manifest can be attacker-controlled and may trigger SSRF when fetched by training/discovery services.", "mitigation": "Restrict CDN fetches to an allowlist of domains and validate/normalize URLs before use; avoid following redirects to internal endpoints."}, {"severity": "low", "class": "other", "detail": "Operator-facing FastUI may expose manifest metadata (URLs, sizes, repo/date) that can aid reconnaissance.", "mitigation": "Require authentication/authorization on the discovery UI and rate-limit endpoints to prevent scraping."}, {"severity": "low", "class": "other", "detail": "Deterministic schema projection with string coercion could allow injection of malformed content into downstream training pipelines.", "mitigation": "Sanitize and validate prompt/response fields (length, encoding) before ingestion and log coercion events for audit."}], "summary": "No critical or high-severity issues; medium SSRF risk from CDN URL usage and low risks around information disclosure and data injection remain."}
