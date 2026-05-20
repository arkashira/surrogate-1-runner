import json
from typing import Dict, List

class LabProgressService:
    def __init__(self):
        self.lab_paths = {}
        self.progress = {}

    def add_lab_path(self, lab_path: str, challenges: List[str]):
        self.lab_paths[lab_path] = challenges
        self.progress[lab_path] = {challenge: False for challenge in challenges}

    def update_progress(self, lab_path: str, challenge: str, completed: bool):
        if lab_path in self.progress and challenge in self.progress[lab_path]:
            self.progress[lab_path][challenge] = completed

    def get_progress(self, lab_path: str):
        return self.progress.get(lab_path, {})

    def get_completion_badge(self, lab_path: str):
        progress = self.get_progress(lab_path)
        if progress:
            completed_challenges = sum(1 for challenge, completed in progress.items() if completed)
            total_challenges = len(progress)
            return f"{completed_challenges}/{total_challenges}"
        return "0/0"

    def to_json(self):
        return json.dumps(self.progress)

    @classmethod
    def from_json(cls, json_str: str):
        service = cls()
        progress = json.loads(json_str)
        for lab_path, challenges in progress.items():
            service.add_lab_path(lab_path, list(challenges.keys()))
            for challenge, completed in challenges.items():
                service.update_progress(lab_path, challenge, completed)
        return service