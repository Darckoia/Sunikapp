from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


@dataclass(slots=True)
class Track:
    """Core song/project metadata independent of the UI."""

    title: str
    prompt: str = ""
    genre: str = ""
    duration_seconds: float = 0.0
    audio_path: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def as_dict(self) -> dict:
        return {
            "title": self.title,
            "prompt": self.prompt,
            "genre": self.genre,
            "duration_seconds": self.duration_seconds,
            "audio_path": self.audio_path,
            "created_at": self.created_at.isoformat(),
        }
