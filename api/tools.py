from typing import List
import json

class Tool:
    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url

class ToolManager:
    def __init__(self):
        self.tools = []

    def add_tool(self, tool: Tool):
        self.tools.append(tool)

    def get_tools(self):
        return self.tools

tool_manager = ToolManager()

def add_tool(name: str, url: str):
    tool = Tool(name, url)
    tool_manager.add_tool(tool)

def get_tools():
    return tool_manager.get_tools()