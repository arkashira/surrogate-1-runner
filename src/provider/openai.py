from typing import Dict, Any, Optional
import openai
from .base import BaseProvider
from ..models import LLMResponse
from ..exceptions import ProviderError, RateLimitError

class OpenAIProvider(BaseProvider):
    """OpenAI provider implementation for the surrogate-1 SDK."""
    
    SUPPORTED_MODELS = ['gpt-4', 'gpt-4-turbo', 'gpt-3.5-turbo']
    
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.client = openai.OpenAI(api_key=api_key)
    
    @property
    def provider_name(self) -> str:
        return 'openai'
    
    def generate(self, prompt: str, **kwargs) -> LLMResponse:
        model = kwargs.get('model', 'gpt-3.5-turbo')
        
        if model not in self.SUPPORTED_MODELS:
            raise ValueError(f"Unsupported model: {model}")
        
        params = {
            'model': model,
            'messages': [{"role": "user", "content": prompt}],
            'max_tokens': kwargs.get('max_tokens', 1000),
            'temperature': kwargs.get('temperature', 1.0),
        }
        
        # Add optional parameters
        for key in ['top_p', 'frequency_penalty', 'presence_penalty', 'stop']:
            if key in kwargs:
                params[key] = kwargs[key]
        
        params = {k: v for k, v in params.items() if v is not None}
        
        try:
            response = self.client.chat.completions.create(**params)
            
            choice = response.choices[0]
            usage = response.usage
            
            return LLMResponse(
                text=choice.message.content or "",
                usage={
                    "prompt_tokens": usage.prompt_tokens,
                    "completion_tokens": usage.completion_tokens,
                    "total_tokens": usage.total_tokens
                },
                finish_reason=choice.finish_reason or 'unknown'
            )
            
        except openai.RateLimitError as e:
            raise RateLimitError(f"OpenAI rate limit exceeded: {str(e)}")
        except Exception as e:
            raise ProviderError(f"OpenAI API error: {str(e)}")