import time
import requests
from typing import Optional, Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ZoomSessionDetector:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://api.zoom.us/v2"
        self._token_cache = None
        self._token_expiry = 0

    def _get_access_token(self) -> str:
        """Get or refresh access token for Zoom API"""
        current_time = int(time.time())
        if self._token_cache and current_time < self._token_expiry:
            return self._token_cache
            
        # Generate JWT token
        import jwt
        payload = {
            'iss': self.api_key,
            'exp': current_time + 3600  # 1 hour expiry
        }
        token = jwt.encode(payload, self.api_secret)
        
        self._token_cache = token
        self._token_expiry = current_time + 3000  # Refresh after 50 minutes
        
        return token

    def _make_api_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict[Any, Any]:
        """Make authenticated request to Zoom API"""
        try:
            headers = {
                'Authorization': f'Bearer {self._get_access_token()}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(
                f"{self.base_url}/{endpoint}",
                headers=headers,
                params=params or {}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Zoom API error: {e}")
            return {}

    def get_active_meetings(self) -> list:
        """Detect currently active meetings for the user"""
        try:
            # Get meetings for current user
            data = self._make_api_request("users/me/meetings", {"type": "live"})
            
            meetings = []
            if 'meetings' in data:
                for meeting in data['meetings']:
                    if meeting.get('status') == 'started':
                        meetings.append({
                            'id': meeting.get('id'),
                            'topic': meeting.get('topic'),
                            'start_time': meeting.get('start_time'),
                            'meeting_type': meeting.get('type')
                        })
            
            return meetings
        except Exception as e:
            logger.error(f"Error detecting Zoom meetings: {e}")
            return []

    def is_in_meeting(self) -> bool:
        """Check if user is currently in a Zoom meeting"""
        meetings = self.get_active_meetings()
        return len(meetings) > 0

    def get_current_meeting_info(self) -> Optional[Dict]:
        """Get information about the current active meeting"""
        meetings = self.get_active_meetings()
        if meetings:
            return meetings[0]
        return None

    def monitor_meetings(self, callback_func):
        """Continuously monitor for meeting start/end events"""
        last_state = False
        while True:
            try:
                current_state = self.is_in_meeting()
                
                if not last_state and current_state:
                    # Meeting started
                    meeting_info = self.get_current_meeting_info()
                    logger.info(f"Zoom meeting started: {meeting_info}")
                    callback_func("meeting_started", meeting_info)
                    
                elif last_state and not current_state:
                    # Meeting ended
                    logger.info("Zoom meeting ended")
                    callback_func("meeting_ended", None)
                    
                last_state = current_state
                time.sleep(10)  # Check every 10 seconds
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(f"Error in Zoom monitoring: {e}")
                time.sleep(10)