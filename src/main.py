import os
import asyncio

from .server import start_server

def main() -> None:
    """
    Entry point for the surrogate-1 WebSocket server.
    Reads the port from the SURROGATE_WS_PORT environment variable,
    defaults to 8765, and starts the async server.
    """
    port = int(os.getenv("SURROGATE_WS_PORT", "8765"))
    try:
        asyncio.run(start_server(port))
    except KeyboardInterrupt:
        print("\nSurrogate-1 WebSocket server stopped.")


if __name__ == "__main__":
    main()