"""
SUNIKFLOW API - Main Application Entry Point
FastAPI backend for audio generation and synthesis platform
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os

# Create FastAPI instance
app = FastAPI(
    title="SUNIKFLOW API",
    description="Audio Generation & Synthesis Platform API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health Check Endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "SUNIKFLOW API",
        "version": "1.0.0"
    }

# API Routes
@app.get("/api/v1/health")
async def api_health():
    """API health check"""
    return {
        "status": "healthy",
        "api": "SUNIKFLOW v1.0.0"
    }

# WebSocket endpoint placeholder
@app.websocket("/ws/generate")
async def websocket_generate(websocket):
    """WebSocket endpoint for real-time audio generation"""
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            # Process audio generation request
            response = {"status": "processing", "data": data}
            await websocket.send_json(response)
    except Exception as e:
        await websocket.close(code=1000)

# Mount static frontend files
frontend_dir = Path(__file__).parent.parent / "frontend"
if frontend_dir.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))
    reload = os.getenv("API_RELOAD", "true").lower() == "true"
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
    )
