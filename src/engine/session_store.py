import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class SessionStore:
    def __init__(self):
        self.sessions: Dict[str, Dict] = {}
        self.native_speakers: Dict[str, bool] = {}  # speaker_id -> availability status

    def create_session(self, user_id: str, native_speaker_id: str) -> str:
        """Create a new session and return session ID"""
        if not self.native_speakers.get(native_speaker_id, False):
            raise ValueError(f"Native speaker {native_speaker_id} is not available")
        
        session_id = str(uuid.uuid4())
        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=15)
        
        session = {
            "session_id": session_id,
            "user_id": user_id,
            "native_speaker_id": native_speaker_id,
            "start_time": start_time,
            "end_time": end_time,
            "status": "active",
            "recording_url": None
        }
        
        self.sessions[session_id] = session
        self.native_speakers[native_speaker_id] = False  # Mark as busy
        return session_id

    def get_session(self, session_id: str) -> Optional[Dict]:
        """Retrieve session by ID"""
        return self.sessions.get(session_id)

    def get_available_native_speakers(self) -> List[str]:
        """Get list of available native speaker IDs"""
        return [speaker_id for speaker_id, available in self.native_speakers.items() if available]

    def end_session(self, session_id: str) -> bool:
        """End a session and mark speaker as available"""
        session = self.sessions.get(session_id)
        if not session or session["status"] != "active":
            return False
        
        session["status"] = "completed"
        session["end_time"] = datetime.now()
        self.native_speakers[session["native_speaker_id"]] = True
        return True

    def add_native_speaker(self, speaker_id: str):
        """Add a new native speaker to the pool"""
        self.native_speakers[speaker_id] = True

    def get_user_sessions(self, user_id: str) -> List[Dict]:
        """Get all sessions for a specific user"""
        return [session for session in self.sessions.values() if session["user_id"] == user_id]

    def log_session_data(self, session_id: str, recording_url: str):
        """Attach recording URL to session"""
        if session_id in self.sessions:
            self.sessions[session_id]["recording_url"] = recording_url