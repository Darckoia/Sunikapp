from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "SUNIKFLOW"
    database_url: str = "sqlite:///./sunikflow.db"
    audio_cache_dir: str = "backend/audio_cache"


settings = Settings()
