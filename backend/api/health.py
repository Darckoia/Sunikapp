"""
Health check API endpoints
"""

from fastapi import APIRouter
from backend.schemas import HealthCheck

router = APIRouter(prefix="/api/v1", tags=["health"])

@router.get("/health", response_model=HealthCheck)
async def health_check():
    """Check API health status"""
    return HealthCheck(
        status="healthy",
        version="1.0.0",
        service="SUNIKFLOW"
    )
