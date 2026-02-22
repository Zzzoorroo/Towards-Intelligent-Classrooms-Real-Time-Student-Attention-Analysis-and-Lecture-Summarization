import os
import whisper

class AudioTranscriber:
    def __init__(self, model_size="base"):
        """Loads the AI model into RAM."""
        print(f"Loading Whisper model ({model_size})...")
        self.model = whisper.load_model(model_size)

    def transcribe(self, audio_path, language="en"):
        """Reads a .wav file and returns the text."""
        if not os.path.exists(audio_path):
            return "Error: File not found."
            
        print(f"Transcribing {audio_path} (Forced Language: {language})...")
        result = self.model.transcribe(audio_path, language=language)
        return result["text"]