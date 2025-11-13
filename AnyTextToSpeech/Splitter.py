from abc import ABC, abstractmethod
from typing import List, Dict, Union
import os
import torch
import AnyTextToSpeech.folder_utils as futils
import ffmpeg

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


class TextToSpeechSplitter(Splitter):
    SAMPLING_RATE = 16000

    def split_locator(self) -> Union[List[Dict[str,int]],None]:
        # File path for testing

        # Initiate Speech Detector
        torch.set_num_threads(1)
        silero_model, utils = torch.hub.load(
            repo_or_dir='snakers4/silero-vad',
            model='silero_vad',
            force_reload=True  # Keeps older file saves time
        )
        (get_speech_timestamps, _, read_audio, *_) = utils

        wav = read_audio(self.raw_audio_path, sampling_rate=TextToSpeechSplitter.SAMPLING_RATE)  # Read the audio file

        speech_timestamps = get_speech_timestamps(
            wav,
            silero_model,
            sampling_rate=TextToSpeechSplitter.SAMPLING_RATE,
            return_seconds=True
        )

        return speech_timestamps

    def split_video(self, split_locations: Union[List[Dict[str,int]],None])-> None:
        if split_locations:

            #____place in outer class
            filename = os.path.basename(self.raw_audio_path)

            # start seperate and create files
            for time_stamp in split_locations:
                output_destination = f"{self.output_path}/{filename}_{time_stamp['start']}_{time_stamp['end']}.wav"
                self.audio_created.append(output_destination)
                (
                    ffmpeg
                    .input(self.raw_audio_path, ss=time_stamp['start'], to=time_stamp['end'])  # Specify start and end time for input
                    .output(output_destination, c='copy')  # Copy streams without re-encoding
                    .run(overwrite_output=True)  # Run the command and overwrite if output exists
                )

            print("Split Completed")

#splitter = TextToSpeechSplitter("/home/vexed/SDRTrunk/recordings/20251111_190803Cities_Fresno_PoliceNorthEast__TO_4.mp3",
                                #"/home/vexed/PycharmProjects/PoliceScannerSDR/data/processed")
#splitter.split()
