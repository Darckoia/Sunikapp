from datetime import datetime

from pydantic import BaseModel


class AudioGenerationRequest(BaseModel):
    prompt: str
    genre: str = "Electronic"
    duration: float = 10.0
    bpm: int = 120
    scale: str = "C Minor"
    instrumental_mode: bool = False


class GenerationOut(BaseModel):
    id: int
    status: str
    prompt: str
    created_at: datetime

    model_config = {"from_attributes": True}
