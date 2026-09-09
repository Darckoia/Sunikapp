from backend.app.services.audio_synth import AudioSynthService


def test_generate_full_track_returns_audio_array():
    synth = AudioSynthService()
    audio = synth.generate_full_track("dark synth pop", "Pop", 2.0, 120, True)
    assert audio.size > 0
    assert float(audio.max()) <= 1.0
