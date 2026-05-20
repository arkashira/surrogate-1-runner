import asyncio
import websockets

class WebSocketServer:
    async def handle_connection(self, websocket):
        async for message in websocket:
            print(f"Received message: {message}")

    async def start(self):
        async with websockets.serve(self.handle_connection, "localhost", 8765):
            await asyncio.Future()  # run forever

async def main():
    server = WebSocketServer()
    await server.start()

if __name__ == "__main__":
    asyncio.run(main())