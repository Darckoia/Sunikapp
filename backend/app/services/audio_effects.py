import numpy as np
from scipy.signal import butter, lfilter


class AudioEffectsService:
    def reverb(self, audio: np.ndarray, decay_time: float = 0.3, wet_level: float = 0.3, dry_level: float = 0.7) -> np.ndarray:
        delay = max(1, int(22050 * min(decay_time, 2.0) * 0.1))
        wet = np.zeros_like(audio)
        wet[delay:] = audio[:-delay] * 0.5
        return (dry_level * audio) + (wet_level * wet)

    def eq_3band(self, audio: np.ndarray, bass_gain: float = 0, mid_gain: float = 0, treble_gain: float = 0) -> np.ndarray:
        nyq = 0.5 * 22050
        b, a = butter(2, [250 / nyq, 4000 / nyq], btype="band")
        mid = lfilter(b, a, audio)
        low = audio - mid
        high = audio - low - mid
        return low * (1 + bass_gain / 12) + mid * (1 + mid_gain / 12) + high * (1 + treble_gain / 12)

    def compressor(self, audio: np.ndarray, threshold: float = 0.25, ratio: float = 4.0, attack: float = 0.01, release: float = 0.1) -> np.ndarray:
        out = np.copy(audio)
        over = np.abs(audio) > threshold
        out[over] = np.sign(audio[over]) * (threshold + (np.abs(audio[over]) - threshold) / max(ratio, 1.0))
        return out

    def distortion(self, audio: np.ndarray, drive: float = 1.5, tone: float = 0.5, level: float = 0.8) -> np.ndarray:
        return np.tanh(audio * max(drive, 0.1)) * level

    def delay(self, audio: np.ndarray, time: float = 0.2, feedback: float = 0.3, wet_level: float = 0.25) -> np.ndarray:
        delay_samples = max(1, int(22050 * time))
        delayed = np.zeros_like(audio)
        delayed[delay_samples:] = audio[:-delay_samples] * feedback
        return audio * (1 - wet_level) + delayed * wet_level
