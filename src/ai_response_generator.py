from typing import List, Dict
import random
import json
import os

class AIResponseGenerator:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.conversation_history = []
        self.load_conversation()

    def generate_response(self, user_input: str) -> str:
        """
        Generates a response based on the user input.
        """
        responses = [
            "That's an interesting point. Can you elaborate on that?",
            "I see. How does that relate to your previous statement?",
            "I'm not sure I understand. Could you rephrase that?",
            "That's a good question. Let me think about it.",
            "I appreciate your input. How do you feel about this topic?"
        ]
        response = random.choice(responses)
        self.conversation_history.append({"user": user_input, "ai": response})
        self.save_conversation()
        return response

    def get_conversation_history(self) -> List[Dict[str, str]]:
        """
        Returns the conversation history.
        """
        return self.conversation_history

    def save_conversation(self) -> None:
        """
        Saves the conversation history to a JSON file.
        """
        file_path = f"/opt/axentx/surrogate-1/data/conversations/{self.session_id}.json"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            json.dump(self.conversation_history, file, indent=4)

    def load_conversation(self) -> None:
        """
        Loads the conversation history from a JSON file.
        """
        file_path = f"/opt/axentx/surrogate-1/data/conversations/{self.session_id}.json"
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                self.conversation_history = json.load(file)

# /opt/axentx/surrogate-1/tests/test_ai_response_generator.py
import unittest
from src.ai_response_generator import AIResponseGenerator

class TestAIResponseGenerator(unittest.TestCase):
    def setUp(self):
        self.session_id = "test_session"
        self.generator = AIResponseGenerator(self.session_id)

    def tearDown(self):
        file_path = f"/opt/axentx/surrogate-1/data/conversations/{self.session_id}.json"
        if os.path.exists(file_path):
            os.remove(file_path)

    def test_generate_response(self):
        user_input = "Hello, how are you?"
        response = self.generator.generate_response(user_input)
        self.assertIn(response, [
            "That's an interesting point. Can you elaborate on that?",
            "I see. How does that relate to your previous statement?",
            "I'm not sure I understand. Could you rephrase that?",
            "That's a good question. Let me think about it.",
            "I appreciate your input. How do you feel about this topic?"
        ])

    def test_get_conversation_history(self):
        user_input = "Hello, how are you?"
        self.generator.generate_response(user_input)
        history = self.generator.get_conversation_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["user"], user_input)

if __name__ == '__main__':
    unittest.main()