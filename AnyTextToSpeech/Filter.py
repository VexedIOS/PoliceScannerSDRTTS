from abc import ABC, abstractmethod
from df.enhance import enhance, init_df, load_audio, save_audio
from pydub import AudioSegment

class Filter(ABC):
    def __init__(self, raw_audio_path, output_path=None):
        self.raw_audio_path = raw_audio_path
        self.output_path = output_path

    @abstractmethod
    def filter_audio(self):
        pass

class DeepFilterNet(Filter):

    def filter_audio(self):

        # Load default model
        model, df_state, _ = init_df()
        # Download and open some audio file. You use your audio files here
        audio_path = ""
        audio, _ = load_audio(audio_path, sr=df_state.sr())
        # Denoise the audio
        enhanced = enhance(model, df_state, audio)
        # Save for listening
        save_audio("enhanced.wav", enhanced, df_state.sr())

    def resample_48K(self):
        audio = AudioSegment.from_file(self.raw_audio_path)
        audio_resampled = audio.set_frame_rate(48000)
        # Export the resampled audio file
        output_resample_path = f"{self.output_path}/resampled.wav"
        audio_resampled.export(self.output_path, format="wav")
        return

