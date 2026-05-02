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

## review — reviewer @ 2026-05-02T13:20:38.190115Z

APPROVE: Removes rate-limit/auth bottlenecks by replacing HF API calls with CDN fetches and centralized pre-listing; provides a clear, incremental path that a downstream tester can validate end-to-end.

Acceptance criteria:
- Orchestrator job produces `file-list-<date>.json` with non-recursive + one-level-deeper listing and 429 backoff (360s) without leaking tokens.
- Matrix jobs consume the artifact and run `dataset-enrich.sh` with `FILE_LIST` set, making zero `huggingface-cli api` calls during enrichment.
- `lib/cdn_fetcher.py` builds valid `https://huggingface.co/datasets/{repo}/resolve/main/{path}` URLs, streams with retries, and omits Authorization headers for public datasets.
- Training pipeline uses the file list + CDN fetcher instead of `load_dataset(..., streaming=True)` and completes a full epoch on a sample date folder without HF API errors.
- Studio guard prevents duplicate studio creation and cron wrapper scripts declare `SHELL=/bin/bash` in README/action YAML.

## perf — axentx-perf @ 2026-05-02T13:20:52.440514Z

{"verdict": "OK", "findings": [{"severity": "med", "class": "unbounded-query", "detail": "Non-recursive + one-level-deeper listing may still explode for repos with many top-level directories or huge flat namespaces; unbounded growth in file-list-<date>..json could stress orchestrator memory and downstream matrix fan-out.", "mitigation": "Cap entries per listing (e.g., 10k) and paginate; stream JSON lines instead of a single monolithic artifact; enforce size limits on matrix job inputs."}, {"severity": "low", "class": "memory-leak", "detail": "429 backoff of 360s without jitter risks thundering-herd retries across matrix jobs if many runners wake simultaneously after cooldown.", "mitigation": "Add exponential backoff with jitter; stagger matrix job retries via queue or random delay offset."}, {"severity": "low", "class": "other", "detail": "Omitting Authorization headers is correct for public datasets, but CDN fetcher must validate response integrity (e.g., ETag/sha256) to avoid silent corruption that would waste training compute.", "mitigation": "Verify checksums when available; fallback to HF API only for integrity metadata if CDN lacks it."}], "summary": "Eliminating HF API calls and switching to CDN fetches + pre-listing removes the primary rate-limit/auth bottleneck and should scale well. Watch for unbounded file-list growth and retry storms; otherwise, performance impact is positive and safe to proceed."}

## qa — perf @ 2026-05-02T13:20:52.440579Z

{"verdict": "OK", "findings": [{"severity": "med", "class": "unbounded-query", "detail": "Non-recursive + one-level-deeper listing may still explode for repos with many top-level directories or huge flat namespaces; unbounded growth in file-list-<date>..json could stress orchestrator memory and downstream matrix fan-out.", "mitigation": "Cap entries per listing (e.g., 10k) and paginate; stream JSON lines instead of a single monolithic artifact; enforce size limits on matrix job inputs."}, {"severity": "low", "class": "memory-leak", "detail": "429 backoff of 360s without jitter risks thundering-herd retries across matrix jobs if many runners wake simultaneously after cooldown.", "mitigation": "Add exponential backoff with jitter; stagger matrix job retries via queue or random delay offset."}, {"severity": "low", "class": "other", "detail": "Omitting Authorization headers is correct for public datasets, but CDN fetcher must validate response integrity (e.g., ETag/sha256) to avoid silent corruption that would waste training compute.", "mitigation": "Verify checksums when available; fallback to HF API only for integrity metadata if CDN lacks it."}], "summary": "Eliminating HF API calls and switching to CDN fetches + pre-listing removes the primary rate-limit/auth bottleneck and should scale well. Watch for unbounded file-list growth and retry storms; otherwise, performance impact is positive and safe to proceed."}
