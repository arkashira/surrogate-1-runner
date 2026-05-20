from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import json

app = FastAPI()

class Tool(BaseModel):
    name: str
    url: str

class Workflow(BaseModel):
    name: str
    steps: List[str]

tools = []
workflows = []

@app.post("/tools/")
def create_tool(tool: Tool):
    tools.append(tool)
    return {"message": "Tool created successfully"}

@app.get("/tools/")
def read_tools():
    return tools

@app.post("/workflows/")
def create_workflow(workflow: Workflow):
    workflows.append(workflow)
    return {"message": "Workflow created successfully"}

@app.get("/workflows/")
def read_workflows():
    return workflows

@app.post("/workflows/{workflow_id}/steps/")
def add_step(workflow_id: int, step: str):
    if workflow_id < len(workflows):
        workflows[workflow_id].steps.append(step)
        return {"message": "Step added successfully"}
    else:
        raise HTTPException(status_code=404, detail="Workflow not found")

@app.get("/workflows/{workflow_id}/steps/")
def read_steps(workflow_id: int):
    if workflow_id < len(workflows):
        return workflows[workflow_id].steps
    else:
        raise HTTPException(status_code=404, detail="Workflow not found")