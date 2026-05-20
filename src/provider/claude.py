from typing import Dict, Any, Optional
import anthropic
from .base import BaseProvider
from ..models import LLMResponse
from ..exceptions import ProviderError, RateLimitError

class ClaudeProvider(BaseProvider):
    """Claude provider implementation for the surrogate-1 SDK."""
    
    SUPPORTED_MODELS = ['claude-3-haiku', 'claude-3-sonnet', 'claude-3-opus']
    
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.client = anthropic.Anthropic(api_key=api_key)
    
    @property
    def provider_name(self) -> str:
        return 'claude'
    
    def generate(self, prompt: str, **kwargs) -> LLMResponse:
        model = kwargs.get('model', 'claude-3-haiku')
        
        if model not in self.SUPPORTED_MODELS:
            raise ValueError(f"Unsupported model: {model}. Choose from {self.SUPPORTED_MODELS}")
        
        params = {
            'model': model,
            'messages': [{"role": "user", "content": prompt}],
            'max_tokens': kwargs.get('max_tokens', 1000),
            'temperature': kwargs.get('temperature', 1.0),
            'top_p': kwargs.get('top_p', 1.0),
        }
        
        # Add optional parameters if provided
        if 'system' in kwargs:
            params['system'] = kwargs['system']
        if 'stop_sequences' in kwargs:
            params['stop_sequences'] = kwargs['stop_sequences']
        
        # Filter None values
        params = {k: v for k, v in params.items() if v is not None}
        
        try:
            response = self.client.messages.create(**params)
            
            # FIXED: Correct usage calculation
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens
            
            return LLMResponse(
                text=response.content[0].text if response.content else "",
                usage={
                    "prompt_tokens": input_tokens,
                    "completion_tokens": output_tokens,
                    "total_tokens": input_tokens + output_tokens  # Fixed calculation
                },
                finish_reason=response.stop_reason or 'unknown'
            )
            
        except anthropic.RateLimitError as e:
            raise RateLimitError(f"Claude rate limit exceeded: {str(e)}")
        except anthropic.APIConnectionError as e:
            raise ProviderError(f"Claude connection error: {str(e)}")
        except Exception as e:
            raise ProviderError(f"Claude API error: {str(e)}")