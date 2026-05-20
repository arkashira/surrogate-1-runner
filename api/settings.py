from flask import Blueprint, request, jsonify
from models.user_preferences import UserPreferences, UserPreferencesManager
import json

settings_bp = Blueprint('settings', __name__)

def get_db():
    # This would typically be your database connection manager
    # For now we'll simulate it
    pass

@settings_bp.route('/api/preferences', methods=['GET'])
def get_user_preferences():
    """Get current user preferences"""
    user_id = request.headers.get('user-id')
    if not user_id:
        return jsonify({'error': 'User ID required'}), 400
    
    prefs_manager = UserPreferencesManager(get_db())
    preferences = prefs_manager.get_preferences(user_id)
    
    if preferences:
        return jsonify(preferences.to_dict())
    else:
        # Return default preferences
        default_prefs = UserPreferences(
            user_id=user_id,
            preferred_languages=[],
            learning_goals=[],
            daily_goal_minutes=30,
            notification_preferences={},
            theme='light',
            auto_play_audio=True,
            show_translations=True
        )
        return jsonify(default_prefs.to_dict())

@settings_bp.route('/api/preferences', methods=['POST'])
def update_user_preferences():
    """Update user preferences"""
    user_id = request.headers.get('user-id')
    if not user_id:
        return jsonify({'error': 'User ID required'}), 400
    
    try:
        data = request.get_json()
        preferences = UserPreferences(
            user_id=user_id,
            preferred_languages=data.get('preferred_languages', []),
            learning_goals=data.get('learning_goals', []),
            daily_goal_minutes=data.get('daily_goal_minutes', 30),
            notification_preferences=data.get('notification_preferences', {}),
            theme=data.get('theme', 'light'),
            auto_play_audio=data.get('auto_play_audio', True),
            show_translations=data.get('show_translations', True)
        )
        
        prefs_manager = UserPreferencesManager(get_db())
        success = prefs_manager.save_preferences(preferences)
        
        if success:
            return jsonify({'message': 'Preferences updated successfully'})
        else:
            return jsonify({'error': 'Failed to update preferences'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Invalid request data: {str(e)}'}), 400