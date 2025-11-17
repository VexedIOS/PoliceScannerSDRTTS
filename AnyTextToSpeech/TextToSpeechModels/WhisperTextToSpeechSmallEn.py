import warnings
warnings.simplefilter("ignore")
import os
import whisper
from AnyTextToSpeech.TextToSpeechModels.TextToSpeech import TextToSpeech

whisper_model = whisper.load_model("small.en")

class WhisperTextToSpeechSmallEn(TextToSpeech):
    def get_text(self):

        if not os.path.exists(self.audio_path):
            print(f"Error: Audio file not found at '{self.audio_path}'.'")
            return None
        else:
            # Transcribe the audio
            # print(f"Transcribing '{audio_file_path}' using Whisper..")
            self.text_data = whisper_model.transcribe(self.audio_path, temperature=0)
            return self.text_data