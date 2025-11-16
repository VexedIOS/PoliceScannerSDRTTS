from AnyTextToSpeech.AnyTextToSpeechBuilder import AnyTextToSpeechBuild
from AnyTextToSpeech.SplitterModels.TextToSpeechSplitter import TextToSpeechSplitter
from AnyTextToSpeech.TextToSpeechModels.WhisperTextToSpeechSmallEn import WhisperTextToSpeechSmallEn
from AnyTextToSpeech.folder_utils import check_all_files_in_folder
import os
import sys




if __name__ == "__main__":
    # This code will only run when the script is executed directly
    # While
    list_files = check_all_files_in_folder(starting_file_dir:="/home/vexed/SDRTrunk/recordings/")
    # check to see if files are in list_used_files
    oldest_first_ordered = sorted(list_files, key=lambda f: os.path.getmtime(os.path.join(starting_file_dir, f)))

    for file_name in oldest_first_ordered:

        any_tts = AnyTextToSpeechBuild(splitter=TextToSpeechSplitter,
                                  texttospeech= WhisperTextToSpeechSmallEn,
                                  raw_audio_path=file_name,
                                  output_path="/home/vexed/PycharmProjects/PoliceScannerSDR/data/processed")
        any_tts.text_to_speech()
        any_tts.clean_SDR_text()