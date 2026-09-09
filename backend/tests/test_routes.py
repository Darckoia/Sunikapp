from backend.tests.conftest import client


def test_generate_and_list_tracks_flow():
    response = client.post(
        "/api/v1/audio/generate",
        json={
            "prompt": "cyberpunk synthwave",
            "genre": "Electronic",
            "duration": 1.0,
            "bpm": 120,
            "scale": "C Minor",
            "instrumental_mode": True,
        },
    )
    assert response.status_code == 200
    tracks = client.get("/api/v1/tracks")
    assert tracks.status_code == 200
    assert len(tracks.json()) >= 1
