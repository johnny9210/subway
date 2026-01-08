"""Train Arrivals Endpoints"""
from typing import List
from fastapi import APIRouter, Query
from pydantic import BaseModel

router = APIRouter()


class TrainArrival(BaseModel):
    """열차 도착 정보"""
    train_id: str
    destination: str
    arrival_seconds: int
    current_station: str
    is_express: bool = False


class ArrivalsResponse(BaseModel):
    """열차 도착 정보 응답"""
    station_id: str
    direction: str
    arrivals: List[TrainArrival]
    updated_at: str


@router.get("/{station_id}/arrivals", response_model=ArrivalsResponse)
async def get_arrivals(
    station_id: str,
    direction: str = Query(..., description="방향 (inbound/outbound)"),
):
    """실시간 열차 도착 정보 조회"""
    # TODO: 공공 API 연동 및 캐시 로직 구현
    return ArrivalsResponse(
        station_id=station_id,
        direction=direction,
        arrivals=[
            TrainArrival(
                train_id="2001",
                destination="신도림",
                arrival_seconds=120,
                current_station="역삼",
            ),
            TrainArrival(
                train_id="2003",
                destination="신도림",
                arrival_seconds=420,
                current_station="선릉",
            ),
        ],
        updated_at="2026-01-08T08:30:00Z",
    )
