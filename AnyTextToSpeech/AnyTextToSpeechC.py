from numba.core.types import Callable
from whisper import Whisper

import AnyTextToSpeech.Splitter as Splitter
from AnyTextToSpeech.TextToSpeech import WhisperAPITextToSpeech
from typing import Any
import os
import AnyTextToSpeech.folder_utils as futils


class AnyTextToSpeech:

     def __init__(self, texttospeech: Any, splitter: Any, raw_audio_path, output_path, filter=None):
         self.raw_audio_path = raw_audio_path
         self.output_path= output_path
         self.texttospeech = texttospeech

         # Creates folder
         filename = os.path.basename(self.raw_audio_path)
         self.new_folder_path = f"{self.output_path}/{filename[:-4]}"
         futils.make_dir(self.new_folder_path)


         if filter is None:
            self.splitter = splitter(raw_audio_path=self.raw_audio_path, output_path=self.new_folder_path)
         else:
            pass

     def text_to_speech(self):
         self.splitter.split()
         audio_list = self.splitter.audio_created
         print(audio_list)
         if audio_list:
             for audio in audio_list:
                 TTS = self.texttospeech(audio)
                 TTS.get_text()
                 print(TTS.text_data)






any_tts = AnyTextToSpeech(splitter=Splitter.TextToSpeechSplitter,
                          texttospeech=WhisperAPITextToSpeech,
                          raw_audio_path="/home/vexed/SDRTrunk/recordings/20251111_190803Cities_Fresno_PoliceNorthEast__TO_4.mp3",
                          output_path="/home/vexed/PycharmProjects/PoliceScannerSDR/data/processed")
any_tts.text_to_speech()

