import httpx
import asyncio
from typing import Dict, Any, Optional
from config import LLAMA_GATE_API_URL, LLAMA_GATE_API_KEY

class LlamaGateClient:
    """
    Safe API client for Llama-Gate playbook generation.
    Implements error handling, timeouts, and resource cleanup.
    """
    
    def __init__(self):
        self.base_url = LLAMA_GATE_API_URL
        self.api_key = LLAMA_GATE_API_KEY
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={"Authorization": f"Bearer {self.api_key}"},
            timeout=30.0  # Prevent hanging requests
        )

    async def generate_playbook(self, profile_data: Dict[str, Any]) -> str:
        """
        Generate a markdown playbook from profile data.
        
        Args:
            profile_data: Founder profile information
            
        Returns:
            Generated markdown playbook (≤800 words)
            
        Raises:
            httpx.HTTPError: For API failures
            ValueError: For invalid responses
        """
        try:
            response = await self.client.post(
                "/generate-playbook",
                json={"profile": profile_data},
                timeout=30.0
            )
            response.raise_for_status()
            
            playbook = response.json().get("playbook")
            if not playbook:
                raise ValueError("Empty playbook response")
            return playbook
            
        except httpx.HTTPStatusError as e:
            raise httpx.HTTPError(f"API error {e.response.status_code}: {e.response.text}")
        except (httpx.RequestError, ValueError) as e:
            raise httpx.HTTPError(f"Playbook generation failed: {str(e)}")

    async def close(self):
        """Safely close HTTP client connection"""
        await self.client.aclose()

# Synchronous wrapper for compatibility
def generate_playbook_sync(profile_data: Dict[str, Any]) -> str:
    """
    Thread-safe synchronous wrapper for playbook generation.
    
    Args:
        profile_data: Founder profile information
        
    Returns:
        Generated markdown playbook (≤800 words)
    """
    client = LlamaGateClient()
    try:
        return asyncio.run(client.generate_playbook(profile_data))
    finally:
        # Ensure cleanup even if errors occur
        asyncio.run(client.close())