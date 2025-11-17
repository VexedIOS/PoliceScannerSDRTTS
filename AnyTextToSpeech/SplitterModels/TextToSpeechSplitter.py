from AnyTextToSpeech.SplitterModels.Splitter import Splitter
from typing import Union, List, Dict
import torch
import os
import ffmpeg

# LOAD MODEL

torch.set_num_threads(1)
silero_model, utils = torch.hub.load(
    repo_or_dir='snakers4/silero-vad',
    model='silero_vad',
    force_reload=True  # Keeps older file saves time
)
(get_speech_timestamps, _, read_audio, *_) = utils


class TextToSpeechSplitter(Splitter):
    SAMPLING_RATE = 16000

    def split_locator(self) -> Union[List[Dict[str,int]],None]:
        try:
            wav = read_audio(self.raw_audio_path, sampling_rate=TextToSpeechSplitter.SAMPLING_RATE)  # Read the audio file

            speech_timestamps = get_speech_timestamps(
                wav,
                silero_model,
                sampling_rate=TextToSpeechSplitter.SAMPLING_RATE,
                return_seconds=True,
                threshold = 0.3
            )

            return speech_timestamps
        except:
            return None
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
                    .output(output_destination, c='copy', loglevel="panic")  # Copy streams without re-encoding
                    .run(overwrite_output=True)  # Run the command and overwrite if output exists
                )

