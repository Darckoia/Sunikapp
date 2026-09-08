from dataclasses import dataclass, field
from typing import Any


@dataclass
class SongSpec:
    title: str = "Untitled"
    genre: str = "Unknown"
    subgenre: str = ""
    language: str = "es"
    bpm: int = 120
    key: str = "C"
    duration_seconds: float = 180.0
    structure: list[str] = field(default_factory=list)
    instruments: list[str] = field(default_factory=list)
    vocal_style: str = ""
    lyrics: str = ""
    production_instructions: str = ""
    original_prompt: str = ""
    sfx_requests: list[SFXRequest] = field(default_factory=list)


@dataclass
class ProviderInfo:
    name: str
    category: str
    mode: str = "DEMO"
    description: str = ""
    available: bool = True


@dataclass
class PipelineResult:
    success: bool
    status: str
    message: str = ""
    files: dict[str, str] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)


@dataclass
class SFXRequest:
    name: str
    category: str = ""
    position: str = ""
    intensity: str = ""
    duration_seconds: float | None = None
    prompt: str = ""
