import numpy as np
from sklearn.metrics import accuracy_score
from audio_processing import AudioProcessor
from transcription import TranscriptionEngine

class TranscriptionAccuracyAnalyzer:
    def __init__(self):
        self.audio_processor = AudioProcessor()
        self.transcription_engine = TranscriptionEngine()

    def analyze_accuracy(self, audio_file_path, reference_transcript):
        # Process audio with gain control
        processed_audio = self.audio_processor.process_audio(audio_file_path, gain_control=True)

        # Generate transcript
        generated_transcript = self.transcription_engine.transcribe(processed_audio)

        # Calculate accuracy
        accuracy = self._calculate_accuracy(generated_transcript, reference_transcript)

        return accuracy

    def _calculate_accuracy(self, generated_transcript, reference_transcript):
        # Tokenize transcripts
        generated_tokens = generated_transcript.split()
        reference_tokens = reference_transcript.split()

        # Calculate accuracy
        accuracy = accuracy_score(reference_tokens, generated_tokens)

        return accuracy