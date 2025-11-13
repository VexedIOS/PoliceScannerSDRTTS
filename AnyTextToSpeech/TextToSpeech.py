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

class WhisperAPITextToSpeech(TextToSpeech):
    def get_text(self):
        # Initiate Whisper API
        whisper_model = whisper.load_model("large-v3-turbo")
        if not os.path.exists(self.audio_path):
            print(f"Error: Audio file not found at '{self.audio_path}'.'")
            return None
        else:
            # Transcribe the audio
            # print(f"Transcribing '{audio_file_path}' using Whisper..")
            self.text_data = whisper_model.transcribe(self.audio_path)
            return self.text_data
        # run and get text

#wapi=WhisperAPITextToSpeech("/home/vexed/PycharmProjects/PoliceScannerSDR/data/processed/20251111_190803Cities_Fresno_PoliceNorthEast__TO_4/20251111_190803Cities_Fresno_PoliceNorthEast__TO_4.mp3_0.8_7.7.wav")
#a =wapi.get_text()
#print(a)
#print(wapi.text_data['text'])
