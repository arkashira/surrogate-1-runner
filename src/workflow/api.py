
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()
manager = WorkflowManager()

class Tool(BaseModel):
    id: int
    name: str
    status: str

@app.post("/tools/add")
def add_tool(tool: Tool):
    manager.add_tool(tool.dict())
    return {"message": "Tool added successfully"}

@app.post("/tools/remove/{tool_id}")
def remove_tool(tool_id: int):
    if tool_id not in [tool["id"] for tool in manager.get_tools()]:
        raise HTTPException(status_code=404, detail="Tool not found")
    manager.remove_tool(tool_id)
    return {"message": "Tool removed successfully"}

@app.put("/tools/modify/{tool_id}")
def modify_tool(tool_id: int, updates: Dict):
    if tool_id not in [tool["id"] for tool in manager.get_tools()]:
        raise HTTPException(status_code=404, detail="Tool not found")
    manager.modify_tool(tool_id, updates)
    return {"message": "Tool modified successfully"}

@app.get("/tools")
def get_tools():
    return manager.get_tools()