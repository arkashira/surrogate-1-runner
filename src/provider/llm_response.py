from dataclasses import dataclass, asdict
from typing import Dict, Any

@dataclass
class LLMResponse:
    """
    Standardised response object for all LLM providers.
    
    Attributes:
        text (str): The generated text from the LLM.
        usage (Dict[str, Any]): Token usage statistics (e.g., prompt_tokens, completion_tokens).
        finish_reason (str): Reason the LLM stopped generating (e.g., "stop", "length").
    """
    text: str
    usage: Dict[str, Any]
    finish_reason: str

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the LLMResponse to a JSON-serialisable dictionary.
        """
        return asdict(self)