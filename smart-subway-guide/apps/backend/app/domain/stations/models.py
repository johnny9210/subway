"""Station Domain Models"""
from typing import Optional
from pydantic import BaseModel


class StationLocation(BaseModel):
    """역 위치 정보"""
    station_id: str
    station_name: str
    line: str
    latitude: float
    longitude: float


class NearbyStation(BaseModel):
    """가까운 역 정보 (거리 포함)"""
    station_id: str
    station_name: str
    line: str
    latitude: float
    longitude: float
    distance_meters: float
    distance_text: str  # "350m", "1.2km"
