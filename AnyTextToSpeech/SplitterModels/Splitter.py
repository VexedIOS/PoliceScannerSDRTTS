from abc import ABC, abstractmethod
from typing import List, Dict, Union
import os

class Splitter(ABC):

    def __init__(self, raw_audio_path: Union[os.PathLike,str], output_path: Union[os.PathLike,str]):
        self.raw_audio_path = raw_audio_path
        self.output_path = output_path
        self.audio_created = []

    @abstractmethod
    def split_locator(self) -> Union[List[Dict[str,int]],None]: # return None or List of tupples
        pass

    @abstractmethod
    def split_video(self, split_locations: Union[List[Dict[str,int]],None]): # return new
        pass

    def split(self):
        self.split_video(split_locations=self.split_locator())






