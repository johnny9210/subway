"""Health Check Endpoints"""
from fastapi import APIRouter

router = APIRouter()


@router.get("")
async def health_check():
    """서버 상태 확인"""
    return {
        "status": "healthy",
        "service": "Smart Subway Guide API",
    }
