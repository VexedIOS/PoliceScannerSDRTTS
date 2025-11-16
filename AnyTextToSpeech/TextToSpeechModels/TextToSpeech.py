from abc import abstractmethod, ABC
from typing import Any
import whisper
import os


class TextToSpeech(ABC):

    def __init__(self, audio_path):
        self.audio_path = audio_path
        self.text_data : Any = None

    @abstractmethod
    def get_text(self):
        # From split audio file not orginal
        pass



class WhisperTextToSpeechFast(TextToSpeech):
    def get_text(self):
        # Initiate Whisper API
        whisper_model = whisper.load_model("medium.en")
        if not os.path.exists(self.audio_path):
            print(f"Error: Audio file not found at '{self.audio_path}'.'")
            return None
        else:
            # Transcribe the audio
            # print(f"Transcribing '{audio_file_path}' using Whisper..")
            self.text_data = whisper_model.transcribe(self.audio_path)
            return self.text_data

class WhisperTextToSpeechBlazing(TextToSpeech):
    def get_text(self):
        # Initiate Whisper API
        whisper_model = whisper.load_model("small.en")
        if not os.path.exists(self.audio_path):
            print(f"Error: Audio file not found at '{self.audio_path}'.'")
            return None
        else:
            # Transcribe the audio
            # print(f"Transcribing '{audio_file_path}' using Whisper..")
            self.text_data = whisper_model.transcribe(self.audio_path, temperature=0)
            return self.text_data
