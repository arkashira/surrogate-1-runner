import asyncio
from typing import List
from .websockets import WebSocketServer

class TerminalEnvironment:
    def __init__(self, websocket_host: str, websocket_port: int):
        self.websocket_server = WebSocketServer(websocket_host, websocket_port)
        self.users: List[str] = []

    async def add_user(self, user_id: str):
        self.users.append(user_id)
        await self.update_environment()

    async def remove_user(self, user_id: str):
        self.users.remove(user_id)
        await self.update_environment()

    async def update_environment(self):
        message = f"Users in environment: {', '.join(self.users)}"
        await self.websocket_server.broadcast(message)

    def start(self):
        self.websocket_server.start()

def main():
    env = TerminalEnvironment('localhost', 8765)
    asyncio.run(env.add_user("user1"))
    asyncio.run(env.add_user("user2"))
    env.start()

if __name__ == "__main__":
    main()