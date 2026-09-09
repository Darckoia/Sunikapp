from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend.app.api.routes import api_router
from backend.app.api.websocket import router as ws_router
from backend.app.middleware.cors import apply_cors
from backend.app.middleware.error_handler import register_error_handlers


def create_app() -> FastAPI:
    app = FastAPI(title="SUNIKFLOW API", version="1.0.0")
    apply_cors(app)
    register_error_handlers(app)
    app.include_router(api_router, prefix="/api/v1")
    app.include_router(ws_router)
    frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
    if not frontend_dir.exists():
        frontend_dir = Path(__file__).resolve().parent.parent.parent / "frontend"
    app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")
    return app


app = create_app()
