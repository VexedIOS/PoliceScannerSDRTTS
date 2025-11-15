from AnyTextToSpeech.AnyTextToSpeechBuilder import AnyTextToSpeechBuild
from AnyTextToSpeech.Splitter import TextToSpeechSplitter
from AnyTextToSpeech.TextToSpeech import WhisperTextToSpeechBlazing
#from AnyTextToSpeech.Filter import DeepNetFilter
from AnyTextToSpeech.folder_utils import check_all_files_in_folder
import os




if __name__ == "__main__":
    # This code will only run when the script is executed directly
    # While
    list_files = check_all_files_in_folder(starting_file_dir:="/home/vexed/SDRTrunk/recordings/")
    oldest_first_ordered = sorted(list_files, key=lambda f: os.path.getmtime(os.path.join(starting_file_dir, f)))

    for file_name in oldest_first_ordered:

        any_tts = AnyTextToSpeechBuild(splitter=TextToSpeechSplitter,
                                  texttospeech=WhisperTextToSpeechBlazing,
                                  raw_audio_path=file_name,
                                  output_path="/home/vexed/PycharmProjects/PoliceScannerSDR/data/processed")
        any_tts.text_to_speech()
        print(any_tts.file_all_data)
        #any_tts.delete_all_files()