import librosa
import soundfile as sf

def crop_wav_file(wav_file, start_time, end_time, save_path):
    (sig, rate) = librosa.load(wav_file, sr=None)
    new_sig = sig[int(start_time*rate) : int(end_time*rate)]
    sf.write(save_path, new_sig, rate)
