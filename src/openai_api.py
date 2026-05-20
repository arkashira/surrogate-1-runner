import openai

class OpenAIAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = api_key

    def generate_text(self, prompt, model="text-davinci-003", max_tokens=50):
        response = openai.Completion.create(
            engine=model,
            prompt=prompt,
            max_tokens=max_tokens
        )
        return response.choices[0].text.strip()

    def get_embeddings(self, text, model="text-similarity-davinci-001"):
        response = openai.Embedding.create(
            input=text,
            model=model
        )
        return response.data[0].embedding

    def list_models(self):
        models = openai.Model.list()
        return [model.id for model in models.data]