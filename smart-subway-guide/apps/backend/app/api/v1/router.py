"""API v1 Router"""
from fastapi import APIRouter

from app.api.v1.endpoints import auth, stations, arrivals, travel_logs, health

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(stations.router, prefix="/stations", tags=["stations"])
api_router.include_router(arrivals.router, prefix="/stations", tags=["arrivals"])
api_router.include_router(travel_logs.router, prefix="/travel-logs", tags=["travel-logs"])
