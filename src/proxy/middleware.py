
from os import getenv
from fastapi import HTTPException

def surrogate_struct_output_middleware(app):
    async def middleware(request, call_next):
        if getenv("SURROGATE_STRUCT_OUTPUT_ENABLED", "false").lower() not in ["true", "1"]:
            raise HTTPException(status_code=501, detail="Structured output tool calling is not enabled.")
        response = await call_next(request)
        return response

    app.middleware("http")(middleware)