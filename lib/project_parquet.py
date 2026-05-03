import pyarrow.parquet as pq
import pyarrow as pa
import io
import hashlib
import json

CANDIDATE_PROMPT = {"prompt", "instruction", "input", "question"}
CANDIDATE_RESPONSE = {"response", "output", "answer", "completion"}

def normalize_record(rec: dict) -> dict | None:
    # Best-effort pick prompt/response
    prompt_keys = [k for k in rec if k in CANDIDATE_PROMPT]
    response_keys = [k for k in rec if k in CANDIDATE_RESPONSE]

    prompt = rec[prompt_keys[0]] if prompt_keys else rec.get("prompt", "")
    response = rec[response_keys[0]] if response_keys else rec.get("response", "")

    if not prompt or not response:
        return None
    return {"prompt": str(prompt).strip(), "response": str(response).strip()}

def project_parquet_bytes(data: bytes):
    table = pq.read_table(io.BytesIO(data))
    for batch in table.to_batches():
        cols = batch.columns
        col_map = {name: batch.schema.get_field_index(name) for name in table.column_names if name in table.column_names}
        n = batch.num_rows
        for i in range(n):
            rec = {}
            for name, idx in col_map.items():
                try:
                    val = cols[idx][i].as_py()
                    rec[name] = val
                except Exception:
                    rec[name] = None
            nr = normalize_record(rec)
            if nr:
                nr["_hash"] = hashlib.md5(json.dumps(nr, sort_keys=True).encode()).hexdigest()
                yield nr