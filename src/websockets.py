import asyncio
import websockets
from typing import Dict, List

class WebSocketServer:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.clients: Dict[str, websockets.WebSocketServerProtocol] = {}

    async def handler(self, websocket: websockets.WebSocketServerProtocol, path: str):
        client_id = id(websocket)
        self.clients[client_id] = websocket
        try:
            async for message in websocket:
                await self.broadcast(message)
        finally:
            del self.clients[client_id]

    async def broadcast(self, message: str):
        if self.clients:
            await asyncio.wait([client.send(message) for client in self.clients.values()])

    def start(self):
        start_server = websockets.serve(self.handler, self.host, self.port)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

def main():
    server = WebSocketServer('localhost', 8765)
    server.start()

if __name__ == "__main__":
    main()