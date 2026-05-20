
from typing import List, Dict
import json

class OnboardingSurvey:
    def __init__(self):
        self.questions = [
            {"id": 1, "type": "text", "question": "What is your business name?"},
            {"id": 2, "type": "text", "question": "What is your website?"},
            {"id": 3, "type": "select", "question": "Which marketing channels do you currently use?", "options": ["Social Media", "Email", "SEO", "PPC", "Other"]},
            {"id": 4, "type": "text", "question": "What are your current marketing challenges?"},
            {"id": 5, "type": "text", "question": "What are your marketing goals for the next 6 months?"},
        ]

    def get_survey(self) -> List[Dict]:
        return self.questions

    def submit_survey(self, responses: List[Dict]) -> None:
        # Save responses to a file or database
        with open('survey_responses.json', 'w') as f:
            json.dump(responses, f)

# Test the OnboardingSurvey class
survey = OnboardingSurvey()
print(json.dumps(survey.get_survey(), indent=4))

# Sample responses
responses = [
    {"id": 1, "answer": "AxentX"},
    {"id": 2, "answer": "https://axentx.com"},
    {"id": 3, "answer": ["Social Media", "SEO"]},
    {"id": 4, "answer": "Reaching a larger audience"},
    {"id": 5, "answer": "Increase website traffic by 50%"},
]

survey.submit_survey(responses)