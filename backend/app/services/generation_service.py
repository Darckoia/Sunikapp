from pathlib import Path

from sqlalchemy.orm import Session

from backend.app.models.generation import Generation
from backend.app.models.track import Track
from backend.app.schemas.generation import AudioGenerationRequest
from backend.app.services.audio_synth import AudioSynthService
from backend.app.services.export_service import ExportService
from backend.app.utils.file_utils import ensure_dir


synth = AudioSynthService()
exporter = ExportService()


def start_generation(db: Session, payload: AudioGenerationRequest) -> Generation:
    generation = Generation(prompt=payload.prompt, status="processing")
    db.add(generation)
    db.commit()
    db.refresh(generation)

    audio = synth.generate_full_track(
        prompt=payload.prompt,
        genre=payload.genre,
        duration=payload.duration,
        bpm=payload.bpm,
        instrumental_mode=payload.instrumental_mode,
    )

    cache_dir = ensure_dir("backend/audio_cache")
    track_id = f"track_{generation.id}.wav"
    wav_path = Path(cache_dir) / track_id
    wav_path.write_bytes(exporter.export_wav(audio, bit_depth=24, sample_rate=44100))

    track = Track(
        title=payload.prompt[:40] or "Generated track",
        description=payload.prompt,
        genre=payload.genre,
        mood="Energetic",
        bpm=payload.bpm,
        duration=payload.duration,
        scale=payload.scale,
        audio_url=str(wav_path),
        instrumental=payload.instrumental_mode,
    )
    db.add(track)
    db.commit()
    db.refresh(track)

    generation.status = "completed"
    generation.result_track_id = track.id
    db.commit()
    db.refresh(generation)
    return generation
