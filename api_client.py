
import requests
import os
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class AxentxApiClient:
    BASE_URL = os.environ.get('AXENTX_API_URL', "https://api.axentx.com")
    
    def __init__(self, api_key: Optional[str] = None):
        self.session = requests.Session()
        self.api_key = api_key or os.environ.get('AXENTX_API_KEY')
        if self.api_key:
            self.session.headers.update({'Authorization': f'Bearer {self.api_key}'})
    
    def get_signature_drift_detections(
        self, 
        page: int = 1, 
        per_page: int = 25,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Fetch signature drift detections with pagination support."""
        try:
            params = {'page': page, 'per_page': per_page}
            if limit:
                params['limit'] = limit
                
            response = self.session.get(
                f"{self.BASE_URL}/v1/signature-drift-detections",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json().get('detections', [])
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise