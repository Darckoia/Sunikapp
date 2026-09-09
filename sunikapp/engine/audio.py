from pathlib import Path

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt


class AudioEngine:
    """Deterministic local audio engine used by the UI and future AI backends."""

    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate

    def normalize(self, audio: np.ndarray, peak: float = 0.95) -> np.ndarray:
        audio = np.asarray(audio, dtype=np.float32)
        maximum = float(np.max(np.abs(audio))) if audio.size else 0.0
        return audio if maximum == 0 else audio * (peak / maximum)

    def bandpass(self, audio: np.ndarray, low: float = 40, high: float = 16000) -> np.ndarray:
        nyquist = self.sample_rate / 2
        low = max(1.0, min(low, nyquist - 2)) / nyquist
        high = max(low + 0.001, min(high, nyquist - 1))
        sos = butter(4, [low, high], btype="band", output="sos")
        return sosfilt(sos, np.asarray(audio, dtype=np.float32))

    def soft_clip(self, audio: np.ndarray, drive: float = 1.0) -> np.ndarray:
        return np.tanh(np.asarray(audio, dtype=np.float32) * drive)

    def delay_reverb(self, audio: np.ndarray, delay_ms: float = 45, mix: float = 0.15) -> np.ndarray:
        audio = np.asarray(audio, dtype=np.float32)
        delay = max(1, int(self.sample_rate * delay_ms / 1000))
        wet = np.zeros_like(audio)
        if delay < len(audio):
            wet[delay:] = audio[:-delay]
        return audio * (1 - mix) + wet * mix

    def master(self, audio: np.ndarray, eq: bool = True, compression: bool = True,
               reverb: float = 0.0) -> np.ndarray:
        result = np.asarray(audio, dtype=np.float32)
        if eq:
            result = self.bandpass(result)
        if compression:
            result = self.soft_clip(result, 1.25)
        if reverb > 0:
            result = self.delay_reverb(result, mix=min(float(reverb), 1.0) * 0.35)
        return self.normalize(result)

    def write_wav(self, path: str, audio: np.ndarray) -> str:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        pcm = np.int16(np.clip(audio, -1, 1) * 32767)
        wavfile.write(target, self.sample_rate, pcm)
        return str(target)
