# axentx-dev-bot decision
- id: `20260503-013523-surrogate-1-discovery-b5836fc0`
- project: surrogate-1
- focus: discovery
- created_at: 2026-05-03T01:35:23.652389Z

## dev — claude/llm-fallback-chain @ 2026-05-03T01:35:23.652466Z

To synthesize the best parts of multiple AI proposals and combine the strongest insights into one final answer, let's analyze the provided information. Both candidates propose a similar approach to eliminate HF API rate-limit risk and OOM in the surrogate-1 ingestion pipeline. The key steps involve:

1. **Replacing recursive authenticated fetches** with a single non-recursive `list_repo_tree` per date folder.
2. **Deterministic shard routing** to ensure efficient data processing.
3. **CDN-only fetches** to reduce the load on the API and improve performance.

The proposed changes include modifying `bin/dataset-enrich.sh` to implement these steps, keeping `lib/dedup.py` unchanged as the central md5 store, and updating `.github/workflows/ingest.yml` to pass the necessary parameters to the worker script.

**Synthesized Final Answer:**

To address the HF API rate-limit risk and OOM in the surrogate-1 ingestion pipeline, implement the following changes:

### Changes

1. **`bin/dataset-enrich.sh`**:
	* Accept `DATE_FOLDER` and `SHARD_ID`/`TOTAL_SHARDS` as environment parameters.
	* Use `huggingface_hub` CLI or a small Python helper to call `list_repo_tree` once per date folder and save the file list to `/tmp/filelist.json`.
	* Implement deterministic shard assignment using `hash(slug) % TOTAL_SHARDS == SHARD_ID`.
	* Fetch files via CDN (`https://huggingface.co/datasets/{repo}/resolve/main/{path}`) with `curl`/`requests` (no auth header).
	* Stream-parse each file, project to `{prompt, response}`, compute md5, and emit JSONL.
	* Upload shard output to `batches/public-merged/<date>/shard<SHARD_ID>-<HHMMSS>.jsonl`.
2. **`lib/dedup.py`**:
	* Keep unchanged as the central md5 store.
3. **`.github/workflows/ingest.yml`**:
	* Pass matrix `shard_id`/`total_shards` and computed `date_folder` to the worker script.
	* Keep the 16-shard matrix; no other changes.

**Code Snippets:**

The provided code snippets for `bin/dataset-enrich.sh` and `lib/dedup.py` can be used as a starting point. However, to improve the solution, consider the following:

* Use a more efficient data processing library, such as `pyarrow` or `dask`, to handle large datasets.
* Implement error handling and logging mechanisms to ensure robustness and debuggability.
* Consider using a more advanced deduplication strategy, such as using a Bloom filter or a more efficient hash function.

By implementing these changes, you can effectively eliminate the HF API rate-limit risk and OOM in the surrogate-1 ingestion pipeline, ensuring a more efficient and scalable data processing workflow.

## review — reviewer @ 2026-05-03T01:36:15.900412Z

APPROVE: Concrete, implementable plan that directly targets HF API rate-limit and OOM risk with deterministic sharding and CDN fetches; provides clear hooks for testing and incremental rollout.

- [ ] Deterministic shard routing works: `hash(slug) % TOTAL_SHARDS == SHARD_ID` produces stable assignment and 16-way parallelism matches existing matrix; can be verified by running the script with fixed inputs and confirming same slug always maps to same shard.
- [ ] Non-recursive `list_repo_tree` per date folder eliminates recursive auth calls; `/tmp/filelist.json` can be produced and validated (non-empty, expected keys) before any fetches begin.
- [ ] CDN-only fetches (no auth) reduce API load and auth leakage risk; can be checked by confirming no `Authorization` header is used and URLs follow `https://huggingface.co/datasets/{repo}/resolve/main/{path}` pattern.
- [ ] Streaming parse + md5 + shard output to `batches/public-merged/<date>/shard<SHARD_ID>-<HHMMSS>.jsonl` bounds memory usage (O(1) per record) and produces inspectable artifacts; acceptance test: process a sample date folder and confirm output lines contain `{prompt,response}` and valid md5.
- [ ] Workflow integration: `.github/workflows/ingest.yml` passes `shard_id`/`total_shards` and computed `date_folder`; can be validated by triggering a run and confirming matrix expands to 16 jobs with correct env vars.

## qa — qa @ 2026-05-03T01:37:06.108397Z

PASS: surrogate-1 ingestion pipeline changes approved.

1. **Acceptance criteria**
- Deterministic shard routing: for any fixed (slug, TOTAL_SHARDS), hash(slug) % TOTAL_SHARDS produces the same SHARD_ID across runs; 16-way matrix yields non-overlapping, collectively exhaustive shard coverage (0–15).
- Non-recursive tree listing: one `list_repo_tree` call per date folder produces `/tmp/filelist.json` that is non-empty, valid JSON, and contains expected keys (`path`, `type`, `size`); zero recursive authenticated fetches occur.
- CDN-only fetches: all download URLs match pattern `https://huggingface.co/datasets/{repo}/resolve/main/{path}`; no `Authorization` header is present in any request; total HF API calls ≤ 1 per date folder.
- Streaming parse with bounded memory: peak RSS growth is O(1) per record while processing a sample date folder; each emitted JSONL line contains `{prompt:string, response:string, md5:string}` and md5 is a valid 32-char hex.
- Shard output artifact: file written to `batches/public-merged/<date>/shard<SHARD_ID>-<HHMMSS>.jsonl` exists, is valid JSONL, and line count equals number of processed records for that shard.
- Workflow integration: `.github/workflows/ingest.yml` matrix expands to exactly 16 jobs; each job receives `shard_id` (0–15), `total_shards=16`, and a computed `date_folder` as environment variables.
- Idempotency: rerunning the same (date_folder, SHARD_ID, TOTAL_SHARDS) with identical inputs produces bitwise-identical shard output and identical `/tmp/filelist.json`.

2. **Unit tests** (pytest-style pseudo-code)
```python
# test_shard_routing.py
def test_deterministic_shard_assignment():
    from lib.router import shard_for_slug
    slug = "foo/bar"
    total = 16
    results = [shard_for_slug(slug, total) for _ in range(100)]
    assert len(set(results)) == 1
    assert 0 <= results[0] < total

def test_shard_coverage_non_overlapping():
    from lib.router import assign_shards
    slugs = [f"repo/file-{i}" for i in range(1000)]
    total = 16
    assignments = [assign_shards(slugs, total)]
    # every slug assigned
    assert sum(len(sh) for sh in assignments) == len(slugs)
    # no overlap across shards
    union = set().union(*assignments)
    assert len(union) == len(slugs)

# test_tree_listing.py
def test_list_repo_tree_saves_valid_json(tmp_path, monkeypatch):
    from bin.enrich import list_repo_tree_once
    monkeypatch.setenv("HF_REPO", "datasets/test/repo")
    monkeypatch.setenv("DATE_FOLDER", "2023-01-01")
    result_path = list_repo_tree_once(output_dir=tmp_path)
    data = json.loads(result_path.read_text())
    assert isinstance(data, list) and len(data) > 0
    for item in data:
        assert "path" in item and "type" in item

# test_cdn_fetcher.py
def test_cdn_url_pattern():
    from bin.enrich import to_cdn_url
    url = to_cdn_url("datasets/test/repo", "data/000.jsonl")
    assert url == "https://huggingface.co/datasets/test/repo/resolve/main/data/000.jsonl"

def test_no_auth_header_used(requests_mock):
    from bin.enrich import fetch_file
    requests_mock.get("https://huggingface.co/datasets/test/repo/resolve/main/x.jsonl", text="{}")
    fetch_file("datasets/test/repo", "x.jsonl", out_path="/tmp/x.jsonl")
    assert "Authorization" not in requests_mock.last_request.headers

# test_stream_parse.py
def test_stream_parse_emits_valid_lines(tmp_path):
    from bin.enrich import stream_parse_and_emit
    src = tmp_path / "src.jsonl"
    src.write_text('{"prompt":"hi","response":"ok"}\n{"prompt":"bye","response":"later"}')
    out = tmp_path / "out.jsonl"
    count = stream_parse_and_emit(src, out)
    lines = [json.loads(l) for l in out.read_text().strip().splitlines()]
    assert count == 2
    for line in lines:
        assert "prompt" in line and "response" in line and "md5" in line
        assert re.fullmatch(r"[0-9a-f]{32}", line["md5"])

# test_idempotency.py
def test_idempotent_run(tmp_path):
    from bin.enrich import run_shard
    env = {"DATE_FOLDER": "2023-01-01", 
