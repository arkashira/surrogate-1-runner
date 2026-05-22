import asyncio
import json
import logging
from typing import Dict, Any

import websockets
from websockets.server import WebSocketServerProtocol

# Configure basic logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

# Expected payload schema
REQUIRED_FIELDS = {
    "file_path": str,
    "content": str,
    "cursor_position": int,
    "selection": str,
}


def validate_payload(data: Dict[str, Any]) -> None:
    """
    Validate that the incoming JSON payload matches the expected schema.
    Raises ValueError with a descriptive message if validation fails.
    """
    if not isinstance(data, dict):
        raise ValueError("Payload must be a JSON object")

    missing = [field for field in REQUIRED_FIELDS if field not in data]
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")

    for field, expected_type in REQUIRED_FIELDS.items():
        if not isinstance(data[field], expected_type):
            raise ValueError(
                f"Field '{field}' must be of type {expected_type.__name__}"
            )


async def handle_connection(ws: WebSocketServerProtocol, path: str) -> None:
    """
    Handle an individual WebSocket connection.
    Receives a single JSON message, validates it, and sends an acknowledgment.
    """
    try:
        message = await asyncio.wait_for(ws.recv(), timeout=0.2)
        logger.debug("Received raw message: %s", message)

        try:
            payload = json.loads(message)
        except json.JSONDecodeError as exc:
            error_msg = f"Invalid JSON: {exc}"
            logger.warning(error_msg)
            await ws.send(json.dumps({"status": "error", "message": error_msg}))
            return

        try:
            validate_payload(payload)
        except ValueError as exc:
            error_msg = f"Validation error: {exc}"
            logger.warning(error_msg)
            await ws.send(json.dumps({"status": "error", "message": error_msg}))
            return

        # If we reach here, payload is valid
        logger.info("Valid payload received from %s", ws.remote_address)
        await ws.send(json.dumps({"status": "ok"}))

    except asyncio.TimeoutError:
        logger.warning("Client did not send data within 200ms")
        await ws.send(json.dumps({"status": "error", "message": "Timeout waiting for data"}))
    except websockets.exceptions.ConnectionClosedOK:
        logger.info("Connection closed normally")
    except Exception as exc:
        logger.exception("Unexpected error: %s", exc)
        await ws.send(json.dumps({"status": "error", "message": str(exc)}))


async def start_server(port: int = 8765) -> None:
    """
    Start the WebSocket server on the specified port.
    """
    logger.info("Starting WebSocket server on port %s", port)
    async with websockets.serve(handle_connection, "0.0.0.0", port):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    # Allow overriding port via environment variable
    port = int(os.getenv("SURROGATE_WS_PORT", "8765"))
    try:
        asyncio.run(start_server(port))
    except KeyboardInterrupt:
        logger.info("Server stopped by user")