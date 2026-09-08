from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

class SFXProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, output_path: str | Path, duration_seconds: float = 2.0, settings: dict | None = None) -> str:
        raise NotImplementedError

class DemoSFXProvider(SFXProvider):
    """Proveedor DEMO/LOCAL. No simula IA: genera un marcador WAV en futuras implementaciones."""

    def generate(self, prompt: str, output_path: str | Path, duration_seconds: float = 2.0, settings: dict | None = None) -> str:
        raise NotImplementedError("DemoSFXProvider aún no genera audio. Conecta un proveedor SFX real.")
