"""Train Arrivals Endpoints - 실시간 열차 도착 정보"""
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Query, Path, HTTPException
from pydantic import BaseModel

from app.infrastructure.external.public_api import public_api_client

router = APIRouter()


class TrainArrival(BaseModel):
    """열차 도착 정보"""
    train_id: str
    line_name: str
    line_color: str
    line_number: int
    destination: str
    arrival_seconds: int
    arrival_message: str
    arrival_message_detail: str
    current_station: str
    direction: str
    train_type: str
    is_express: bool = False
    is_last_train: bool = False


class ArrivalsResponse(BaseModel):
    """열차 도착 정보 응답"""
    station_name: str
    arrivals: List[TrainArrival]
    updated_at: str


class DirectionArrivalsResponse(BaseModel):
    """방향별 열차 도착 정보 응답"""
    station_name: str
    direction: str
    arrivals: List[TrainArrival]
    updated_at: str


@router.get("/{station_name}/arrivals", response_model=ArrivalsResponse)
async def get_arrivals(
    station_name: str,
    line_id: Optional[str] = Query(None, description="호선 ID (예: 1002는 2호선)"),
):
    """
    실시간 열차 도착 정보 조회

    - station_name: 역 이름 (예: "강남", "강남역", "신도림")
    - line_id: 특정 호선만 필터링 (선택사항)
    """
    try:
        raw_arrivals = await public_api_client.get_arrivals(station_name)

        # 호선 ID로 필터링
        if line_id:
            raw_arrivals = [a for a in raw_arrivals if a["subway_id"] == line_id]

        arrivals = [
            TrainArrival(
                train_id=a["train_no"],
                line_name=a["line_name"],
                line_color=a["line_color"],
                line_number=a["line_number"],
                destination=a["destination"],
                arrival_seconds=a["arrival_seconds"],
                arrival_message=a["arrival_message"],
                arrival_message_detail=a["arrival_message_detail"],
                current_station=a["station_name"],
                direction=a["updn_line"],
                train_type=a["train_type"],
                is_express=a["is_express"],
                is_last_train=a["is_last_train"],
            )
            for a in raw_arrivals
        ]

        # 도착 시간순 정렬
        arrivals.sort(key=lambda x: x.arrival_seconds)

        return ArrivalsResponse(
            station_name=station_name.replace("역", ""),
            arrivals=arrivals,
            updated_at=datetime.now().isoformat(),
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"도착 정보 조회 실패: {str(e)}")


@router.get("/{station_name}/arrivals/{direction}", response_model=DirectionArrivalsResponse)
async def get_arrivals_by_direction(
    station_name: str,
    direction: str = Path(..., description="방향 (상행/내선 또는 하행/외선)"),
    line_id: Optional[str] = Query(None, description="호선 ID"),
):
    """
    방향별 실시간 열차 도착 정보 조회

    - direction: "상행" 또는 "하행" (2호선 순환선은 "내선" 또는 "외선")
    """
    try:
        raw_arrivals = await public_api_client.get_arrivals(station_name)

        # 방향 필터링
        filtered = [
            a for a in raw_arrivals
            if direction in a["updn_line"]
        ]

        # 호선 ID로 필터링
        if line_id:
            filtered = [a for a in filtered if a["subway_id"] == line_id]

        arrivals = [
            TrainArrival(
                train_id=a["train_no"],
                line_name=a["line_name"],
                line_color=a["line_color"],
                line_number=a["line_number"],
                destination=a["destination"],
                arrival_seconds=a["arrival_seconds"],
                arrival_message=a["arrival_message"],
                arrival_message_detail=a["arrival_message_detail"],
                current_station=a["station_name"],
                direction=a["updn_line"],
                train_type=a["train_type"],
                is_express=a["is_express"],
                is_last_train=a["is_last_train"],
            )
            for a in filtered
        ]

        arrivals.sort(key=lambda x: x.arrival_seconds)

        return DirectionArrivalsResponse(
            station_name=station_name.replace("역", ""),
            direction=direction,
            arrivals=arrivals,
            updated_at=datetime.now().isoformat(),
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"도착 정보 조회 실패: {str(e)}")
