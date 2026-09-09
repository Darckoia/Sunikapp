from backend.app.services.analysis_service import AnalysisService


def test_analysis_detect_bpm_bounds():
    svc = AnalysisService()
    bpm = svc.detect_bpm([0.1, -0.2, 0.1, -0.2] * 500)
    assert 60 <= bpm <= 200
