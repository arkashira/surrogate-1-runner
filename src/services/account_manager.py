import uuid
from typing import List

class TeamAccount:
    def __init__(self, id: str, name: str, members: List[str]):
        self.id = id
        self.name = name
        self.members = members

class AccountManager:
    def create_team_account(self, name: str, members: List[str]) -> TeamAccount:
        team_account_id = str(uuid.uuid4())
        team_account = TeamAccount(id=team_account_id, name=name, members=members)
        # Logic to link team account to Freedom Link and setup usage tracking/reporting
        return team_account