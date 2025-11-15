import AnyTextToSpeech.Splitter as Splitter
from AnyTextToSpeech.TextToSpeech import WhisperAPITextToSpeech
from typing import Any
import os
import AnyTextToSpeech.folder_utils as futils
import shutil


class AnyTextToSpeechBuild:

    def __init__(self, texttospeech: Any, splitter: Any, raw_audio_path, output_path, filter=None):
        self.raw_audio_path = raw_audio_path
        self.output_path = output_path
        self.texttospeech = texttospeech
        self.file_all_data = []

        # Creates folder
        filename = os.path.basename(self.raw_audio_path)
        self.new_folder_path = f"{self.output_path}/{filename[:-4]}"
        futils.make_dir(self.new_folder_path)

        if filter is None:
            self.splitter = splitter(raw_audio_path=self.raw_audio_path, output_path=self.new_folder_path)
        else:
            filter_obj = filter(raw_audio_path=self.raw_audio_path, output_path=self.new_folder_path)
            filtered_path = filter_obj.filter_audio()
            self.splitter = splitter(raw_audio_path=filtered_path, output_path=self.new_folder_path)

    def text_to_speech(self):
        self.splitter.split()
        audio_list = self.splitter.audio_created
        print(audio_list)
        if audio_list:
            for audio in audio_list:
                TTS = self.texttospeech(audio)
                TTS.get_text()
                self.file_all_data.append(TTS.text_data)

    def delete_all_files(self):
        if not os.path.isdir(self.output_path):
            print(f"Error: The path '{self.output_path}' is not a valid directory.")
            return

        for item in os.listdir(self.output_path):
            item_path = os.path.join(self.output_path, item)
            try:
                if os.path.isfile(item_path):
                    os.remove(item_path)  # Remove files
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)  # Remove subdirectories and their contents
            except OSError as e:
                print(f"Error deleting {item_path}: {e}")

    def clean_text(self):
        pass


