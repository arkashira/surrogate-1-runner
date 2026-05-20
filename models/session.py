from datetime import datetime
from typing import Dict

class Session:
    def __init__(self, session_id: str, start_time: datetime, end_time: datetime, participants: Dict[str, str]):
        self.session_id = session_id
        self.start_time = start_time
        self.end_time = end_time
        self.participants = participants  # Mapping of participant ID to their role

    def add_participant(self, participant_id: str, role: str) -> None:
        self.participants[participant_id] = role

    def remove_participant(self, participant_id: str) -> None:
        if participant_id in self.participants:
            del self.participants[participant_id]

    def get_participant_role(self, participant_id: str) -> str:
        return self.participants.get(participant_id, '')

# Example usage
if __name__ == "__main__":
    session = Session('session1', datetime.now(), datetime.now(), {})
    session.add_participant('user1', 'viewer')
    print(session.get_participant_role('user1'))  # Output: viewer