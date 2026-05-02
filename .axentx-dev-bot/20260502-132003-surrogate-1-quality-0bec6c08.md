# axentx-dev-bot decision
- id: `20260502-132003-surrogate-1-quality-0bec6c08`
- project: surrogate-1
- focus: quality
- created_at: 2026-05-02T13:20:03.225480Z

## dev — claude/llm-fallback-chain @ 2026-05-02T13:20:03.225665Z

## Final Synthesis: CDN-Only Ingestion with Pre-Listed Manifests

**Highest-Value Fix (<2h):** Eliminate all Hugging Face API calls during parallel training by pre-listing files once on the orchestrator and fetching raw data via CDN (`resolve/main/...`). This removes rate limits (429), commit caps (128/hr), and auth bottlenecks while keeping schema logic intact.

---

## Concrete Implementation Plan (≤2h)

| Step | Owner | Time | Action |
|------|-------|------|--------|
| **1** | Orchestrator | 20m | Add `bin/list-date-folder.py` that uses `list_repo_tree(recursive=False)` per date folder → outputs `file-list-<date>.json`. Handles 429 with 360s backoff. |
| **2** | Workflow | 15m | Add `generate-file-list` job (runs once) → uploads artifact. Matrix jobs download artifact via `needs.generate-file-list.outputs.file-list`. |
| **3** | Enrich Script | 15m | Update `bin/dataset-enrich.sh` to accept `FILE_LIST` env var. If set, iterate over JSON list; skip `huggingface-cli api` calls entirely. |
| **4** | Fetcher | 20m | Add `lib/cdn_fetcher.py`: builds `https://huggingface.co/datasets/{repo}/resolve/main/{path}`, streams with retries, zero auth headers. |
| **5** | Training | 30m | Replace `load_dataset`/`streaming` with embedded file list + `cdn_fetcher`. Remove schema-dependent streaming to avoid heterogeneous parsing bugs. |
| **6** | Studio Guard | 10m | Wrap `Studio(create_ok=True)` with running-instance reuse check to prevent duplicate studios. |
| **7** | Cron Safeguard | 5m | Document `SHELL=/bin/bash` in README for GitHub Actions wrapper scripts. |

---

## Resolved Contradictions (Correctness + Actionability)

1. **Recursive vs Non-Recursive Listing**  
   Use **non-recursive per folder + one-level deeper** (Candidate 1). Fully recursive risks pagination explosion and 100× API calls. The hybrid approach bounds calls to `O(date_folders)` and stays under rate limits.

2. **Auth vs No-Auth CDN**  
   **Zero Authorization header** on CDN downloads (both candidates agree). Auth is unnecessary for public dataset files and consumes rate-limit quota.

3. **Streaming Dataset vs CDN Fetch**  
   **Drop `streaming=True`** in training when using heterogeneous schemas (Candidate 1). It introduces parsing fragility; CDN fetch + local buffering is deterministic and removes HF API dependency.

4. **Where Listing Happens**  
   **Orchestrator-only listing** (both candidates). Never in matrix jobs. Single source of truth prevents 16× duplicate listing and race conditions.

---

## Key Code Snippets (Integrated)

### `bin/list-date-folder.py`
```python
#!/usr/bin/env python3
import json, os, sys, time
from huggingface_hub import HfApi, login

def list_date_folder(repo_id: str, folder: str, token: str = None):
    if token:
        login(token=token, add_to_git_credential=False)
    api = HfApi()
    items = api.list_repo_tree(repo_id=repo_id, path=folder, recursive=False)
    files = []
    for item in items:
        if item.type == "file":
            files.append(f"{folder}/{item.path.split('/')[-1]}")
        elif item.type == "directory":
            subitems = api.list_repo_tree(repo_id=repo_id, path=item.path, recursive=False)
            for sub in subitems:
                if sub.type == "file":
                    files.append(f"{item.path}/{sub.path.split('/')[-1]}")
    return files

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: list-date-folder.py <repo> <date_folder> [--token TOKEN]")
        sys.exit(1)
    repo, folder = sys.argv[1], sys.argv[2]
    token = sys.argv[sys.argv.index("--token") + 1] if "--token" in sys.argv else None
    for attempt in range(3):
        try:
            files = list_date_folder(repo, folder, token)
            break
        except Exception as e:
            if "429" in str(e):
                print(f"Rate limited, waiting 360s...")
                time.sleep(360)
            else:
                raise
    else:
        sys.exit(1)
    out_name = f"file-list-{folde

## review — reviewer @ 2026-05-02T13:20:16.655894Z

APPROVE: Removes HF API dependency during parallel training, replaces it with CDN fetches and pre-listed manifests, and includes concrete retry/backoff and orchestrator-only listing — a clear, workable step toward reliability and rate-limit avoidance.

Acceptance criteria:
- Orchestrator can run `bin/list-date-folder.py` once per date folder and produce valid `file-list-<date>.json` (non-recursive + one-level deeper) with bounded API calls.
- Workflow uploads the file-list artifact and matrix jobs consume it via `needs.generate-file-list.outputs.file-list` (or equivalent download) without re-listing.
- `bin/dataset-enrich.sh` accepts `FILE_LIST` and iterates over the JSON list without invoking `huggingface-cli api` or `list_repo_tree` per file.
- `lib/cdn_fetcher.py` builds correct CDN URLs (`resolve/main/{path}`), streams with retries/timeouts, and never sends auth headers for public datasets.
- Training path uses the file list + CDN fetches instead of `load_dataset(..., streaming=True)` for heterogeneous schemas, and Studio reuse logic prevents duplicate studios.

## security — axentx-security @ 2026-05-02T13:20:22.442883Z

{"verdict": "OK", "findings": [{"severity": "med", "class": "ssrf", "detail": "CDN fetcher may follow redirects to internal endpoints or attacker-controlled hosts if URL resolution and destination validation are not strict.", "mitigation": "Pin CDN hostnames, disable cross-origin redirects, and validate final URL against an allowlist before streaming."}, {"severity": "low", "class": "other", "detail": "Orchestrator-generated file-list JSON could be tampered with in transit or at rest, causing the pipeline to fetch malicious or unintended objects.", "mitigation": "Sign or hash the file-list artifact and verify integrity in matrix jobs prior to consumption."}, {"severity": "low", "class": "other", "detail": "Retry/backoff without jitter and unbounded concurrency could amplify traffic to the CDN or cause noisy neighbor effects.", "mitigation": "Add jitter to backoff, cap concurrency, and enforce per-job rate limits."}], "summary": "Removes HF API dependency and auth exposure; medium SSRF risk from CDN redirect handling and low integrity/abuse risks remain."}

## qa — security @ 2026-05-02T13:20:22.442942Z

{"verdict": "OK", "findings": [{"severity": "med", "class": "ssrf", "detail": "CDN fetcher may follow redirects to internal endpoints or attacker-controlled hosts if URL resolution and destination validation are not strict.", "mitigation": "Pin CDN hostnames, disable cross-origin redirects, and validate final URL against an allowlist before streaming."}, {"severity": "low", "class": "other", "detail": "Orchestrator-generated file-list JSON could be tampered with in transit or at rest, causing the pipeline to fetch malicious or unintended objects.", "mitigation": "Sign or hash the file-list artifact and verify integrity in matrix jobs prior to consumption."}, {"severity": "low", "class": "other", "detail": "Retry/backoff without jitter and unbounded concurrency could amplify traffic to the CDN or cause noisy neighbor effects.", "mitigation": "Add jitter to backoff, cap concurrency, and enforce per-job rate limits."}], "summary": "Removes HF API dependency and auth exposure; medium SSRF risk from CDN redirect handling and low integrity/abuse risks remain."}
