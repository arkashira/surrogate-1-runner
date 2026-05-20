from typing import Optional

class ConfigSchema:
    def __init__(self, audio_gain_control_enabled: bool = False, audio_gain_boost_level: float = 1.0):
        self.audio_gain_control_enabled = audio_gain_control_enabled
        self.audio_gain_boost_level = audio_gain_boost_level

    def to_dict(self):
        return {
            'audio_gain_control_enabled': self.audio_gain_control_enabled,
            'audio_gain_boost_level': self.audio_gain_boost_level
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            audio_gain_control_enabled=data.get('audio_gain_control_enabled', False),
            audio_gain_boost_level=data.get('audio_gain_boost_level', 1.0)
        )