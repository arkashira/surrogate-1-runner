import os
import logging
from typing import Optional, Dict, Any, Tuple
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class LLMProviderError(Exception):
    """Base exception for LLM provider errors with meaningful messages."""
    def __init__(self, message: str, provider: Optional[str] = None, context: Optional[Dict[str, Any]] = None):
        self.provider = provider
        self.context = context or {}
        super().__init__(message)


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    @abstractmethod
    def create_client(self, **kwargs) -> Any:
        """Create and return an LLM client instance."""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> Dict[str, Any]:
        """Return provider capabilities and configuration."""
        pass


class SurrogateProvider(LLMProvider):
    """Default surrogate LLM provider implementation."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.name = "surrogate-default"
    
    def create_client(self, **kwargs) -> Any:
        """Create surrogate LLM client."""
        logger.info(f"Creating surrogate LLM client with config: {self.config}")
        # Implementation would create actual client
        return {"client": "surrogate", "config": self.config}
    
    def get_capabilities(self) -> Dict[str, Any]:
        return {
            "provider": self.name,
            "supports_streaming": True,
            "supports_function_calling": True,
            "max_tokens": 4096
        }


class IDEProvider(LLMProvider):
    """IDE-specific LLM provider implementation."""
    
    def __init__(self, config: Dict[str, Any], provider_id: str):
        self.config = config
        self.provider_id = provider_id
        self.name = f"surrogate-{provider_id}"
    
    def create_client(self, **kwargs) -> Any:
        """Create IDE-specific LLM client."""
        logger.info(f"Creating IDE LLM client (provider={self.provider_id}) with config: {self.config}")
        # Implementation would create actual client
        return {"client": "surrogate-ide", "provider_id": self.provider_id, "config": self.config}
    
    def get_capabilities(self) -> Dict[str, Any]:
        return {
            "provider": self.name,
            "supports_streaming": True,
            "supports_function_calling": True,
            "max_tokens": 8192
        }


class LLMClient:
    """Main LLM client that routes through provider selection logic."""
    
    DEFAULT_PROVIDER = "surrogate-default"
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self._provider: Optional[LLMProvider] = None
        self._initialize_provider()
    
    def _initialize_provider(self) -> None:
        """Initialize provider based on environment and config."""
        # Check for IDE-specific provider first
        ide_provider_env = os.environ.get("SURROGATE_IDE_PROVIDER")
        
        if ide_provider_env:
            logger.info(f"Using IDE-specific provider from env: {ide_provider_env}")
            provider_config = self.config.get("providers", {}).get(ide_provider_env, {})
            self._provider = IDEProvider(provider_config, ide_provider_env)
        else:
            # Fall back to default provider
            logger.info(f"Using default provider: {self.DEFAULT_PROVIDER}")
            provider_config = self.config.get("providers", {}).get(self.DEFAULT_PROVIDER, {})
            self._provider = SurrogateProvider(provider_config)
        
        if self._provider is None:
            raise LLMProviderError(
                f"No valid provider configured for IDE context",
                provider=None,
                context={"env_var": "SURROGATE_IDE_PROVIDER", "value": ide_provider_env}
            )
    
    @property
    def provider(self) -> LLMProvider:
        """Get the current provider instance."""
        if self._provider is None:
            self._initialize_provider()
        return self._provider
    
    def create_client(self, **kwargs) -> Any:
        """Create LLM client through the selected provider."""
        try:
            return self.provider.create_client(**kwargs)
        except Exception as e:
            raise LLMProviderError(
                f"Failed to create LLM client: {str(e)}",
                provider=self.provider.name,
                context=kwargs
            )
    
    def get_capabilities(self) -> Dict[str, Any]:
        """Get capabilities from the selected provider."""
        try:
            return self.provider.get_capabilities()
        except Exception as e:
            raise LLMProviderError(
                f"Failed to get provider capabilities: {str(e)}",
                provider=self.provider.name,
                context={"error_type": type(e).__name__}
            )
    
    def execute_request(self, prompt: str, **kwargs) -> Tuple[Dict[str, Any], Optional[str]]:
        """Execute a request and return response with error handling."""
        try:
            client = self.create_client(**kwargs)
            response = client["response"]
            return response, None
        except LLMProviderError as e:
            return {"error": str(e)}, e.provider
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}, self.provider.name


def get_llm_client(config: Optional[Dict[str, Any]] = None) -> LLMClient:
    """Factory function to create LLM client with proper provider selection."""
    return LLMClient(config)