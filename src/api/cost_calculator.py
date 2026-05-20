"""
Cost calculator module for real-time token usage and API cost estimation.

This module provides utilities to calculate the cost of an API call based on
the number of tokens processed and the per-token pricing for a given LLM
model. It also exposes a simple helper to aggregate costs across multiple
calls, which can be used by dashboard components.

The pricing data is expected to be supplied as a dictionary mapping model
names to a tuple of (input_price_per_token, output_price_per_token).  The
module is intentionally lightweight and does not depend on external services,
making it suitable for unit testing and real‑time usage in a dashboard.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple, Iterable, List


@dataclass(frozen=True)
class TokenUsage:
    """Represents token usage for a single API call."""
    model: str
    input_tokens: int
    output_tokens: int


class CostCalculator:
    """
    Calculates the cost of API calls based on token usage and model pricing.

    Pricing data should be provided as a mapping from model name to a tuple
    of (input_price_per_token, output_price_per_token).  Prices are in
    USD per token.  If a model is not present in the pricing map, a
    default price of $0.0 is used for both input and output tokens.
    """

    def __init__(self, pricing: Dict[str, Tuple[float, float]], default_price: float = 0.0) -> None:
        self.pricing = pricing
        self.default_price = default_price

    def calculate_call_cost(self, usage: TokenUsage) -> float:
        """
        Calculate the cost for a single API call.

        Args:
            usage: TokenUsage instance containing model name and token counts.

        Returns:
            The cost in USD as a float rounded to 8 decimal places.
        """
        input_price, output_price = self.pricing.get(usage.model, (self.default_price, self.default_price))
        cost = (usage.input_tokens * input_price) + (usage.output_tokens * output_price)
        return round(cost, 8)

    def aggregate_costs(self, usages: Iterable[TokenUsage]) -> float:
        """
        Aggregate costs across multiple API calls.

        Args:
            usages: Iterable of TokenUsage instances.

        Returns:
            Total cost in USD as a float rounded to 8 decimal places.
        """
        return round(sum(self.calculate_call_cost(u) for u in usages), 8)

    def format_cost(self, cost: float) -> str:
        """
        Format the cost as a USD string.

        Args:
            cost: Cost in USD.

        Returns:
            Formatted string, e.g., "$0.00123456".
        """
        return f"${cost:,.8f}"


# Example usage (for debugging or quick manual tests)
if __name__ == "__main__":
    # Sample pricing: model -> (input_price_per_token, output_price_per_token)
    sample_pricing = {
        "gpt-4o-mini": (0.0000005, 0.0000015),
        "gpt-4o": (0.000003, 0.000006),
    }

    calculator = CostCalculator(sample_pricing, default_price=0.00001)

    # Simulate a batch of calls
    calls = [
        TokenUsage(model="gpt-4o-mini", input_tokens=1200, output_tokens=300),
        TokenUsage(model="gpt-4o", input_tokens=800, output_tokens=200),
        TokenUsage(model="unknown-model", input_tokens=500, output_tokens=100),
    ]

    for call in calls:
        cost = calculator.calculate_call_cost(call)
        print(f"Call {call.model}: {calculator.format_cost(cost)}")

    total_cost = calculator.aggregate_costs(calls)
    print(f"Total cost: {calculator.format_cost(total_cost)}")