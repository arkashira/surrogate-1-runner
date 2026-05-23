import pytest
from fastapi.testclient import TestClient
from fastapi import WebSocketDisconnect
from src.api.transcription import router, verify_api_key
from unittest.mock import AsyncMock, patch

client = TestClient(router)

@pytest.mark.asyncio
async def test_transcribe_endpoint():
    with patch('src.api.transcription.process_audio', return_value={"text": "test", "confidence": 0.95}):
        with client.websocket_connect("/v1/transcribe", headers={"Authorization": "Bearer YOUR_API_KEY"}) as websocket:
            websocket.send_bytes(b"audio_data")
            data = websocket.receive_text()
            assert data == '{"text": "test", "confidence": 0.95}'

@pytest.mark.asyncio
async def test_invalid_api_key():
    with pytest.raises(WebSocketDisconnect):
        with client.websocket_connect("/v1/transcribe", headers={"Authorization": "Bearer INVALID_KEY"}):
            pass