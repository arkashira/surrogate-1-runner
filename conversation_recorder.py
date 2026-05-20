import os
import wave
import pyaudio

class ConversationRecorder:
    def __init__(self, filename="conversation.wav"):
        self.filename = filename
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100
        self.chunk = 1024
        self.frames = []

    def start_recording(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=self.format, channels=self.channels,
                            rate=self.rate, input=True,
                            frames_per_buffer=self.chunk)

        print("Recording...")

        while True:
            data = stream.read(self.chunk)
            self.frames.append(data)

    def stop_recording(self):
        print("Finished recording.")
        audio = pyaudio.PyAudio()
        stream = audio.open(format=self.format, channels=self.channels,
                            rate=self.rate, input=True,
                            frames_per_buffer=self.chunk)
        stream.stop_stream()
        stream.close()
        audio.terminate()

        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(audio.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(self.frames))
        wf.close()

    def get_filename(self):
        return self.filename