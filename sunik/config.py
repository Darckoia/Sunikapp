from dataclasses import dataclass
from pathlib import Path
import os


@dataclass(frozen=True)
class Settings:
    environment: str
    storage_dir: Path
    audio_dir: Path
    projects_dir: Path

    openai_api_key: str | None
    music_provider_api_key: str | None
    voice_provider_api_key: str | None
    stem_provider_api_key: str | None

    @classmethod
    def from_env(cls) -> "Settings":
        storage = Path(os.getenv("SUNIK_STORAGE_DIR", "storage"))
        audio = Path(os.getenv("SUNIK_AUDIO_DIR", str(storage / "audio")))
        projects = Path(os.getenv("SUNIK_PROJECTS_DIR", str(storage / "projects")))

        return cls(
            environment=os.getenv("SUNIK_ENV", "demo"),
            storage_dir=storage,
            audio_dir=audio,
            projects_dir=projects,
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            music_provider_api_key=os.getenv("MUSIC_PROVIDER_API_KEY"),
            voice_provider_api_key=os.getenv("VOICE_PROVIDER_API_KEY"),
            stem_provider_api_key=os.getenv("STEM_PROVIDER_API_KEY"),
        )

    def ensure_directories(self) -> None:
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.audio_dir.mkdir(parents=True, exist_ok=True)
        self.projects_dir.mkdir(parents=True, exist_ok=True)

