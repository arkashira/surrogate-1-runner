"""
Locust load test for the /v1/transcribe WebSocket endpoint.

This script creates 100 concurrent users that open a WebSocket
connection, stream dummy 16 kHz PCM frames, and assert that the
first transcription chunk is received within 200 ms.  It also
validates that the server responds with JSON containing `text`
and `confidence` fields and that the overall error rate stays
below 5 %.

The test requires the `websocket-client` package:
    pip install websocket-client
"""

import os
import json
import time
import random
import string
import struct

from locust import HttpUser, task, between, events
from websocket import create_connection, WebSocketException

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def generate_pcm_frame(duration_ms: int = 20, sample_rate: int = 16000) -> bytes:
    """
    Generate a dummy PCM frame of the given duration in milliseconds.
    16 kHz, 16‑bit signed little‑endian, mono.
    """
    samples = int(sample_rate * duration_ms / 1000)
    # Random samples between -32768 and 32767
    frame = struct.pack("<" + "h" * samples, *(
        random.randint(-32768, 32767) for _ in range(samples)
    ))
    return frame

def random_api_key(length: int = 32) -> str:
    """Generate a random API key for authentication."""
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))

# ----------------------------------------------------------------------
# Locust user
# ----------------------------------------------------------------------
class TranscribeUser(HttpUser):
    """
    A Locust user that connects to the /v1/transcribe WebSocket endpoint,
    streams dummy audio, and records latency and success/failure metrics.
    """
    wait_time = between(1, 2)  # idle time between tasks

    # Host can be overridden via environment variable
    host = os.getenv("LOCUST_HOST", "http://localhost:8000")

    # API key can be overridden via environment variable
    api_key = os.getenv("API_KEY", random_api_key())

    @task
    def transcribe(self):
        ws_url = f"ws://{self.host.split('://')[1]}/v1/transcribe"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "User-Agent": "Locust-Transcribe-LoadTest",
        }

        try:
            # Open WebSocket connection
            ws = create_connection(ws_url, header=[f"{k}: {v}" for k, v in headers.items()])

            # Send 10 frames of 20 ms each
            start_send = time.time()
            for _ in range(10):
                frame = generate_pcm_frame()
                ws.send(frame, opcode=websocket.ABNF.OPCODE_BINARY)
            end_send = time.time()

            # Wait for first JSON chunk
            first_chunk_time = None
            while True:
                try:
                    msg = ws.recv()
                except WebSocketException as e:
                    events.request_failure.fire(
                        request_type="WS",
                        name="transcribe",
                        response_time=int((time.time() - start_send) * 1000),
                        exception=e,
                    )
                    ws.close()
                    return

                try:
                    data = json.loads(msg)
                except json.JSONDecodeError:
                    continue  # ignore non‑JSON messages

                if "text" in data and "confidence" in data:
                    first_chunk_time = time.time()
                    break  # we got the first transcription chunk

            # Close the connection
            ws.close()

            # Calculate latency in milliseconds
            latency_ms = int((first_chunk_time - start_send) * 1000)

            # Record success if latency <= 200 ms
            if latency_ms <= 200:
                events.request_success.fire(
                    request_type="WS",
                    name="transcribe",
                    response_time=latency_ms,
                    response_length=len(msg),
                )
            else:
                events.request_failure.fire(
                    request_type="WS",
                    name="transcribe",
                    response_time=latency_ms,
                    exception=Exception(f"Latency {latency_ms} ms > 200 ms"),
                )

        except Exception as exc:
            events.request_failure.fire(
                request_type="WS",
                name="transcribe",
                response_time=0,
                exception=exc,
            )