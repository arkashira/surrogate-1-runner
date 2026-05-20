"""
A lightweight HTTP server that generates synthetic Datadog data on demand.

Features
--------
- Accepts CLI arguments for data type, volume, output format, and mode.
- Supports two modes:
    * `batch`  – returns a single response containing all synthetic records.
    * `realtime` – streams records one by one using Server‑Sent Events (SSE).
- Exposes a `/data` endpoint that streams or returns the data.
- Uses FastAPI for the web framework and uvicorn for the ASGI server.

Usage
-----
    python datadog_server.py \
        --data-type metric \
        --volume 100 \
        --format json \
        --mode realtime \
        --host 0.0.0.0 \
        --port 8000

The server will listen on the specified host/port and expose the `/data` endpoint.
"""

import argparse
import asyncio
import json
import random
import string
import time
from datetime import datetime
from typing import AsyncGenerator, Dict, Iterable, List

import uvicorn
from fastapi import FastAPI, Response, Request
from fastapi.responses import StreamingResponse, JSONResponse

app = FastAPI(title="Synthetic Datadog Data Server")

# --------------------------------------------------------------------------- #
# Synthetic data generators
# --------------------------------------------------------------------------- #
def _random_string(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=length))


def generate_metric_record() -> Dict:
    """Generate a single synthetic metric record."""
    return {
        "metric": f"synthetic.metric.{_random_string()}",
        "points": [(int(time.time()), random.uniform(0, 100))],
        "tags": [f"env:{_random_string(4)}", f"region:{_random_string(2)}"],
        "type": "gauge",
    }


def generate_log_record() -> Dict:
    """Generate a single synthetic log record."""
    return {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "service": f"synthetic-service-{_random_string(3)}",
        "status": random.choice(["info", "warning", "error"]),
        "message": f"Log message {_random_string(10)}",
        "attributes": {"key1": _random_string(5), "key2": _random_string(5)},
    }


def get_generator(data_type: str, volume: int) -> Iterable[Dict]:
    """Return an iterable that yields synthetic records."""
    if data_type == "metric":
        gen_func = generate_metric_record
    elif data_type == "log":
        gen_func = generate_log_record
    else:
        raise ValueError(f"Unsupported data_type: {data_type}")

    for _ in range(volume):
        yield gen_func()


# --------------------------------------------------------------------------- #
# FastAPI endpoints
# --------------------------------------------------------------------------- #
@app.get("/data")
async def data_endpoint(
    request: Request,
    data_type: str = "metric",
    volume: int = 10,
    fmt: str = "json",
    mode: str = "batch",
) -> Response:
    """
    Endpoint to serve synthetic Datadog data.

    Parameters
    ----------
    data_type : str
        Type of data to generate: 'metric' or 'log'.
    volume : int
        Number of records to generate.
    fmt : str
        Output format: 'json' or 'csv'.
    mode : str
        'batch' returns all data at once; 'realtime' streams via SSE.
    """
    if mode == "batch":
        records = list(get_generator(data_type, volume))
        if fmt == "json":
            return JSONResponse(content=records)
        elif fmt == "csv":
            # Simple CSV conversion
            if not records:
                return Response(content="", media_type="text/csv")
            headers = records[0].keys()
            lines = [",".join(headers)]
            for rec in records:
                lines.append(",".join(str(rec[h]) for h in headers))
            csv_text = "\n".join(lines)
            return Response(content=csv_text, media_type="text/csv")
        else:
            raise ValueError(f"Unsupported format: {fmt}")

    elif mode == "realtime":
        async def event_generator() -> AsyncGenerator[str, None]:
            for rec in get_generator(data_type, volume):
                # SSE format: data: <payload>\n\n
                payload = json.dumps(rec)
                yield f"data: {payload}\n\n"
                await asyncio.sleep(0.1)  # simulate delay

        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache"},
        )
    else:
        raise ValueError(f"Unsupported mode: {mode}")


# --------------------------------------------------------------------------- #
# CLI entry point
# --------------------------------------------------------------------------- #
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the synthetic Datadog data server.")
    parser.add_argument("--data-type", type=str, default="metric", choices=["metric", "log"])
    parser.add_argument("--volume", type=int, default=10)
    parser.add_argument("--format", type=str, default="json", choices=["json", "csv"])
    parser.add_argument("--mode", type=str, default="batch", choices=["batch", "realtime"])
    parser.add_argument("--host", type=str, default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    uvicorn.run(
        "datadog_server:app",
        host=args.host,
        port=args.port,
        log_level="info",
        reload=False,
    )


if __name__ == "__main__":
    main()