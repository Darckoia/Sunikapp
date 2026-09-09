from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.models.database import Base


class Generation(Base):
    __tablename__ = "generations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), default=1)
    prompt: Mapped[str] = mapped_column(String(1000))
    status: Mapped[str] = mapped_column(String(50), default="pending")
    result_track_id: Mapped[int | None] = mapped_column(ForeignKey("tracks.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
