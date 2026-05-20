from config.config_schema import ConfigSchema

class TranscriptionSettings:
    def __init__(self, config: ConfigSchema):
        self.config = config

    def toggle_audio_gain_control(self, enabled: bool):
        self.config.audio_gain_control_enabled = enabled

    def apply_audio_gain_boost(self, audio_input):
        if self.config.audio_gain_control_enabled:
            return audio_input * self.config.audio_gain_boost_level
        return audio_input

    def is_audio_gain_control_active(self):
        return self.config.audio_gain_control_enabled