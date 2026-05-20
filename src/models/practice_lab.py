class PracticeLab:
    def __init__(self, id, title, description, instructions, objectives, difficulty, duration):
        self.id = id
        self.title = title
        self.description = description
        self.instructions = instructions
        self.objectives = objectives
        self.difficulty = difficulty
        self.duration = duration

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'instructions': self.instructions,
            'objectives': self.objectives,
            'difficulty': self.difficulty,
            'duration': self.duration
        }