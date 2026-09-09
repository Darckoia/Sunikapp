import numpy as np


class AnalysisService:
    def detect_bpm(self, audio_array: np.ndarray) -> int:
        if len(audio_array) == 0:
            return 0
        crossings = np.where(np.diff(np.signbit(audio_array)))[0]
        rough = max(60, min(200, int(len(crossings) / 10)))
        return rough

    def detect_key(self, audio_array: np.ndarray) -> str:
        return "C Minor" if float(np.mean(audio_array)) < 0.01 else "A Minor"

    def get_spectral_features(self, audio_array: np.ndarray) -> dict:
        spectrum = np.abs(np.fft.rfft(audio_array))
        return {
            "centroid": float(np.argmax(spectrum)) if len(spectrum) else 0.0,
            "energy": float(np.mean(spectrum)) if len(spectrum) else 0.0,
        }

    def get_audio_duration(self, audio_array: np.ndarray, sr: int) -> float:
        return 0.0 if sr <= 0 else len(audio_array) / sr

    def get_loudness(self, audio_array: np.ndarray) -> float:
        rms = np.sqrt(np.mean(np.square(audio_array))) if len(audio_array) else 0.0
        return float(20 * np.log10(rms + 1e-9))
