import torch
import whisper
from typing import Optional, Dict, Any
import numpy as np

class WhisperWrapper:
    def __init__(self, model_name: str = "base", device: str = "cpu"):
        self.model = whisper.load_model(model_name)
        self.device = device
        self.model.to(device)

    def transcribe_stream(self, audio_frames: np.ndarray) -> Dict[str, Any]:
        """
        Transcribe audio stream in chunks.

        Args:
            audio_frames: numpy array of audio frames (16 kHz PCM)

        Returns:
            Dictionary containing transcription results with 'text' and 'confidence' fields
        """
        # Convert numpy array to tensor
        audio_tensor = torch.from_numpy(audio_frames).to(self.device)

        # Process audio with Whisper
        result = self.model.transcribe(audio_tensor)

        # Format the result
        formatted_result = {
            "text": result["text"],
            "confidence": result.get("confidence", 0.0)
        }

        return formatted_result