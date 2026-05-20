import json
import os
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class AITool:
    """Represents an AI tool available for single-click access."""
    name: str
    description: str
    url: str
    category: str
    icon_url: Optional[str] = None
    is_subscribed: bool = False


class SingleClickAccessManager:
    """Manages AI tools for single-click access and subscription management."""
    
    def __init__(self, storage_path: str = "ai_tools.json"):
        self.storage_path = Path(storage_path)
        self.tools: List[AITool] = []
        self._load_tools()
    
    def _load_tools(self):
        """Load AI tools from persistent storage."""
        if self.storage_path.exists():
            try:
                with open(self.storage_path, 'r') as f:
                    data = json.load(f)
                    self.tools = [AITool(**tool_data) for tool_data in data]
            except Exception:
                self.tools = []
        else:
            # Initialize with default tools if none exist
            self.tools = [
                AITool(
                    name="ChatGPT",
                    description="Advanced conversational AI",
                    url="https://chat.openai.com",
                    category="Chat",
                    icon_url="https://example.com/chatgpt-icon.png"
                ),
                AITool(
                    name="GitHub Copilot",
                    description="AI pair programmer",
                    url="https://github.com/features/copilot",
                    category="Development",
                    icon_url="https://example.com/copilot-icon.png"
                ),
                AITool(
                    name="Midjourney",
                    description="AI image generation",
                    url="https://www.midjourney.com",
                    category="Creative",
                    icon_url="https://example.com/midjourney-icon.png"
                )
            ]
            self._save_tools()
    
    def _save_tools(self):
        """Save AI tools to persistent storage."""
        with open(self.storage_path, 'w') as f:
            json.dump([asdict(tool) for tool in self.tools], f, indent=2)
    
    def get_available_tools(self) -> List[AITool]:
        """Get all available AI tools."""
        return self.tools.copy()
    
    def get_subscribed_tools(self) -> List[AITool]:
        """Get only subscribed AI tools."""
        return [tool for tool in self.tools if tool.is_subscribed]
    
    def subscribe_to_tool(self, tool_name: str) -> bool:
        """Subscribe to an AI tool by name."""
        for tool in self.tools:
            if tool.name == tool_name:
                tool.is_subscribed = True
                self._save_tools()
                return True
        return False
    
    def unsubscribe_from_tool(self, tool_name: str) -> bool:
        """Unsubscribe from an AI tool by name."""
        for tool in self.tools:
            if tool.name == tool_name:
                tool.is_subscribed = False
                self._save_tools()
                return True
        return False
    
    def add_tool(self, tool: AITool) -> bool:
        """Add a new AI tool."""
        # Check if tool already exists
        for existing_tool in self.tools:
            if existing_tool.name == tool.name:
                return False
        
        self.tools.append(tool)
        self._save_tools()
        return True
    
    def remove_tool(self, tool_name: str) -> bool:
        """Remove an AI tool by name."""
        initial_count = len(self.tools)
        self.tools = [tool for tool in self.tools if tool.name != tool_name]
        if len(self.tools) < initial_count:
            self._save_tools()
            return True
        return False
    
    def get_tool_by_name(self, tool_name: str) -> Optional[AITool]:
        """Get a specific AI tool by name."""
        for tool in self.tools:
            if tool.name == tool_name:
                return tool
        return None


def main():
    """Example usage of the single-click access system."""
    manager = SingleClickAccessManager()
    
    print("Available AI Tools:")
    for tool in manager.get_available_tools():
        status = "✓ Subscribed" if tool.is_subscribed else "○ Not subscribed"
        print(f"  {tool.name}: {tool.description} ({status})")
    
    # Example subscription management
    print("\nSubscribing to ChatGPT...")
    if manager.subscribe_to_tool("ChatGPT"):
        print("Successfully subscribed!")
    else:
        print("Failed to subscribe.")
    
    print("\nSubscribed Tools:")
    for tool in manager.get_subscribed_tools():
        print(f"  {tool.name}: {tool.url}")


if __name__ == "__main__":
    main()