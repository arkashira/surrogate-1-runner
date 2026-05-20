import requests
import logging
import time

class PCPartPickerClient:
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key
        self.logger = logging.getLogger(__name__)

    def get_components(self):
        """
        Fetches components from the PCPartPicker API.
        
        Returns:
            dict: JSON response containing components data.
            None: If the request fails.
        """
        try:
            response = requests.get(
                self.api_url + '/v1/components',
                headers={'Authorization': f'Bearer {self.api_key}'}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f'Failed to fetch components: {e}')
            return None

    def get_components_with_retry(self, max_retries=5, initial_delay=1):
        """
        Fetches components with exponential backoff on failure.
        
        Args:
            max_retries (int): Maximum number of retry attempts.
            initial_delay (int): Initial delay between retries in seconds.
            
        Returns:
            dict: JSON response containing components data.
            None: If all retries fail.
        """
        delay = initial_delay
        for attempt in range(max_retries):
            try:
                return self.get_components()
            except requests.exceptions.RequestException as e:
                self.logger.error(f'Failed to fetch components (attempt {attempt+1}/{max_retries}): {e}')
                if attempt < max_retries - 1:
                    time.sleep(delay)
                    delay *= 2
        self.logger.error(f'Failed to fetch components after {max_retries} retries')
        return None

# /opt/axentx/surrogate-1/src/data/__init__.py
from .pcpartpicker_client import PCPartPickerClient

def get_pcpartpicker_client(api_url, api_key):
    """
    Factory function to create an instance of PCPartPickerClient.
    
    Args:
        api_url (str): The base URL of the PCPartPicker API.
        api_key (str): The API key for authentication.
        
    Returns:
        PCPartPickerClient: An instance of the PCPartPickerClient class.
    """
    return PCPartPickerClient(api_url, api_key)