"""Travel Logs Endpoints"""
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class TravelLogCreate(BaseModel):
    """소요시간 데이터 생성 요청"""
    station_id: str
    platform_id: str
    gate_id: str
    travel_seconds: int
    day_type: str
    time_slot: str
    device_hash: str


class TravelLogResponse(BaseModel):
    """소요시간 데이터 응답"""
    id: int
    station_id: str
    platform_id: str
    travel_seconds: int
    created_at: str


@router.post("", response_model=TravelLogResponse)
async def create_travel_log(log: TravelLogCreate):
    """소요시간 데이터 업로드"""
    # TODO: 실제 DB 저장 로직 구현
    return TravelLogResponse(
        id=1,
        station_id=log.station_id,
        platform_id=log.platform_id,
        travel_seconds=log.travel_seconds,
        created_at="2026-01-08T08:30:00Z",
    )
