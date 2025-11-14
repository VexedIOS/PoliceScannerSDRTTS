from AnyTextToSpeech.AnyTextToSpeechBuilder import AnyTextToSpeechBuild
from AnyTextToSpeech.AnyTextToSpeechBuilder import Splitter
from AnyTextToSpeech.AnyTextToSpeechBuilder import WhisperAPITextToSpeech

any_tts = AnyTextToSpeechBuild(splitter=Splitter.TextToSpeechSplitter,
                          texttospeech=WhisperAPITextToSpeech,
                          raw_audio_path="/home/vexed/SDRTrunk/recordings/20251111_190803Cities_Fresno_PoliceNorthEast__TO_4.mp3",
                          output_path="/home/vexed/PycharmProjects/PoliceScannerSDR/data/processed")
any_tts.text_to_speech()
#any_tts.delete_all_files()