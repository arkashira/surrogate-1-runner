from transcription_settings import TranscriptionSettings

class UI:
    def __init__(self, transcription_settings: TranscriptionSettings):
        self.transcription_settings = transcription_settings

    def render_audio_gain_control_status(self):
        if self.transcription_settings.is_audio_gain_control_active():
            print("Microphone boost is active.")
        else:
            print("Microphone boost is inactive.")

    def handle_toggle_audio_gain_control(self):
        current_state = self.transcription_settings.is_audio_gain_control_active()
        self.transcription_settings.toggle_audio_gain_control(not current_state)
        self.render_audio_gain_control_status()