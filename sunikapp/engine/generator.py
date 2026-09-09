from dataclasses import dataclass

import numpy as np

from .audio import AudioEngine


@dataclass(slots=True)
class GenerationRequest:
    prompt: str
    genre: str = ""
    duration_seconds: float = 8.0
    frequency_hz: float = 220.0


class LocalGenerator:
    """Fallback generator. Replaceable by an AI music provider without UI changes."""

    def __init__(self, engine: AudioEngine | None = None):
        self.engine = engine or AudioEngine()

    def generate(self, request: GenerationRequest) -> np.ndarray:
        seconds = max(1.0, min(float(request.duration_seconds), 60.0))
        n = int(seconds * self.engine.sample_rate)
        t = np.arange(n, dtype=np.float32) / self.engine.sample_rate
        freq = max(40.0, min(float(request.frequency_hz), 1000.0))
        envelope = np.minimum(t / 0.08, 1.0) * np.minimum((seconds - t) / 0.15, 1.0)
        envelope = np.clip(envelope, 0, 1)
        tone = np.sin(2 * np.pi * freq * t)
        harmonic = 0.25 * np.sin(2 * np.pi * freq * 2 * t)
        return self.engine.normalize((tone + harmonic) * 0.35 * envelope)
