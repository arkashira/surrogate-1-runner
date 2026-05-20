import asyncio
import json
import websockets
from config.webrtc_config import WebRTCConfig

class Shell:
    def __init__(self):
        self.config = WebRTCConfig()
        self.shell_process = None

    async def start_shell(self):
        self.shell_process = await asyncio.create_subprocess_shell(
            self.config.shell_command,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

    async def handle_input(self, websocket, path):
        await self.start_shell()
        try:
            while True:
                data = await websocket.recv()
                if data == "exit":
                    break
                self.shell_process.stdin.write(data.encode() + b'\n')
                output = await self.shell_process.stdout.readline()
                await websocket.send(output.decode())
        finally:
            self.shell_process.terminate()

async def main():
    shell = Shell()
    async with websockets.serve(shell.handle_input, "0.0.0.0", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())