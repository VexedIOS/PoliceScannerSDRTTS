from abc import ABC, abstractmethod
import ffmpeg
from df.enhance import enhance, init_df, load_audio, save_audio
import os

class Filter(ABC):
    def __init__(self, raw_audio_path, output_path=None):
        self.raw_audio_path = raw_audio_path
        self.output_path = output_path

    @abstractmethod
    def filter_audio(self):
        pass




class ReduceNoiseFilter(Filter):
    def filter_audio(self):
        pass
