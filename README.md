# surrogate-1-runner

Parallel public-dataset ingest workers for the
[axentx/surrogate-1-training-pairs](https://huggingface.co/datasets/axentx/surrogate-1-training-pairs)
HuggingFace dataset.

## What this does

Every 30 minutes (or on `workflow_dispatch`), GitHub Actions launches **16 parallel runners**.
Each runner takes a deterministic 1/16 slice (`slug-hash bucket = SHARD_ID`)
of the public dataset list defined in `bin/dataset-enrich.sh`, streams,
normalizes per-schema, dedups via the central md5 hash store, and uploads
its output to a unique path on the dataset repo:

## Authentication

All API endpoints exposed by **surrogate-1** require an API key for access.

- **Header**: Include `X-API-Key: <your-api-key>` in every HTTP request.
- **Missing or invalid key**: The service responds with **401 Unauthorized**.
- **Health‑check endpoint**: `GET /health` returns **200 OK** when a valid API key is supplied.
- **Rate limiting**: Each API key is limited to **100 requests per minute**. Exceeding this limit results in a **429 Too Many Requests** response.

### Example request