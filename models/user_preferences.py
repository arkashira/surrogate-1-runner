from dataclasses import dataclass
from typing import Optional, List
import json

@dataclass
class UserPreferences:
    """Data class representing user learning preferences"""
    user_id: str
    preferred_languages: List[str]
    learning_goals: List[str]
    daily_goal_minutes: int
    notification_preferences: dict
    theme: str
    auto_play_audio: bool
    show_translations: bool
    
    def to_dict(self) -> dict:
        """Convert to dictionary for database storage"""
        return {
            'user_id': self.user_id,
            'preferred_languages': self.preferred_languages,
            'learning_goals': self.learning_goals,
            'daily_goal_minutes': self.daily_goal_minutes,
            'notification_preferences': self.notification_preferences,
            'theme': self.theme,
            'auto_play_audio': self.auto_play_audio,
            'show_translations': self.show_translations
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create instance from dictionary"""
        return cls(
            user_id=data['user_id'],
            preferred_languages=data.get('preferred_languages', []),
            learning_goals=data.get('learning_goals', []),
            daily_goal_minutes=data.get('daily_goal_minutes', 30),
            notification_preferences=data.get('notification_preferences', {}),
            theme=data.get('theme', 'light'),
            auto_play_audio=data.get('auto_play_audio', True),
            show_translations=data.get('show_translations', True)
        )

class UserPreferencesManager:
    """Manages user preference operations"""
    
    def __init__(self, db_connection):
        self.db = db_connection
    
    def get_preferences(self, user_id: str) -> Optional[UserPreferences]:
        """Retrieve user preferences from database"""
        try:
            result = self.db.execute(
                "SELECT preferences FROM user_preferences WHERE user_id = ?",
                (user_id,)
            ).fetchone()
            
            if result:
                prefs_data = json.loads(result[0])
                return UserPreferences.from_dict(prefs_data)
            return None
        except Exception:
            return None
    
    def save_preferences(self, preferences: UserPreferences) -> bool:
        """Save user preferences to database"""
        try:
            prefs_json = json.dumps(preferences.to_dict())
            self.db.execute(
                """
                INSERT OR REPLACE INTO user_preferences 
                (user_id, preferences) VALUES (?, ?)
                """,
                (preferences.user_id, prefs_json)
            )
            self.db.commit()
            return True
        except Exception:
            return False