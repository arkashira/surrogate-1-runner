import random
from typing import List

class Provider:
    def __init__(self, name: str):
        self.name = name
        self.available = True

    def process_request(self, request: str) -> str:
        if not self.available:
            raise Exception(f"Provider {self.name} is unavailable.")
        return f"Processed by {self.name}: {request}"

class Orchestrator:
    def __init__(self, providers: List[Provider]):
        self.providers = providers

    def _select_provider(self) -> Provider:
        available_providers = [p for p in self.providers if p.available]
        if not available_providers:
            raise Exception("No available providers.")
        return random.choice(available_providers)

    def process_request(self, request: str) -> str:
        try:
            provider = self._select_provider()
            return provider.process_request(request)
        except Exception as e:
            print(f"Error processing request: {e}")
            # Failover logic: Mark the current provider as unavailable and retry
            provider.available = False
            return self.process_request(request)

    def load_balance_requests(self, requests: List[str]) -> List[str]:
        results = []
        for request in requests:
            result = self.process_request(request)
            results.append(result)
        return results

# Example usage
if __name__ == "__main__":
    providers = [
        Provider("ProviderA"),
        Provider("ProviderB"),
        Provider("ProviderC")
    ]
    orchestrator = Orchestrator(providers)
    requests = ["Request1", "Request2", "Request3"]
    responses = orchestrator.load_balance_requests(requests)
    for response in responses:
        print(response)