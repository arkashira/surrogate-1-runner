from typing import List

class TerminalSession:
    def __init__(self, session_id: str, owner: str):
        self.session_id = session_id
        self.owner = owner
        self.users: List[str] = [owner]
        self.output_buffer = []

    def add_user(self, user: str):
        if user not in self.users:
            self.users.append(user)

    def remove_user(self, user: str):
        if user in self.users:
            self.users.remove(user)

    def add_output(self, data: str):
        self.output_buffer.append(data)
        self.broadcast(data)

    def broadcast(self, data: str):
        # In a real implementation, this would send data to all connected users
        pass

    def get_output(self) -> List[str]:
        return self.output_buffer.copy()