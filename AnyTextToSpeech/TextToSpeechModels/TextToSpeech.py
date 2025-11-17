from abc import abstractmethod, ABC
from typing import Any


class TextToSpeech(ABC):

    def __init__(self, audio_path):
        self.audio_path = audio_path
        self.text_data : Any = None

    @abstractmethod
    def get_text(self):
        # From split audio file not orginal
        pass

