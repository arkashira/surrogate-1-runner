import hashlib
from typing import List, Callable

class Orchestrator:
    def __init__(self, llm_providers: List[Callable]):
        self.llm_providers = sorted(llm_providers, key=lambda x: x.__name__)

    def execute_calls(self, requests: List[str]) -> List[str]:
        responses = []
        for request in requests:
            for provider in self.llm_providers:
                try:
                    response = provider(request)
                    responses.append(response)
                    break
                except Exception as e:
                    print(f"Retry failed with {provider.__name__}: {str(e)}")
        return responses

def deterministic_llm_call_provider(request: str) -> str:
    # Simulate an LLM call provider
    return hashlib.sha256(request.encode()).hexdigest()

if __name__ == "__main__":
    providers = [deterministic_llm_call_provider]
    orchestrator = Orchestrator(providers)
    requests = ["request1", "request2"]
    responses = orchestrator.execute_calls(requests)
    print(responses)