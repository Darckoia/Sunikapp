import numpy as np


class AudioSynthService:
    def __init__(self, sample_rate: int = 22050):
        self.sample_rate = sample_rate

    def generate_beat(self, genre: str, style: str, duration: float, bpm: int, scale: str) -> np.ndarray:
        return self.generate_full_track(style or genre, genre, duration, bpm, instrumental_mode=True)

    def synthesize_melody(self, pattern: list[float], duration: float, scale: str, timbre: str) -> np.ndarray:
        t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)
        note = pattern[0] if pattern else 220.0
        return np.sin(2 * np.pi * note * t) * 0.15

    def synthesize_bass(self, frequency: float, pattern: list[int], duration: float, modulation: float) -> np.ndarray:
        t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)
        return np.sin(2 * np.pi * max(frequency, 30.0) * t) * np.exp(-2.5 * t / max(duration, 0.1))

    def synthesize_drums(
        self,
        kick_pattern: list[int],
        snare_pattern: list[int],
        hihat_pattern: list[int],
        duration: float,
    ) -> np.ndarray:
        t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)
        noise = np.random.normal(0, 1, len(t))
        hats = noise * (((t * 8) % 1) < 0.08).astype(float) * 0.12
        kick = np.sin(2 * np.pi * 55 * t) * np.exp(-8.0 * ((t * 2) % 1))
        return kick * 0.7 + hats

    def generate_full_track(self, prompt: str, genre: str, duration: float, bpm: int, instrumental_mode: bool) -> np.ndarray:
        text = (prompt or "").lower()
        t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)
        if "synth" in text or "pop" in text:
            bass_hz = 60
        elif "reggaeton" in text or "urbano" in text:
            bass_hz = 50
        else:
            bass_hz = 55
        kick = np.sin(2 * np.pi * bass_hz * t) * np.exp(-4.0 * ((t * (bpm / 60)) % 1))
        melody = self.synthesize_melody([110.0, 130.81, 146.83, 164.81], duration, "C minor", "soft")
        drums = self.synthesize_drums([1], [1], [1], duration)
        mix = (kick * 0.45) + (melody * 0.35) + (drums * 0.3)
        return mix / (np.max(np.abs(mix)) + 1e-9) * 0.8
