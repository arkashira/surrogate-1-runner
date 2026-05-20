"""FastAPI GitHub Webhook Listener with HMAC Verification and Task Management

This module implements a secure webhook listener that:
1. Validates GitHub webhook signatures
2. Processes issue events (opened/closed)
3. Maintains task state in memory (replace with database in production)
"""

import hmac
import hashlib
import json
import os
from typing import Dict, Any
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse

app = FastAPI(title="GitHub Webhook Listener")

# Configuration - should be loaded from environment variables in production
GITHUB_WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET", "supersecret")
TASK_STORE: Dict[int, Dict[str, Any]] = {}

def verify_signature(payload: bytes, signature: str) -> bool:
    """Verify GitHub webhook HMAC signature using SHA-256."""
    mac = hmac.new(
        GITHUB_WEBHOOK_SECRET.encode(),
        msg=payload,
        digestmod=hashlib.sha256
    )
    expected = f"sha256={mac.hexdigest()}"
    return hmac.compare_digest(expected, signature)

def create_task(issue: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new task from a GitHub issue."""
    task_id = issue["number"]
    TASK_STORE[task_id] = {
        "id": task_id,
        "title": issue["title"],
        "state": "open",
        "url": issue["html_url"],
        "description": issue.get("body", "")
    }
    return TASK_STORE[task_id]

def update_task_status(issue: Dict[str, Any]) -> Dict[str, Any]:
    """Update task status based on GitHub issue state."""
    task_id = issue["number"]
    if task_id not in TASK_STORE:
        return create_task(issue)

    TASK_STORE[task_id]["state"] = "closed" if issue["state"] == "closed" else "open"
    return TASK_STORE[task_id]

@app.post("/webhook")
async def github_webhook(
    request: Request,
    x_github_event: str = Header(..., alias="X-GitHub-Event"),
    x_hub_signature_256: str = Header(..., alias="X-Hub-Signature-256")
):
    """Endpoint to receive and process GitHub webhook events.

    Args:
        request: FastAPI request object
        x_github_event: GitHub event type header
        x_hub_signature_256: HMAC signature for verification

    Returns:
        JSONResponse: Processing result

    Raises:
        HTTPException: For invalid signatures or malformed data
    """
    raw_body = await request.body()

    # Verify webhook signature
    if not verify_signature(raw_body, x_hub_signature_256):
        raise HTTPException(status_code=401, detail="Invalid signature")

    try:
        payload = json.loads(raw_body.decode())
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Malformed JSON")

    # Process supported events
    if x_github_event == "issues":
        action = payload.get("action")
        issue = payload.get("issue")

        if not issue:
            raise HTTPException(status_code=400, detail="Missing issue data")

        if action == "opened":
            task = create_task(issue)
            return JSONResponse(content={"status": "created", "task": task})
        elif action == "closed":
            task = update_task_status(issue)
            return JSONResponse(content={"status": "updated", "task": task})

    # Default response for unsupported events
    return JSONResponse(content={"status": "ignored", "event_type": x_github_event})

@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "GitHub Webhook Listener is running"}