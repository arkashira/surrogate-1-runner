
import os
import json
from axentx.core.config import Config
from axentx.core.utils import load_json_file, save_json_file

class SubscriptionManager:
    def __init__(self):
        self.config = Config()
        self.subscriptions_file = self.config.get('subscriptions_file', 'subscriptions.json')

    def load_subscriptions(self):
        if os.path.exists(self.subscriptions_file):
            return load_json_file(self.subscriptions_file)
        return {}

    def save_subscriptions(self, subscriptions):
        save_json_file(self.subscriptions_file, subscriptions)

    def subscribe(self, tool_id):
        subscriptions = self.load_subscriptions()
        if tool_id not in subscriptions:
            subscriptions[tool_id] = True
            self.save_subscriptions(subscriptions)
            return True
        return False

    def unsubscribe(self, tool_id):
        subscriptions = self.load_subscriptions()
        if tool_id in subscriptions:
            del subscriptions[tool_id]
            self.save_subscriptions(subscriptions)
            return True
        return False

    def is_subscribed(self, tool_id):
        subscriptions = self.load_subscriptions()
        return tool_id in subscriptions

# opt/axentx/surrogate-1/src/tools.py

from axentx.core.config import Config
from axentx.core.utils import load_json_file
from subscription_management import SubscriptionManager

class Tool:
    def __init__(self, tool_id, tool_data):
        self.tool_id = tool_id
        self.tool_data = tool_data
        self.subscription_manager = SubscriptionManager()

    def is_subscribed(self):
        return self.subscription_manager.is_subscribed(self.tool_id)

# opt/axentx/surrogate-1/src/ui.py

# ... (other UI code)

def display_tools(tools):
    for tool in tools:
        if tool.is_subscribed():
            button_text = "Unsubscribe"
        else:
            button_text = "Subscribe"
        button_id = f"{tool.tool_id}-button"
        ui.append(
            ui.button(
                id=button_id,
                children=button_text,
                on_click=lambda event, tool=tool: handle_tool_subscription(event, tool)
            )
        )

def handle_tool_subscription(event, tool):
    if tool.is_subscribed():
        tool.subscription_manager.unsubscribe(tool.tool_id)
    else:
        tool.subscription_manager.subscribe(tool.tool_id)
    display_tools(tools)

## Summary
- Implemented `SubscriptionManager` class to handle subscriptions.
- Added subscription methods to `Tool` class.
- Updated UI to display subscription status and handle subscription changes.
- Added a short summary of changes made to address the task.