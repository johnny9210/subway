"""Public Data API Client - 공공 데이터 포털 연동"""
from typing import List, Optional
import httpx

from app.config import settings
from app.core.exceptions import ExternalAPIException


class PublicAPIClient:
    """서울시 지하철 실시간 도착 정보 API 클라이언트"""

    def __init__(self):
        self.base_url = settings.PUBLIC_API_BASE_URL
        self.api_key = settings.PUBLIC_API_KEY
        self.timeout = 3.0  # 3초 타임아웃

    async def get_arrivals(self, station_name: str) -> List[dict]:
        """
        실시간 열차 도착 정보 조회

        Args:
            station_name: 역 이름 (예: "강남")

        Returns:
            열차 도착 정보 리스트
        """
        url = f"{self.base_url}/{self.api_key}/json/realtimeStationArrival/0/10/{station_name}"

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()

                # API 응답 파싱
                if "realtimeArrivalList" in data:
                    return self._parse_arrivals(data["realtimeArrivalList"])
                return []

        except httpx.TimeoutException:
            raise ExternalAPIException(detail="Public API timeout")
        except httpx.HTTPError as e:
            raise ExternalAPIException(detail=f"Public API error: {str(e)}")

    def _parse_arrivals(self, arrivals: List[dict]) -> List[dict]:
        """API 응답을 내부 형식으로 변환"""
        result = []
        for arrival in arrivals:
            result.append({
                "train_id": arrival.get("btrainNo", ""),
                "destination": arrival.get("bstatnNm", ""),
                "arrival_seconds": self._parse_arrival_time(arrival.get("barvlDt", "0")),
                "current_station": arrival.get("arvlMsg3", ""),
                "direction": arrival.get("updnLine", ""),
                "line_id": arrival.get("subwayId", ""),
            })
        return result

    def _parse_arrival_time(self, time_str: str) -> int:
        """도착 시간 문자열을 초 단위로 변환"""
        try:
            return int(time_str)
        except ValueError:
            return 0


# 싱글톤 인스턴스
public_api_client = PublicAPIClient()
