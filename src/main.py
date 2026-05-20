from fastapi import FastAPI
from .api.workflows import router as workflow_router

def create_app() -> FastAPI:
    """
    Factory that builds the FastAPI application.
    Keeping it in a function makes testing (e.g. with `TestClient`) easier
    and avoids side‑effects at import time.
    """
    app = FastAPI(
        title="Surrogate‑1 API",
        description="Accepts workflow definitions and returns a correlation ID.",
        version="1.0.0",
    )
    app.include_router(workflow_router)
    return app

app = create_app()