import asyncio
import websockets
from axentx import settings
from axentx.utils import get_pipeline_status

async def handle_connection(websocket, path):
    while True:
        pipeline_status = await get_pipeline_status()
        await websocket.send(pipeline_status)

async def main():
    async with websockets.serve(handle_connection, settings.WEB_SOCKET_HOST, settings.WEB_SOCKET_PORT):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())