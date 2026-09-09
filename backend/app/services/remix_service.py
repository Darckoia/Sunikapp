import numpy as np


class RemixService:
    def change_tempo(self, track: np.ndarray, new_bpm: int) -> np.ndarray:
        factor = max(new_bpm, 1) / 120.0
        idx = np.arange(0, len(track), factor)
        return np.interp(idx, np.arange(len(track)), track)

    def pitch_shift(self, track: np.ndarray, semitones: int) -> np.ndarray:
        factor = 2 ** (semitones / 12.0)
        idx = np.arange(0, len(track), factor)
        shifted = np.interp(idx, np.arange(len(track)), track)
        return shifted[: len(track)] if len(shifted) >= len(track) else np.pad(shifted, (0, len(track) - len(shifted)))

    def time_stretch(self, track: np.ndarray, factor: float) -> np.ndarray:
        factor = max(factor, 0.1)
        idx = np.arange(0, len(track), factor)
        return np.interp(idx, np.arange(len(track)), track)

    def create_variation(self, track: np.ndarray, style_params: dict) -> np.ndarray:
        semitones = int(style_params.get("semitones", 0))
        bpm = int(style_params.get("bpm", 120))
        return self.change_tempo(self.pitch_shift(track, semitones), bpm)
