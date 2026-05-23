from fastapi import FastAPI, HTTPException
from src.llm_agent_integration import LLMAgentIntegration, OpenAIAgent, HuggingFaceAgent

app = FastAPI()
integration = LLMAgentIntegration()

# Initialize agents
openai_agent = OpenAIAgent(api_key="your_openai_api_key")
huggingface_agent = HuggingFaceAgent(model_name="your_huggingface_model")

# Add agents to integration
integration.add_agent("openai", openai_agent)
integration.add_agent("huggingface", huggingface_agent)

@app.post("/generate_response")
async def generate_response(agent_name: str, prompt: str):
    try:
        response = integration.get_response(agent_name, prompt)
        return {"response": response}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/switch_agent")
async def switch_agent(current_agent_name: str, new_agent_name: str):
    try:
        integration.switch_agent(current_agent_name, new_agent_name)
        return {"message": f"Switched from {current_agent_name} to {new_agent_name}"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))