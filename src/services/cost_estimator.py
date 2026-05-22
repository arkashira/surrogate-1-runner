from typing import Dict, Optional
from transformers import AutoTokenizer

class CostEstimator:
    def __init__(self, model_name: str):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.cost_per_token: Dict[str, float] = {
            "gpt-3.5-turbo": 0.0000015,
            "gpt-4": 0.00003,
            "text-davinci-003": 0.00002,
        }

    def estimate_cost(self, prompt: str, model_name: str) -> Optional[float]:
        if model_name not in self.cost_per_token:
            return None

        tokens = self.tokenizer.encode(prompt)
        num_tokens = len(tokens)
        cost = num_tokens * self.cost_per_token[model_name]
        return cost