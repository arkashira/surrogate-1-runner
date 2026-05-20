import time
from fastapi import FastAPI, HTTPException

from .api.metrics import router as metrics_router, record_workflow_latency

app = FastAPI(title="Surrogate Workflow Service")

# ----------------------------------------------------------------------
# 2️⃣  Mount the metrics router under /metrics
# ----------------------------------------------------------------------
app.include_router(metrics_router)          # /metrics endpoint is now live

@app.get("/", tags=["health"])
async def read_root():
    """Simple health‑check endpoint."""
    return {"message": "Hello World"}


@app.get("/workflow/{workflow_name}", tags=["workflow"])
async def run_workflow(workflow_name: str):
    """
    Simulated workflow execution.
    In a real system you would replace the `time.sleep` with the actual work.
    """
    start = time.time()
    try:
        # ------------------- BEGIN simulated work -------------------
        # Replace this block with your real workflow logic.
        time.sleep(0.1)                     # pretend the workflow takes ~100 ms
        # -------------------- END simulated work --------------------
        status = "success"
        return {"workflow_name": workflow_name, "status": status}
    except Exception as exc:                # pragma: no cover – defensive
        status = "failure"
        raise HTTPException(status_code=500, detail=str(exc))
    finally:
        # ------------------------------------------------------------------
        # 3️⃣  Record latency *exactly once* – even if the handler raised.
        # ------------------------------------------------------------------
        latency = time.time() - start
        record_workflow_latency(workflow_name, status, latency)