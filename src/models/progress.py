
from datetime import datetime, timedelta
from typing import Dict, Any

class Progress:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.session_count = 0
        self.terms_learned = 0
        self.streak = 0
        self.last_practice_date = None

    def increment_session(self):
        self.session_count += 1
        self.streak = 1 if self.last_practice_date is None else self.streak + 1
        self.last_practice_date = datetime.now()

    def learn_term(self):
        self.terms_learned += 1

    def calculate_progress(self) -> Dict[str, Any]:
        total_sessions = self.session_count
        learned_terms = self.terms_learned
        if total_sessions > 0:
            percentage_learned = (learned_terms / total_sessions) * 100
        else:
            percentage_learned = 0
        streak_days = self.streak if self.last_practice_date is not None else 0
        return {
            "total_sessions": total_sessions,
            "terms_learned": learned_terms,
            "percentage_learned": percentage_learned,
            "streak_days": streak_days,
        }

    def export_progress_csv(self, filename: str):
        # Implement CSV export functionality here
        pass