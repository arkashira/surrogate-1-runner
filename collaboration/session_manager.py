import asyncio
import websockets
import yaml
from typing import Dict, List, Set

class SessionManager:
    def __init__(self, config_path: str = '/opt/axentx/surrogate-1/collaboration/config.yaml'):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        self.sessions: Dict[str, Set[str]] = {}
        self.websocket_connections: Dict[str, Dict[str, websockets.WebSocketServerProtocol]] = {}

    async def start(self):
        async with websockets.serve(self.handle_connection, self.config['host'], self.config['port']):
            await asyncio.Future()  # run forever

    async def handle_connection(self, websocket, path):
        session_id = path.strip('/')
        user_id = websocket.remote_address[0]

        if session_id not in self.sessions:
            self.sessions[session_id] = set()
            self.websocket_connections[session_id] = {}

        if len(self.sessions[session_id]) >= self.config.get('max_participants', 10):
            await websocket.close(code=4000, reason="Session full")
            return

        self.sessions[session_id].add(user_id)
        self.websocket_connections[session_id][user_id] = websocket

        try:
            async for message in websocket:
                await self.broadcast(session_id, message, user_id)
        except websockets.ConnectionClosedError:
            pass
        finally:
            self.remove_participant(session_id, user_id)

    async def broadcast(self, session_id: str, message: str, sender_id: str):
        for user_id, ws in self.websocket_connections[session_id].items():
            if user_id != sender_id:
                await ws.send(message)

    def get_participants(self, session_id: str) -> List[str]:
        return list(self.sessions.get(session_id, set()))

    def add_participant(self, session_id: str, user_id: str):
        if session_id not in self.sessions:
            self.sessions[session_id] = set()
            self.websocket_connections[session_id] = {}
        self.sessions[session_id].add(user_id)

    def remove_participant(self, session_id: str, user_id: str):
        if session_id in self.sessions and user_id in self.sessions[session_id]:
            self.sessions[session_id].remove(user_id)
            del self.websocket_connections[session_id][user_id]
            if not self.sessions[session_id]:
                del self.sessions[session_id]
                del self.websocket_connections[session_id]