from transcription_accuracy_analyzer import TranscriptionAccuracyAnalyzer
import pandas as pd

class TranscriptionReporting:
    def __init__(self):
        self.analyzer = TranscriptionAccuracyAnalyzer()

    def generate_report(self, audio_files, reference_transcripts):
        accuracies = []
        for audio_file, reference_transcript in zip(audio_files, reference_transcripts):
            accuracy = self.analyzer.analyze_accuracy(audio_file, reference_transcript)
            accuracies.append(accuracy)

        report = pd.DataFrame({
            'Audio File': audio_files,
            'Reference Transcript': reference_transcripts,
            'Accuracy': accuracies
        })

        return report

    def save_report(self, report, file_path):
        report.to_csv(file_path, index=False)