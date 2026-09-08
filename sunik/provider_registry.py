from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from .models import ProviderInfo
from .sfx_engine import SFXProvider


class MusicProvider(ABC):
    info: ProviderInfo

    @abstractmethod
    def generate(
        self,
        prompt: str,
        output_path: Path,
        duration_seconds: float,
        settings: dict[str, Any] | None = None,
    ) -> Path:
        raise NotImplementedError


class LyricsProvider(ABC):
    info: ProviderInfo

    @abstractmethod
    def generate(
        self,
        prompt: str,
        settings: dict[str, Any] | None = None,
    ) -> str:
        raise NotImplementedError


class VoiceProvider(ABC):
    info: ProviderInfo

    @abstractmethod
    def generate(
        self,
        text: str,
        voice: str,
        language: str,
        output_path: Path,
    ) -> Path:
        raise NotImplementedError


class StemProvider(ABC):
    info: ProviderInfo

    @abstractmethod
    def separate(
        self,
        audio_path: Path,
        output_dir: Path,
    ) -> dict[str, Path]:
        raise NotImplementedError


class MasteringProvider(ABC):
    info: ProviderInfo

    @abstractmethod
    def process(
        self,
        input_path: Path,
        output_path: Path,
        settings: dict[str, Any] | None = None,
    ) -> Path:
        raise NotImplementedError


class ProviderRegistry:
    def __init__(self) -> None:
        self._providers: dict[str, dict[str, Any]] = {
            "music": {},
            "lyrics": {},
            "voice": {},
            "stems": {},
            "mastering": {},
            "sfx": {},
        }

    def register(
        self,
        category: str,
        name: str,
        provider: Any,
    ) -> None:
        if category not in self._providers:
            raise ValueError(f"Categoría de proveedor no válida: {category}")

        self._providers[category][name] = provider

    def get(self, category: str, name: str) -> Any:
        if category not in self._providers:
            raise ValueError(f"Categoría de proveedor no válida: {category}")

        try:
            return self._providers[category][name]
        except KeyError as exc:
            raise KeyError(
                f"Proveedor no registrado: {category}/{name}"
            ) from exc

    def list(self, category: str | None = None) -> dict[str, list[str]]:
        if category is not None:
            if category not in self._providers:
                raise ValueError(f"Categoría de proveedor no válida: {category}")
            return {category: list(self._providers[category].keys())}

        return {
            key: list(value.keys())
            for key, value in self._providers.items()
        }

    def infos(self) -> list[ProviderInfo]:
        result: list[ProviderInfo] = []

        for providers in self._providers.values():
            for provider in providers.values():
                info = getattr(provider, "info", None)
                if isinstance(info, ProviderInfo):
                    result.append(info)

        return result


registry = ProviderRegistry()
py
