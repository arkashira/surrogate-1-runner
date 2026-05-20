
from typing import List, Dict

class WorkflowManager:
    def __init__(self):
        self.tools = []

    def add_tool(self, tool: Dict):
        self.tools.append(tool)

    def remove_tool(self, tool_id: int):
        self.tools = [tool for index, tool in enumerate(self.tools) if index != tool_id]

    def modify_tool(self, tool_id: int, updates: Dict):
        self.tools[tool_id].update(updates)

    def get_tools(self) -> List[Dict]:
        return self.tools