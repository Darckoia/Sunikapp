"""
Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Literal

# User Schemas
class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Project Schemas
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class Project(ProjectBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Track Schemas
class TrackBase(BaseModel):
    title: str
    duration: Optional[float] = None


class TrackCreate(TrackBase):
    project_id: Optional[int] = None


class Track(TrackBase):
    id: int
    user_id: int
    project_id: Optional[int]
    file_path: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Generation Schemas
class SoundEffectRequest(BaseModel):
    type: str
    offset: float = Field(0, ge=0, le=60)
    duration: Optional[float] = Field(None, gt=0, le=60)
    intensity: float = Field(0.6, ge=0, le=1)
    pan: float = Field(0, ge=-1, le=1)


class GenerationRequest(BaseModel):
    title: str = Field("Untitled", min_length=1, max_length=120)
    prompt: str = ""
    styles: List[str] = []
    lyrics: str = ""
    language: str = Field("es", min_length=2, max_length=16)
    voice_id: Optional[str] = None
    gender: Literal["female", "male", "neutral"] = "female"
    duration: float = Field(8, ge=0.1, le=60)
    effects: List[SoundEffectRequest] = []
    reverb: float = Field(20, ge=0, le=100)
    delay: float = Field(10, ge=0, le=100)
    instrumental_only: bool = False
    frequency: Optional[float] = Field(None, ge=20, le=20000)
    type: str = "sine"
    seed: Optional[int] = None


class GenerationCreate(BaseModel):
    track_id: int
    prompt: str


class Generation(GenerationCreate):
    id: int
    track_id: int
    status: str
    output_file: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Preset Schemas
class PresetBase(BaseModel):
    name: str
    description: Optional[str] = None
    config: dict
    is_default: bool = False


class PresetCreate(PresetBase):
    pass


class Preset(PresetBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Health Check Schema
class HealthCheck(BaseModel):
    status: str
    version: str
    service: str
