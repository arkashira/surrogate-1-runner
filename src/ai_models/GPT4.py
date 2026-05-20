import os
import openai

class GPT4:
    def __init__(self, api_key):
        openai.api_key = api_key
        self.model_engine = "text-davinci-003"

    def generate_response(self, prompt):
        response = openai.Completion.create(
            engine=self.model_engine,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        return response.choices[0].text.strip()