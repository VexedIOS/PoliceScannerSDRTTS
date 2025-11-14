from abc import ABC, abstractmethod
import ffmpeg
from df import enhance, init_df
from df.enhance import enhance, init_df, load_audio, save_audio



class Filter(ABC):
    def __init__(self, raw_audio_path, output_path=None):
        self.raw_audio_path = raw_audio_path
        self.output_path = output_path

    @abstractmethod
    def filter_audio(self):
        pass

class RNNoiseFilter(Filter):
    def filter_audio(self):
        resampled_out_path = f"{self.output_path}/resampled_audio.wav"
        (
            ffmpeg
            .input(self.raw_audio_path)
            .output(resampled_out_path, acodec='pcm_s16le', ar='48k')  # Change codec to AAC and set sample rate to 48kHz
            .run()
        )
        model, df_state, _ = init_df()  # Load default model
        audio, _ = load_audio(resampled_out_path, sr=df_state.sr())
        enhanced_audio = enhance(model, df_state, audio)
        save_audio(f"{self.output_path}/enhanced.wav", enhanced_audio, df_state.sr())




filter = RNNoiseFilter(raw_audio_path="/home/vexed/SDRTrunk/recordings/20251111_190803Cities_Fresno_PoliceNorthEast__TO_4.mp3",
                 output_path="/home/vexed/PycharmProjects/PoliceScannerSDR/data/processed/20251111_190803Cities_Fresno_PoliceNorthEast__TO_4"
                 )

filter.filter_audio()