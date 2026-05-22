
from typing import Dict, Any

class TradingBotAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_trades(self) -> Dict[str, Any]:
        # Implement the logic to fetch trades from the API using the provided API key
        pass

class BotAPIs:
    def __init__(self):
        self.apis = {
            "bot_name_1": TradingBotAPI("api_key_1"),
            "bot_name_2": TradingBotAPI("api_key_2"),
            # Add more APIs as needed
        }

    def get_trades(self, bot_name: str) -> Dict[str, Any]:
        return self.apis[bot_name].get_trades()