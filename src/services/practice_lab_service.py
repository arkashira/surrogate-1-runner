from src.models.practice_lab import PracticeLab

class PracticeLabService:
    @staticmethod
    def get_practice_labs(objective=None, difficulty=None):
        # Mock data for practice labs
        practice_labs = [
            PracticeLab(1, 'Lab 1', 'Description for Lab 1', 'Instructions for Lab 1', ['Objective 1', 'Objective 2'], 'Easy', 30),
            PracticeLab(2, 'Lab 2', 'Description for Lab 2', 'Instructions for Lab 2', ['Objective 2', 'Objective 3'], 'Medium', 45),
            PracticeLab(3, 'Lab 3', 'Description for Lab 3', 'Instructions for Lab 3', ['Objective 1', 'Objective 3'], 'Hard', 60),
            # Add more practice labs as needed
        ]

        if objective:
            practice_labs = [lab for lab in practice_labs if objective in lab.objectives]
        if difficulty:
            practice_labs = [lab for lab in practice_labs if lab.difficulty == difficulty]

        return practice_labs

    @staticmethod
    def get_practice_lab_by_id(lab_id):
        practice_labs = PracticeLabService.get_practice_labs()
        for lab in practice_labs:
            if lab.id == lab_id:
                return lab
        return None