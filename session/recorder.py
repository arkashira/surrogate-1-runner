import os
import wave
import pyaudio
import threading
from cryptography.fernet import Fernet

class SessionRecorder:
    def __init__(self, encryption_key: bytes, output_file: str):
        """
        Initialize the SessionRecorder with encryption key and output file path.
        
        Args:
            encryption_key (bytes): The Fernet encryption key for securing recordings.
            output_file (str): Path where the recorded audio will be saved.
        """
        self.encryption_key = encryption_key
        self.output_file = output_file
        self.recording = False
        self.frames = []
        self.audio = pyaudio.PyAudio()

    def start_recording(self):
        """
        Starts recording audio in a separate thread to allow non-blocking operation.
        """
        if self.recording:
            raise RuntimeError("Recording is already in progress.")

        self.recording = True
        self.frames = []
        self.thread = threading.Thread(target=self._record)
        self.thread.daemon = True  # Allows program to exit even if thread is running
        self.thread.start()

    def _record(self):
        """
        Internal method to handle actual audio recording loop.
        """
        try:
            stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=2,
                rate=44100,
                input=True,
                frames_per_buffer=1024
            )
        except Exception as e:
            print(f"Error opening audio stream: {e}")
            return

        while self.recording:
            try:
                data = stream.read(1024)
                self.frames.append(data)
            except Exception as e:
                print(f"Error reading audio data: {e}")
                break

        stream.stop_stream()
        stream.close()

    def stop_recording(self):
        """
        Stops the recording and saves the file with encryption.
        """
        if not self.recording:
            raise RuntimeError("No active recording to stop.")

        self.recording = False
        self.audio.terminate()
        self._save_recording()

    def _save_recording(self):
        """
        Saves the raw audio frames to a WAV file and then encrypts it.
        """
        try:
            with wave.open(self.output_file, 'wb') as wf:
                wf.setnchannels(2)
                wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
                wf.setframerate(44100)
                wf.writeframes(b''.join(self.frames))

            self._encrypt_recording()
        except Exception as e:
            print(f"Error saving or encrypting recording: {e}")

    def _encrypt_recording(self):
        """
        Encrypts the saved WAV file using Fernet encryption.
        """
        try:
            fernet = Fernet(self.encryption_key)
            with open(self.output_file, 'rb') as file:
                original = file.read()
            encrypted = fernet.encrypt(original)
            with open(self.output_file, 'wb') as encrypted_file:
                encrypted_file.write(encrypted)
        except Exception as e:
            print(f"Error during encryption: {e}")

    def replay_recording(self, speed: float = 1.0):
        """
        Plays back the encrypted recording at specified playback speed.
        
        Args:
            speed (float): Playback speed multiplier (default is 1.0).
        """
        try:
            with wave.open(self.output_file, 'rb') as wf:
                p = pyaudio.PyAudio()
                stream = p.open(
                    format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=int(wf.getframerate() * speed),
                    output=True
                )

                data = wf.readframes(1024)
                while data:
                    stream.write(data)
                    data = wf.readframes(1024)

                stream.stop_stream()
                stream.close()
                p.terminate()
        except Exception as e:
            print(f"Error during playback: {e}")

# Example usage:
if __name__ == "__main__":
    key = Fernet.generate_key()
    recorder = SessionRecorder(key, 'session_recording.wav')
    
    print("Starting recording...")
    recorder.start_recording()
    
    try:
        input("Press Enter to stop recording...\n")
    except KeyboardInterrupt:
        pass
    
    print("Stopping recording...")
    recorder.stop_recording()
    
    print("Replaying recording at 1.5x speed...")
    recorder.replay_recording(speed=1.5)