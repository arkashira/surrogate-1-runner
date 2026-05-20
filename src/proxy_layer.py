from typing import Dict
from token_counter import TokenCounter

class ProxyLayer:
    def __init__(self, model_name: str):
        self.token_counter = TokenCounter(model_name)

    def process_request(self, request: Dict) -> Dict:
        """Process the API request and return the response with token usage and cost."""
        text = request.get("text", "")
        input_tokens, output_tokens = self.token_counter.count_tokens(text)
        cost = self.token_counter.get_cost(input_tokens, output_tokens)

        response = {
            "response": "Processed successfully",  # Placeholder for actual response
            "token_usage": {
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cost": cost
            }
        }
        return response

    def start_monitoring(self, text: str, interval: int = 15):
        """Start monitoring token usage and API costs at regular intervals."""
        for data in self.token_counter.monitor_token_usage(text, interval):
            print(data)