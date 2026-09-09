from sqlalchemy.orm import Session

from backend.app.models.track import Track
from backend.app.schemas.track import TrackCreate, TrackUpdate


def list_tracks(db: Session, skip: int = 0, limit: int = 50) -> list[Track]:
    return db.query(Track).offset(skip).limit(limit).all()


def get_track(db: Session, track_id: int) -> Track | None:
    return db.query(Track).filter(Track.id == track_id).first()


def create_track(db: Session, payload: TrackCreate, audio_url: str) -> Track:
    track = Track(**payload.model_dump(), audio_url=audio_url)
    db.add(track)
    db.commit()
    db.refresh(track)
    return track


def update_track(db: Session, track: Track, payload: TrackUpdate) -> Track:
    for key, value in payload.model_dump(exclude_none=True).items():
        setattr(track, key, value)
    db.commit()
    db.refresh(track)
    return track


def delete_track(db: Session, track: Track) -> None:
    db.delete(track)
    db.commit()
