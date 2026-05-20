from llm_client import LLMClient, ProviderConfigError

try:
    client = LLMClient("openai")          # provider name must exist in JSON
    response = client.inference("Hello!") # will raise NotImplementedError now
except ProviderConfigError as e:
    # Configuration problem – log and abort early
    print(f"Configuration error: {e}")
except NotImplementedError as e:
    # Expected until you wire up the real SDK
    print(e)