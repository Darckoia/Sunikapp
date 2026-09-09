import json
import zipfile
from io import BytesIO

import numpy as np
import soundfile as sf

from backend.app.services.mixer_service import MixerService


class ExportService:
    def export_wav(self, track: np.ndarray, bit_depth: int = 24, sample_rate: int = 44100) -> bytes:
        subtype = "PCM_24" if bit_depth == 24 else "PCM_16"
        buffer = BytesIO()
        sf.write(buffer, track, sample_rate, format="WAV", subtype=subtype)
        return buffer.getvalue()

    def export_stems_zip(self, track: np.ndarray) -> bytes:
        mixer = MixerService()
        instrumental, vocals = mixer.extract_stems(track)
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            ins = BytesIO()
            vox = BytesIO()
            sf.write(ins, instrumental, 44100, format="WAV")
            sf.write(vox, vocals, 44100, format="WAV")
            zf.writestr("instrumental.wav", ins.getvalue())
            zf.writestr("vocals.wav", vox.getvalue())
        return zip_buffer.getvalue()

    def export_metadata_json(self, track: dict) -> bytes:
        return json.dumps(track, ensure_ascii=False, indent=2).encode("utf-8")

    def export_project_zip(self, project: dict) -> bytes:
        buffer = BytesIO()
        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("project.json", json.dumps(project, ensure_ascii=False, indent=2))
        return buffer.getvalue()
