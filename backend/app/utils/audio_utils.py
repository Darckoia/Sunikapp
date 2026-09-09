from io import BytesIO

import numpy as np
import soundfile as sf


def to_wav_bytes(audio: np.ndarray, sr: int) -> bytes:
    buffer = BytesIO()
    sf.write(buffer, audio, sr, format="WAV", subtype="PCM_16")
    return buffer.getvalue()
