import pytest
from fastapi.testclient import TestClient

# Import the main FastAPI app – assuming it is defined in `app.py` at repo root.
# If the actual entry point differs, adjust the import accordingly.
from ..app import app  # type: ignore

client = TestClient(app)


def test_conversation_flow():
    # Start a new session
    start_resp = client.post("/conversation/start")
    assert start_resp.status_code == 201
    data = start_resp.json()
    session_id = data["session_id"]
    assert isinstance(session_id, str)
    assert data["messages"] == []

    # Send a user message
    msg_payload = {"content": "Hello, AI!"}
    msg_resp = client.post(f"/conversation/{session_id}/message", json=msg_payload)
    assert msg_resp.status_code == 200
    history = msg_resp.json()
    assert history["session_id"] == session_id
    assert len(history["messages"]) == 2
    assert history["messages"][0]["role"] == "user"
    assert history["messages"][0]["content"] == "Hello, AI!"
    assert history["messages"][1]["role"] == "assistant"
    assert history["messages"][1]["content"] == "AI: Hello, AI!"

    # Retrieve history
    get_resp = client.get(f"/conversation/{session_id}")
    assert get_resp.status_code == 200
    retrieved = get_resp.json()
    assert retrieved == history


def test_invalid_session():
    invalid_id = "non-existent-id"
    resp = client.get(f"/conversation/{invalid_id}")
    assert resp.status_code == 404
    assert "not found" in resp.json()["detail"]