import asyncio
import websockets
import json

class Shell:
    def __init__(self):
        self.websocket = None

    async def connect(self):
        self.websocket = await websockets.connect('ws://localhost:8765')

    async def send_command(self, command):
        await self.websocket.send(json.dumps({'command': command}))

    async def receive_output(self):
        while True:
            try:
                output = await self.websocket.recv()
                yield output
            except websockets.ConnectionClosed:
                break

    async def close(self):
        await self.websocket.close()

async def main():
    shell = Shell()
    await shell.connect()
    while True:
        command = input('Enter command: ')
        await shell.send_command(command)
        async for output in shell.receive_output():
            print(output)

asyncio.run(main())