from pathlib import Path

import numpy as np
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, Response
from sqlalchemy.orm import Session

from backend.app.api.dependencies import get_db
from backend.app.models.database import Base, engine
from backend.app.models.track import Track
from backend.app.schemas.generation import AudioGenerationRequest, GenerationOut
from backend.app.schemas.project import ProjectCreate, ProjectOut
from backend.app.schemas.track import TrackCreate, TrackOut, TrackUpdate
from backend.app.services.analysis_service import AnalysisService
from backend.app.services.export_service import ExportService
from backend.app.services.generation_service import start_generation
from backend.app.services.mixer_service import MixerService
from backend.app.services.project_service import create_project, list_projects
from backend.app.services.remix_service import RemixService
from backend.app.services.track_service import create_track, delete_track, get_track, list_tracks, update_track


Base.metadata.create_all(bind=engine)

api_router = APIRouter()
analysis = AnalysisService()
remix = RemixService()
mixer = MixerService()
exporter = ExportService()


@api_router.post("/audio/generate", response_model=GenerationOut)
def generate_audio(payload: AudioGenerationRequest, db: Session = Depends(get_db)):
    return start_generation(db, payload)


@api_router.get("/audio/generate/{generation_id}", response_model=GenerationOut)
def generation_status(generation_id: int, db: Session = Depends(get_db)):
    row = db.query(__import__("app.models.generation", fromlist=["Generation"]).Generation).filter_by(id=generation_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Generation not found")
    return row


@api_router.get("/tracks", response_model=list[TrackOut])
def tracks(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return list_tracks(db, skip, limit)


@api_router.get("/tracks/{track_id}", response_model=TrackOut)
def track(track_id: int, db: Session = Depends(get_db)):
    item = get_track(db, track_id)
    if not item:
        raise HTTPException(status_code=404, detail="Track not found")
    return item


@api_router.post("/tracks", response_model=TrackOut)
async def create_track_route(
    title: str,
    description: str = "",
    genre: str = "Electronic",
    mood: str = "Energetic",
    bpm: int = 120,
    duration: float = 10.0,
    scale: str = "C Minor",
    instrumental: bool = False,
    audio_file: UploadFile | None = File(default=None),
    db: Session = Depends(get_db),
):
    payload = TrackCreate(
        title=title,
        description=description,
        genre=genre,
        mood=mood,
        bpm=bpm,
        duration=duration,
        scale=scale,
        instrumental=instrumental,
    )
    audio_url = ""
    if audio_file:
        content = await audio_file.read()
        target = Path("backend/audio_cache") / audio_file.filename
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
        audio_url = str(target)
    return create_track(db, payload, audio_url)


@api_router.patch("/tracks/{track_id}", response_model=TrackOut)
def patch_track(track_id: int, payload: TrackUpdate, db: Session = Depends(get_db)):
    item = get_track(db, track_id)
    if not item:
        raise HTTPException(status_code=404, detail="Track not found")
    return update_track(db, item, payload)


@api_router.delete("/tracks/{track_id}")
def remove_track(track_id: int, db: Session = Depends(get_db)):
    item = get_track(db, track_id)
    if not item:
        raise HTTPException(status_code=404, detail="Track not found")
    delete_track(db, item)
    return {"message": "Track deleted"}


@api_router.get("/tracks/{track_id}/download")
def download_track(track_id: int, db: Session = Depends(get_db)):
    item = get_track(db, track_id)
    if not item or not item.audio_url or not Path(item.audio_url).exists():
        raise HTTPException(status_code=404, detail="Track audio not found")
    return FileResponse(item.audio_url, media_type="audio/wav", filename=f"track_{track_id}.wav")


@api_router.get("/tracks/{track_id}/stems")
def stems(track_id: int, db: Session = Depends(get_db)):
    item = get_track(db, track_id)
    if not item or not item.audio_url or not Path(item.audio_url).exists():
        raise HTTPException(status_code=404, detail="Track audio not found")
    import soundfile as sf

    audio, _ = sf.read(item.audio_url)
    return Response(exporter.export_stems_zip(np.asarray(audio)), media_type="application/zip")


@api_router.get("/tracks/{track_id}/metadata")
def metadata(track_id: int, db: Session = Depends(get_db)):
    item = get_track(db, track_id)
    if not item:
        raise HTTPException(status_code=404, detail="Track not found")
    return Response(exporter.export_metadata_json({"id": item.id, "title": item.title, "bpm": item.bpm}), media_type="application/json")


@api_router.post("/remix/{track_id}/tempo")
def remix_tempo(track_id: int, new_bpm: int, db: Session = Depends(get_db)):
    item = get_track(db, track_id)
    if not item:
        raise HTTPException(status_code=404, detail="Track not found")
    return {"track_id": track_id, "new_bpm": new_bpm}


@api_router.post("/remix/{track_id}/pitch")
def remix_pitch(track_id: int, semitones: int, db: Session = Depends(get_db)):
    item = get_track(db, track_id)
    if not item:
        raise HTTPException(status_code=404, detail="Track not found")
    return {"track_id": track_id, "semitones": semitones}


@api_router.post("/remix/{track_id}")
def remix_track(track_id: int, db: Session = Depends(get_db)):
    item = get_track(db, track_id)
    if not item:
        raise HTTPException(status_code=404, detail="Track not found")
    return {"track_id": track_id, "status": "variation_created"}


@api_router.post("/mixer/combine")
def combine_tracks(track1_id: int, track2_id: int, db: Session = Depends(get_db)):
    t1 = get_track(db, track1_id)
    t2 = get_track(db, track2_id)
    if not t1 or not t2:
        raise HTTPException(status_code=404, detail="Track not found")
    return {"status": "combined", "track1_id": track1_id, "track2_id": track2_id}


@api_router.post("/analysis/detect-bpm")
def detect_bpm(values: list[float]):
    return {"bpm": analysis.detect_bpm(np.asarray(values, dtype=float))}


@api_router.post("/analysis/detect-key")
def detect_key(values: list[float]):
    return {"key": analysis.detect_key(np.asarray(values, dtype=float))}


@api_router.get("/projects", response_model=list[ProjectOut])
def projects(db: Session = Depends(get_db)):
    return list_projects(db)


@api_router.post("/projects", response_model=ProjectOut)
def create_project_route(payload: ProjectCreate, db: Session = Depends(get_db)):
    return create_project(db, payload)


@api_router.get("/projects/{project_id}", response_model=ProjectOut)
def project_get(project_id: int, db: Session = Depends(get_db)):
    item = db.query(__import__("app.models.project", fromlist=["Project"]).Project).filter_by(id=project_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Project not found")
    return item


@api_router.delete("/projects/{project_id}")
def project_delete(project_id: int, db: Session = Depends(get_db)):
    item = db.query(__import__("app.models.project", fromlist=["Project"]).Project).filter_by(id=project_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(item)
    db.commit()
    return {"message": "Project deleted"}


@api_router.post("/projects/{project_id}/export")
def project_export(project_id: int, db: Session = Depends(get_db)):
    item = db.query(__import__("app.models.project", fromlist=["Project"]).Project).filter_by(id=project_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Project not found")
    payload = {"id": item.id, "name": item.name, "description": item.description}
    return Response(exporter.export_project_zip(payload), media_type="application/zip")
