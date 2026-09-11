"""
Configuration and environment variables for SUNIKFLOW backend
"""

from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # Database
    database_url: str = "sqlite:///./sunikapp.db"
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True
    
    # Environment
    environment: str = "development"
    debug: bool = True
    
    # Audio Processing
    sample_rate: int = 44100
    bit_depth: int = 16
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
