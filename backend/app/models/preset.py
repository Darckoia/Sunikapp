from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.models.database import Base


class Preset(Base):
    __tablename__ = "presets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), default=1)
    name: Mapped[str] = mapped_column(String(120), unique=True)
    synth_params: Mapped[str] = mapped_column(String(2000), default="{}")
    effects_params: Mapped[str] = mapped_column(String(2000), default="{}")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
