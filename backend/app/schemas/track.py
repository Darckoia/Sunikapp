from datetime import datetime

from pydantic import BaseModel


class TrackCreate(BaseModel):
    title: str
    description: str = ""
    genre: str = "Electronic"
    mood: str = "Energetic"
    bpm: int = 120
    duration: float = 10.0
    scale: str = "C Minor"
    instrumental: bool = False


class TrackUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    mood: str | None = None


class TrackOut(BaseModel):
    id: int
    title: str
    description: str
    genre: str
    mood: str
    bpm: int
    duration: float
    scale: str
    audio_url: str
    instrumental: bool
    created_at: datetime

    model_config = {"from_attributes": True}
