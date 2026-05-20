
import json
from typing import Dict, List

class CommandPalette:
    def __init__(self):
        self.commands = {}

    def register_command(self, command_id: str, command_func: callable):
        self.commands[command_id] = command_func

    def get_commands(self) -> List[Dict]:
        return list(self.commands.items())

    def execute_command(self, command_id: str):
        if command_id in self.commands:
            return self.commands[command_id]()
        else:
            raise KeyError(f"Command '{command_id}' not found.")

# /opt/axentx/surrogate-1/command_palette_functionality.json

{
    "version": "1.0",
    "commands": [
        {
            "id": "ai_code_suggestions",
            "label": "AI Code Suggestions",
            "description": "Get AI-powered code suggestions for the current selection."
        },
        {
            "id": "ai_code_completions",
            "label": "AI Code Completions",
            "description": "Get AI-powered code completions for the current cursor position."
        },
        {
            "id": "customize_commands",
            "label": "Customize Commands",
            "description": "Customize the available commands and their functionality."
        }
    ]
}