"""FastAPI service that exposes a health endpoint and Prometheus metrics."""
import time
import threading
from fastapi import FastAPI, Response
from prometheus_client import start_http_server, CONTENT_TYPE_LATEST, generate_latest
from .metrics import record_workflow, WORKFLOW_LATENCY

app = FastAPI()


@app.get("/healthz")
def healthz() -> dict:
    """Simple health check used by Docker/CI."""
    return {"status": "ok"}


@app.get("/metrics")
def metrics() -> Response:
    """Expose Prometheus metrics."""
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)


def _background_workload() -> None:
    """
    Simulate a few workflow runs so that the histogram is not empty.
    In a real service this would be replaced by actual business logic.
    """
    for name, ok, sleep_sec in [
        ("dataset_ingest", True, 0.12),
        ("data_validation", False, 0.07),
    ]:
        start = time.time()
        time.sleep(sleep_sec)
        duration = time.time() - start
        record_workflow(name, ok, duration)


def start_background_thread() -> threading.Thread:
    """Start the dummy workload in a daemon thread."""
    t = threading.Thread(target=_background_workload, daemon=True)
    t.start()
    return t


if __name__ == "__main__":
    # Run with `uvicorn app.main:app --host 0.0.0.0 --port 8000`
    # The `start_http_server` call is **not** needed because FastAPI
    # already serves `/metrics`.  It is kept for compatibility with
    # pure‑prometheus‑client usage.
    start_http_server(8000)          # optional, harmless
    start_background_thread()
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)