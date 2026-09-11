"""
Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

# User Schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr

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
class GenerationBase(BaseModel):
    prompt: str

class GenerationCreate(GenerationBase):
    track_id: int

class Generation(GenerationBase):
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
