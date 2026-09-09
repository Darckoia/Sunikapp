from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.models.database import Base


class Track(Base):
    __tablename__ = "tracks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), default=1)
    title: Mapped[str] = mapped_column(String(120), default="Untitled")
    description: Mapped[str] = mapped_column(String(500), default="")
    genre: Mapped[str] = mapped_column(String(50), default="Electronic")
    mood: Mapped[str] = mapped_column(String(50), default="Energetic")
    bpm: Mapped[int] = mapped_column(Integer, default=120)
    duration: Mapped[float] = mapped_column(Float, default=10.0)
    scale: Mapped[str] = mapped_column(String(20), default="C Minor")
    audio_url: Mapped[str] = mapped_column(String(255), default="")
    instrumental: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
