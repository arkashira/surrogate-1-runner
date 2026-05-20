import speech_recognition as sr

class TranscriptionService:
    def __init__(self, audio_file):
        self.audio_file = audio_file

    def transcribe_audio(self):
        recognizer = sr.Recognizer()
        with sr.AudioFile(self.audio_file) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            return text

    def save_transcription(self, transcription, filename="transcription.txt"):
        with open(filename, 'w') as file:
            file.write(transcription)
        return filename