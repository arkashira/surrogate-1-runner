from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

app = FastAPI()

MODEL_ENDPOINTS = {
    "claude": "https://api.claude.com/v1/chat/completions",
    "gpt-4": "https://api.openai.com/v1/chat/completions",
    "gemini": "https://api.gemini.com/v1/chat/completions"
}

class AIRequest(BaseModel):
    model: str
    messages: list[dict[str, str]]

async def forward_request(payload: AIRequest):
    if payload.model not in MODEL_ENDPOINTS:
        raise HTTPException(status_code=400, detail="Invalid model specified")

    async with httpx.AsyncClient() as client:
        response = await client.post(MODEL_ENDPOINTS[payload.model], json=payload.dict())
        return response.json()

@app.post("/ai")
async def ai_endpoint(ai_request: AIRequest):
    try:
        response = await forward_request(ai_request)
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))