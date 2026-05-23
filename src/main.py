from fastapi import FastAPI
from src.middleware.request_validation import request_validation_middleware
from src.routes.metrics import router as metrics_router

app = FastAPI(
    title="Surrogate Datadog API",
    version="1.0.0",
    description="A tiny mock of Datadog’s metric ingestion endpoint."
)

# Global middleware – runs for *every* request.
app.middleware("http")(request_validation_middleware)

# Mount the router under the required prefix.
app.include_router(metrics_router, prefix="/api/v2")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)