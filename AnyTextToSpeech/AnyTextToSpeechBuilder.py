from typing import Any
import os
import AnyTextToSpeech.folder_utils as futils
import shutil
from datetime import datetime

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

        if audio_list:
            for audio in audio_list:
                TTS = self.texttospeech(audio)
                TTS.get_text()
                self.file_all_data.append(TTS.text_data)

    def delete_all_files(self):
        if not os.path.isdir(self.new_folder_path):
            print(f"Error: The path '{self.new_folder_path}' is not a valid directory.")
            return

        for item in os.listdir(self.new_folder_path):
            item_path = os.path.join(self.new_folder_path, item)
            try:
                if os.path.isfile(item_path):
                    os.remove(item_path)  # Remove files
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)  # Remove subdirectories and their contents
            except OSError as e:
                #print(f"Error deleting {item_path}: {e}")
                pass
        os.rmdir(self.new_folder_path)

    def clean_SDR_text(self):
        text_only = []
        if self.file_all_data:
            for text_data in self.file_all_data:
                text_only.append(text_data["text"])

        all_text = "".join(text_only)
        basename= os.path.basename(self.raw_audio_path)
        basename = basename[:-4]
        return f"{basename}: {all_text}"

    def SDR_INFO(self):
        text_only = []
        if self.file_all_data:
            for text_data in self.file_all_data:
                text_only.append(text_data["text"])

        all_text = "".join(text_only)
        basename= os.path.basename(self.raw_audio_path)
        basename = basename[:-4]

        split_ = basename
        split_date = split_.split("_")[0] + split_.split("_")[1]
        split_date = "".join([char for char in split_date if not char.isalpha()])
        dt_object = datetime.strptime(split_date, "%Y%m%d%H%M%S")
        YMDHMS_format = dt_object.strftime("%Y-%m-%d %H:%M:%S")

        return [YMDHMS_format, basename, all_text]

