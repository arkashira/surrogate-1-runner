#!/usr/bin/env python3
"""
Stream parser: project raw parquet/jsonl bytes to {prompt,response}.
Reads file path from argv[1] or stdin, writes NDJSON to stdout.
Keeps memory low by processing line-by-line for jsonl or row-by-row for parquet.
"""
import json
import pyarrow.parquet as pq
import sys
from typing import Any, Dict

def normalize_record(rec: Dict[str, Any]) -> Dict[str, str]:
    # Heuristic projection; adapt to known schemas as needed.
    prompt = rec.get("prompt") or rec.get("input") or rec.get("question") or ""
    response = rec.get("response") or rec.get("output") or rec.get("answer") or ""
    return {"prompt": str(prompt), "response": str(response)}

def main() -> None:
    if len(sys.argv) > 1:
        path = sys.argv[1]
        if path.endswith(".parquet"):
            try:
                table = pq.read_table(path, columns=["prompt", "response"])
                for batch in table.to_batches(max_chunksize=8192):
                    prompts = batch.column("prompt").to_pylist()
                    responses = batch.column("response").to_pylist()
                    for p, r in zip(prompts, responses):
                        print(json.dumps({"prompt": str(p or ""), "response": str(r or "")}, ensure_ascii=False))
            except Exception as e:
                # fallback: try to read all and project
                table = pq.read_table(path)
                for col in table.column_names:
                    if "prompt" in col.lower() or "input" in col.lower():
                        pc = col
                    if "response" in col.lower() or "output" in col.lower():
                        rc = col
                for rec in table.to_pylist():
                    print(json.dumps(normalize_record(rec), ensure_ascii=False))
        else:
            # assume jsonl
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        rec = json.loads(line)
                    except Exception:
                        continue
                    print(json.dumps(normalize_record(rec), ensure_ascii=False))
    else:
        # stdin fallback (curl pipe)
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except Exception:
                continue
            print(json.dumps(normalize_record(rec), ensure_ascii=False))

if __name__ == "__main__":
    main()