# axentx-dev-bot decision
- id: `20260503-004412-surrogate-1-discovery-246bb5d7`
- project: surrogate-1
- focus: discovery
- created_at: 2026-05-03T00:44:12.248470Z

## dev — claude/llm-fallback-chain @ 2026-05-03T00:44:12.248546Z

To synthesize the best parts of multiple AI proposals and combine the strongest insights into one final answer, let's analyze the provided information and resolve any contradictions in favor of correctness and concrete actionability.

### Overview of the Proposals

Both proposals suggest implementing a Mac-side tool, `tools/snapshot_manifest.py`, which lists one date-partition via a single Hugging Face (HF) API call. This tool emits a `file_manifest.json` containing CDN URLs and is accompanied by a training script that utilizes CDN-only fetches. The primary goal is to apply the HF CDN bypass pattern, avoiding 429/rate-limit errors during training while keeping data ingestion simple.

### Key Components and Steps

1. **Create `tools/snapshot_manifest.py`**: This script performs a single `list_repo_tree` call for a specified date folder (e.g., `batches/public-merged/2026-05-03`), generates a `file_manifest.json` with CDN URLs, and includes deterministic ordering for consistency across Lightning workers.

2. **Develop `tools/train_cdn_loader.py`**: This script reads the `file_manifest.json`, builds an `IterableDataset` that downloads data via CDN URLs using `requests`/`urllib` and `pyarrow`, projects only `{prompt, response}` at parse time, and implements retry/backoff on CDN failures.

3. **Update README**: Include instructions for creating a CDN manifest and using it for training in Lightning Studio, emphasizing the avoidance of HF API calls and quota churn.

4. **Smoke Test**: Perform a test run against a small date folder to verify manifest correctness and the loader's ability to stream and project rows without HF API authentication.

### Synthesized Final Answer

The most effective approach involves:

- **Implementing `tools/snapshot_manifest.py`** to generate a `file_manifest.json` with CDN URLs for a specified date partition. This step ensures that only one HF API call is made, reducing the risk of rate limiting.

- **Developing `tools/train_cdn_loader.py`** to facilitate CDN-only data loading. This script should handle different file types (parquet, jsonl), project relevant fields (`prompt`, `response`), and include a retry mechanism for CDN failures.

- **Updating the README** to provide clear instructions on using the `snapshot_manifest.py` tool and integrating the `train_cdn_loader.py` script into the training process in Lightning Studio. This documentation should highlight the benefits of this approach, including the avoidance of HF API rate limits and simplified data ingestion.

- **Conducting a thorough smoke test** to validate the functionality of both scripts and ensure that the generated manifest is correct and usable for training without encountering HF API authentication issues.

By following this synthesized approach, you can effectively bypass HF API rate limits during training, streamline your data loading process, and ensure a more reliable and efficient training workflow. 

Here is a code snippet that combines the key elements:
```python
# tools/snapshot_manifest.py
import argparse
import json
from huggingface_hub import HfApi

def list_date_partition(date_folder, token):
    api = HfApi(token=token)
    entries = api.list_repo_tree(repo_id="axentx/surrogate-1-training-pairs", path=date_folder, recursive=False)
    files = []
    for entry in entries:
        if entry.type != "file":
            continue
        path = entry.path
        files.append({
            "path": path,
            "cdn_url": f"https://huggingface.co/datasets/axentx/surrogate-1-training-pairs/resolve/main/{path}",
            "size": getattr(entry, "size", None),
        })
    files.sort(key=lambda f: f["path"])
    return files

def main():
    parser = argparse.ArgumentParser(description="Create CDN manifest for a date partition.")
    parser.add_argument("--date", required=True, help="Date folder, e.g., batches/public-merged/2026-05-03")
    parser.add_argument("--out", default="file_manifest.json", help="Output JSON path")
   

## review — reviewer @ 2026-05-03T00:44:18.506810Z

APPROVE: This is a workable first step that establishes a clear, testable pattern for CDN-only training data ingestion and rate-limit avoidance. The proposal identifies concrete artifacts (snapshot_manifest.py, train_cdn_loader.py, README updates, smoke test) and acceptance criteria a downstream tester can validate.

Acceptance criteria:
- tools/snapshot_manifest.py accepts --date and --out, performs a single list_repo_tree call for the specified HF path, emits file_manifest.json with deterministic ordering and CDN URLs, and exits non-zero on API/auth errors.
- tools/train_cdn_loader.py (or equivalent stub) can read file_manifest.json, resolve at least one CDN URL to bytes, parse parquet/jsonl, project {prompt, response}, and include retry/backoff for transient CDN failures.
- README includes a “Create CDN manifest” section with example commands and a “Training with CDN manifest” section referencing Lightning Studio usage and noting HF API avoidance.
- Smoke test against a small date folder (e.g., batches/public-merged/YYYY-MM-DD) produces a valid file_manifest.json and demonstrates at least one row streamed without HF API authentication.

## perf — axentx-perf @ 2026-05-03T00:44:28.340206Z

{"verdict": "OK", "findings": [{"severity": "med", "class": "unbounded-query", "detail": "snapshot_manifest.py uses a single list_repo_tree call; if the target folder contains many files or deep trees, the response size and client-side processing (ordering, filtering) could become large and block ingestion startup.", "mitigation": "Paginate or cap tree depth; stream and sort incrementally; add --max-files and warn/trim if exceeded."}, {"severity": "low", "class": "memory-leak", "detail": "train_cdn_loader.py may buffer full parquet/jsonl rows or large CDN responses in memory when projecting {prompt, response}, risking OOM on wide rows or large batches.", "mitigation": "Stream rows (e.g., pyarrow.parquet.ParquetFile.iter_batches), bound batch sizes, and release buffers promptly."}], "summary": "The change establishes a CDN-first ingestion path that avoids HF API auth/rate limits and is testable. Performance risks are limited to potential unbounded tree listings and in-memory buffering during row projection; neither is a prod-outage risk at reasonable scale, so verdict is OK."}

## qa — perf @ 2026-05-03T00:44:28.340233Z

{"verdict": "OK", "findings": [{"severity": "med", "class": "unbounded-query", "detail": "snapshot_manifest.py uses a single list_repo_tree call; if the target folder contains many files or deep trees, the response size and client-side processing (ordering, filtering) could become large and block ingestion startup.", "mitigation": "Paginate or cap tree depth; stream and sort incrementally; add --max-files and warn/trim if exceeded."}, {"severity": "low", "class": "memory-leak", "detail": "train_cdn_loader.py may buffer full parquet/jsonl rows or large CDN responses in memory when projecting {prompt, response}, risking OOM on wide rows or large batches.", "mitigation": "Stream rows (e.g., pyarrow.parquet.ParquetFile.iter_batches), bound batch sizes, and release buffers promptly."}], "summary": "The change establishes a CDN-first ingestion path that avoids HF API auth/rate limits and is testable. Performance risks are limited to potential unbounded tree listings and in-memory buffering during row projection; neither is a prod-outage risk at reasonable scale, so verdict is OK."}
