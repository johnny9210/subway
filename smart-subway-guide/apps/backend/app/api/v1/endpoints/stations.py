"""Station Endpoints"""
from typing import List, Optional
from fastapi import APIRouter, Query
from pydantic import BaseModel

router = APIRouter()


class Platform(BaseModel):
    """승강장 정보"""
    platform_id: str
    direction: str
    line_id: str


class Station(BaseModel):
    """역 정보"""
    station_id: str
    station_name: str
    line_id: str
    is_transfer: bool
    platforms: List[Platform]


class TravelTimeResponse(BaseModel):
    """평균 소요시간 응답"""
    station_id: str
    platform_id: str
    avg_seconds: float
    std_deviation: Optional[float]
    sample_count: int
    day_type: str
    time_slot: str


@router.get("/{station_id}", response_model=Station)
async def get_station(station_id: str):
    """역 정보 조회"""
    # TODO: 실제 DB 조회 로직 구현
    return Station(
        station_id=station_id,
        station_name="강남역",
        line_id="2",
        is_transfer=False,
        platforms=[
            Platform(platform_id=f"{station_id}_IN", direction="내선", line_id="2"),
            Platform(platform_id=f"{station_id}_OUT", direction="외선", line_id="2"),
        ],
    )


@router.get("/{station_id}/platforms", response_model=List[Platform])
async def get_platforms(station_id: str):
    """역 승강장 목록 조회"""
    # TODO: 실제 DB 조회 로직 구현
    return [
        Platform(platform_id=f"{station_id}_IN", direction="내선", line_id="2"),
        Platform(platform_id=f"{station_id}_OUT", direction="외선", line_id="2"),
    ]


@router.get("/{station_id}/travel-time", response_model=TravelTimeResponse)
async def get_travel_time(
    station_id: str,
    platform_id: str = Query(..., description="승강장 ID"),
    day_type: str = Query("weekday", description="요일 유형 (weekday/saturday/sunday)"),
    time_slot: str = Query("08:30", description="시간대 (HH:MM)"),
):
    """역별 평균 소요시간 조회"""
    # TODO: 실제 DB 조회 및 캐시 로직 구현
    return TravelTimeResponse(
        station_id=station_id,
        platform_id=platform_id,
        avg_seconds=200.0,
        std_deviation=30.0,
        sample_count=1500,
        day_type=day_type,
        time_slot=time_slot,
    )
