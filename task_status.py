import asyncio
import websockets
import json
from datetime import datetime
from typing import Dict, List, Set
from flask import Flask, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

class TaskStatusManager:
    def __init__(self):
        self.tasks: Dict[str, Dict] = {}
        self.milestones: Dict[str, List] = {}
        self.active_connections: Set = set()
        self.lock = asyncio.Lock()

    async def connect(self, websocket):
        self.active_connections.add(websocket)
        try:
            await self._send_initial_state(websocket)
            await websocket.wait_closed()
        finally:
            self.active_connections.remove(websocket)

    async def _send_initial_state(self, websocket):
        await websocket.send(json.dumps({
            "type": "INITIAL_STATE",
            "tasks": self.tasks,
            "milestones": self.milestones
        }))

    async def update_task(self, task_id: str, status: str, deadline: str = None, milestone: str = None):
        async with self.lock:
            self.tasks[task_id] = {
                "id": task_id,
                "status": status,
                "deadline": deadline or self.tasks.get(task_id, {}).get("deadline"),
                "milestone": milestone or self.tasks.get(task_id, {}).get("milestone"),
                "last_updated": datetime.utcnow().isoformat()
            }

            if milestone:
                if task_id not in self.milestones:
                    self.milestones[task_id] = []
                self.milestones[task_id].append({
                    "milestone": milestone,
                    "timestamp": datetime.utcnow().isoformat()
                })

        await self._broadcast_update()

    async def _broadcast_update(self):
        message = json.dumps({
            "type": "TASK_UPDATE",
            "tasks": self.tasks,
            "milestones": self.milestones
        })
        if self.active_connections:
            await asyncio.gather(
                *[conn.send(message) for conn in self.active_connections]
            )
        socketio.emit('task_update', message)

    @app.route('/api/tasks', methods=['GET'])
    def get_tasks():
        return jsonify({
            "tasks": manager.tasks,
            "milestones": manager.milestones
        })

manager = TaskStatusManager()

@socketio.on('connect')
def handle_connect():
    print('Client connected')

async def websocket_handler(websocket, path):
    await manager.connect(websocket)

def start_websocket_server():
    start_server = websockets.serve(
        websocket_handler,
        "0.0.0.0",
        8765,
        ping_interval=20
    )
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    start_websocket_server()