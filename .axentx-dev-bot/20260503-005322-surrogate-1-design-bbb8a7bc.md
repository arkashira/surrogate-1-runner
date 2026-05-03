# axentx-dev-bot decision
- id: `20260503-005322-surrogate-1-design-bbb8a7bc`
- project: surrogate-1
- focus: design
- created_at: 2026-05-03T00:53:22.198258Z

## dev — claude/llm-fallback-chain @ 2026-05-03T00:53:22.198341Z

Based on the provided AI proposals, I will synthesize the best parts and combine the strongest insights into a single final answer. The goal is to resolve contradictions in favor of correctness and concrete actionability.

**Final Answer:**

To implement the **HF CDN bypass** pattern and eliminate rate-limit/429 risk during long training runs, follow these steps:

1. **Create `tools/snapshot_manifest.py`**:
	* Make a single `list_repo_tree` API call for one date folder.
	* Build a manifest with CDN URLs, integrity metadata, and save it to `manifests/{date}_file_manifest.json`.
	* Include retry/backoff for 429 with a 360s wait.
2. **Update `train.py`**:
	* Accept a `--manifest` argument pointing to `file_manifest.json`.
	* Use `requests.get(cdn_url, stream=True)` with no Authorization header.
	* Parse parquet in-memory and project to `{prompt, response}` only.
	* Remove any `load_dataset(streaming=True)` usage for heterogeneous schemas.
	* Add deterministic shard selection via `slug-hash % N` if needed.
3. **Add `requirements-dev.txt` entry**:
	* Include `requests`, `pyarrow`, and `tqdm` (already in requirements).
4. **Smoke test on Mac**:
	* Run `python tools/snapshot_manifest.py --date 2026-04-29 --repo axentx/surrogate-1-training-pairs`.
	* Verify the manifest contains CDN URLs.
	* Run `python train.py --manifest manifests/2026-04-29_file_manifest.json --limit 100` and confirm data loads without HF API calls.
5. **Lightning Studio integration**:
	* Embed the manifest path in Lightning `run()` args.
	* Reuse the running Studio: check `Teamspace.studios` before `Studio(create_ok=True)`.
	* On idle stop, restart with `target.start(machine=Machine.L40S)`.

**Code Snippets:**

The provided code snippets for `tools/snapshot_manifest.py` and `train.py` are well-structured and effective. The `tools/snapshot_manifest.py` script lists one date-partition of a Hugging Face dataset and emits a CDN-only manifest. The `train.py` script consumes the manifest and loads data from the CDN without making HF API calls.

**Benefits:**

The proposed solution offers several benefits, including:

* Avoids HF API 429 during ingestion/training (CDN-only fetches)
* Avoids `load_dataset(streaming=True)` on repos with heterogeneous schemas (PyArrow CastError)
* Enables deterministic shard selection via `slug-hash % 16` without listing all files repeatedly
* Fits the existing `batches/public-merged/<date>/shard` structure

By following these steps and using the provided code snippets, you can effectively implement the **HF CDN bypass** pattern and eliminate rate-limit/429 risk during long training runs.

## review — reviewer @ 2026-05-03T00:53:54.175259Z

APPROVE: Proposes a concrete, incremental path to eliminate HF API 429s via CDN-only fetches; manifest-based ingestion is a workable pattern and the code snippets align with the existing structure.

Acceptance criteria:
- `tools/snapshot_manifest.py` lists one date-partition via `list_repo_tree`, emits `manifests/{date}_file_manifest.json` with CDN URLs and integrity metadata, and retries on 429 with exponential backoff (cap ~360s).
- `train.py` accepts `--manifest`, streams files via `requests.get(cdn_url, stream=True)` without Authorization, projects parquet to `{prompt, response}`, and avoids `load_dataset(streaming=True)` for heterogeneous schemas.
- `requirements-dev.txt` includes `requests`, `pyarrow`, and `tqdm` (or confirms they are already present).
- Smoke test on Mac: manifest creation for `2026-04-29` succeeds and contains CDN URLs; `train.py --manifest ... --limit 100` loads data without HF API calls (verify via logs or traffic capture).
- Lightning Studio integration reuses an existing Studio when available and embeds the manifest path in run args; idle-stop/start with `Machine.L40S` is documented and functional.

## security — axentx-security @ 2026-05-03T00:55:41.087582Z

{"verdict": "OK", "findings": [{"severity": "med", "class": "ssrf", "detail": "train.py streams arbitrary CDN URLs from an untrusted manifest without allow-list validation, enabling SSRF against internal endpoints.", "mitigation": "Validate/allow-list CDN hostnames and enforce network egress controls before fetching."}, {"severity": "low", "class": "other", "detail": "Integrity metadata in the manifest is not verified before processing, risking tampering or supply-chain substitution.", "mitigation": "Verify hashes/signatures of each file against the manifest prior to ingestion."}, {"severity": "low", "class": "other", "detail": "Exponential backoff retry logic could be abused to prolong resource consumption or mask availability issues.", "mitigation": "Bound total retries and add jitter; monitor and alert on sustained 429s."}], "summary": "No high/crit issues; proceed with SSRF controls and integrity verification to reduce residual risk."}

## qa — security @ 2026-05-03T00:55:41.087614Z

{"verdict": "OK", "findings": [{"severity": "med", "class": "ssrf", "detail": "train.py streams arbitrary CDN URLs from an untrusted manifest without allow-list validation, enabling SSRF against internal endpoints.", "mitigation": "Validate/allow-list CDN hostnames and enforce network egress controls before fetching."}, {"severity": "low", "class": "other", "detail": "Integrity metadata in the manifest is not verified before processing, risking tampering or supply-chain substitution.", "mitigation": "Verify hashes/signatures of each file against the manifest prior to ingestion."}, {"severity": "low", "class": "other", "detail": "Exponential backoff retry logic could be abused to prolong resource consumption or mask availability issues.", "mitigation": "Bound total retries and add jitter; monitor and alert on sustained 429s."}], "summary": "No high/crit issues; proceed with SSRF controls and integrity verification to reduce residual risk."}
