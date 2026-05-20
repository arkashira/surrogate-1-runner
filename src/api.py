from fastapi import FastAPI
from ai_models.GPT4 import GPT4

app = FastAPI()

@app.post("/gpt4/")
def gpt4_endpoint(prompt: str):
    api_key = os.getenv("OPENAI_API_KEY")
    gpt4 = GPT4(api_key)
    response = gpt4.generate_response(prompt)
    return {"response": response}