from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from auth import get_api_key
from whisper_wrapper import WhisperWrapper
import json

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

whisper_wrapper = WhisperWrapper()

@app.websocket("/v1/transcribe")
async def websocket_endpoint(
    websocket: WebSocket,
    api_key: str = Depends(get_api_key)
):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_bytes()
            audio_data = np.frombuffer(data, dtype=np.int16)
            transcription = whisper_wrapper.transcribe_stream(audio_data)
            await websocket.send_text(json.dumps(transcription))
    except WebSocketDisconnect:
        print("Client disconnected")