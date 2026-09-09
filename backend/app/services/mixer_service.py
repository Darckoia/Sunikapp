import numpy as np


class MixerService:
    def combine_tracks(self, track1: np.ndarray, track2: np.ndarray, volumes: list[float] | None = None) -> np.ndarray:
        volumes = volumes or [1.0, 0.5]
        length = max(len(track1), len(track2))
        a = np.pad(track1, (0, length - len(track1)))
        b = np.pad(track2, (0, length - len(track2)))
        mixed = (a * volumes[0]) + (b * volumes[1])
        return mixed / (np.max(np.abs(mixed)) + 1e-9)

    def extract_stems(self, track: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        return track * 0.8, track * 0.2

    def apply_crossfade(self, track1: np.ndarray, track2: np.ndarray, duration: float) -> np.ndarray:
        n = min(len(track1), len(track2), max(1, int(22050 * duration)))
        fade_out = np.linspace(1, 0, n)
        fade_in = np.linspace(0, 1, n)
        out = np.copy(track1)
        out[-n:] = track1[-n:] * fade_out + track2[:n] * fade_in
        return out
