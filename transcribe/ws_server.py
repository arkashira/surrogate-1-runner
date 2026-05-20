import asyncio
import websockets
from whisper_wrapper import WhisperWrapper
import numpy as np
import json

class TranscriptionWebSocketServer:
    def __init__(self, host: str = "0.0.0.0", port: int = 8765):
        self.host = host
        self.port = port
        self.whisper_wrapper = WhisperWrapper()

    async def handle_connection(self, websocket, path):
        try:
            async for message in websocket:
                # Decode the audio frame
                audio_data = np.frombuffer(message, dtype=np.int16)

                # Transcribe the audio
                transcription = self.whisper_wrapper.transcribe_stream(audio_data)

                # Send the transcription result back
                await websocket.send(json.dumps(transcription))
        except Exception as e:
            print(f"Error handling connection: {e}")

    async def start(self):
        async with websockets.serve(self.handle_connection, self.host, self.port):
            print(f"WebSocket server started on ws://{self.host}:{self.port}")
            await asyncio.Future()  # run forever

if __name__ == "__main__":
    server = TranscriptionWebSocketServer()
    asyncio.run(server.start())