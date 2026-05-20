class OnboardingEngine:
    def __init__(self, db):
        self.db = db

    def load_sequence_and_progress(self, user_id, sequence_id):
        """Load a sequence and current progress for a user."""
        sequence = self.db.get_sequence(sequence_id)
        progress = self.db.get_user_progress(user_id, sequence_id)
        return {
            "sequence": sequence,
            "progress": progress
        }

    def get_next_step(self, user_id, sequence_id):
        """Return the next step for a user in a sequence."""
        data = self.load_sequence_and_progress(user_id, sequence_id)
        sequence = data["sequence"]
        progress = data["progress"]
        
        current_step = progress.get("current_step", 0)
        
        # Find the next step in the sequence
        for step in sequence:
            if step["step_id"] == current_step + 1:
                return step
        
        # If no next step found, sequence might be complete
        return None

    def update_user_progress(self, user_id, sequence_id, step_id):
        """Update the user's progress after completing a step."""
        self.db.update_user_progress(user_id, sequence_id, step_id)