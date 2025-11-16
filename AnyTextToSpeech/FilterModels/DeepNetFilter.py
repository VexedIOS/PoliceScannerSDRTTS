import ffmpeg
from df.enhance import enhance, init_df, load_audio, save_audio
import os
from AnyTextToSpeech.FilterModels.Filter import Filter


class DeepNetFilter(Filter):
    def filter_audio(self):
        resampled_out_path = f"{self.output_path}/resampled_audio.wav"
        (
            ffmpeg
            .input(self.raw_audio_path)
            .output(resampled_out_path, acodec='pcm_s16le',
                    ar='48k')  # Change codec to AAC and set sample rate to 48kHz
            .run()
        )
        model, df_state, _ = init_df()  # Load default model
        audio, _ = load_audio(resampled_out_path, sr=df_state.sr())
        enhanced_audio = enhance(model, df_state, audio)
        basename = os.path.basename(self.raw_audio_path)
        save_audio(out_path := f"{self.output_path}/{basename}", enhanced_audio, df_state.sr())
        return out_path