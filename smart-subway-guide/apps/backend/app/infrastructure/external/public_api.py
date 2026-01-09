"""Public Data API Client - 공공 데이터 포털 연동"""
from typing import List
from datetime import datetime
import httpx

from app.config import settings
from app.core.exceptions import ExternalAPIException


# 지하철 호선 ID 매핑
SUBWAY_LINE_MAP = {
    "1001": {"name": "1호선", "color": "#0052A4", "number": 1},
    "1002": {"name": "2호선", "color": "#00A84D", "number": 2},
    "1003": {"name": "3호선", "color": "#EF7C1C", "number": 3},
    "1004": {"name": "4호선", "color": "#00A5DE", "number": 4},
    "1005": {"name": "5호선", "color": "#996CAC", "number": 5},
    "1006": {"name": "6호선", "color": "#CD7C2F", "number": 6},
    "1007": {"name": "7호선", "color": "#747F00", "number": 7},
    "1008": {"name": "8호선", "color": "#E6186C", "number": 8},
    "1009": {"name": "9호선", "color": "#BDB092", "number": 9},
    "1061": {"name": "중앙선", "color": "#77C4A3", "number": 0},
    "1063": {"name": "경의중앙선", "color": "#77C4A3", "number": 0},
    "1065": {"name": "공항철도", "color": "#0090D2", "number": 0},
    "1067": {"name": "경춘선", "color": "#0C8E72", "number": 0},
    "1075": {"name": "수인분당선", "color": "#F5A200", "number": 0},
    "1077": {"name": "신분당선", "color": "#D4003B", "number": 0},
    "1092": {"name": "우이신설선", "color": "#B7C452", "number": 0},
    "1093": {"name": "서해선", "color": "#81A914", "number": 0},
    "1081": {"name": "경강선", "color": "#0054A6", "number": 0},
    "1032": {"name": "GTX-A", "color": "#9A6292", "number": 0},
}

# 도착 코드 매핑
ARRIVAL_CODE_MAP = {
    "0": "진입",
    "1": "도착",
    "2": "출발",
    "3": "전역출발",
    "4": "전역진입",
    "5": "전역도착",
    "99": "운행중",
}


class PublicAPIClient:
    """서울시 지하철 실시간 도착 정보 API 클라이언트"""

    def __init__(self):
        self.base_url = settings.PUBLIC_API_BASE_URL
        self.api_key = settings.PUBLIC_API_KEY
        self.timeout = 5.0

    async def get_arrivals(self, station_name: str, start_index: int = 0, end_index: int = 20) -> List[dict]:
        """
        실시간 열차 도착 정보 조회

        Args:
            station_name: 역 이름 (예: "강남", "신도림", "서울" - 전체)
            start_index: 요청 시작 위치
            end_index: 요청 종료 위치

        Returns:
            열차 도착 정보 리스트
        """
        # 역 이름에서 "역" 제거
        clean_station_name = station_name.replace("역", "").strip()

        url = f"{self.base_url}/{self.api_key}/json/realtimeStationArrival/{start_index}/{end_index}/{clean_station_name}"

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()

                # API 에러 체크
                if "errorMessage" in data:
                    error_info = data["errorMessage"]
                    error_code = error_info.get("code", "UNKNOWN")
                    error_message = error_info.get("message", "알 수 없는 오류")

                    if error_code == "INFO-200":
                        return []

                    if error_code.startswith("ERROR"):
                        raise ExternalAPIException(detail=f"API 오류: {error_code} - {error_message}")

                if "realtimeArrivalList" in data:
                    return self._parse_arrivals(data["realtimeArrivalList"])
                return []

        except httpx.TimeoutException:
            raise ExternalAPIException(detail="API 응답 시간 초과")
        except httpx.HTTPError as e:
            raise ExternalAPIException(detail=f"API HTTP 오류: {str(e)}")

    def _parse_arrivals(self, arrivals: List[dict]) -> List[dict]:
        """API 응답을 내부 형식으로 변환"""
        result = []
        for arrival in arrivals:
            subway_id = arrival.get("subwayId", "")
            line_info = SUBWAY_LINE_MAP.get(subway_id, {"name": "알 수 없음", "color": "#888888", "number": 0})
            arrival_code = arrival.get("arvlCd", "99")

            arrival_seconds = self._parse_arrival_time(arrival.get("barvlDt", "0"))
            reception_time = arrival.get("recptnDt", "")
            adjusted_seconds = self._adjust_arrival_time(arrival_seconds, reception_time)

            result.append({
                "subway_id": subway_id,
                "line_name": line_info["name"],
                "line_color": line_info["color"],
                "line_number": line_info["number"],
                "updn_line": arrival.get("updnLine", ""),
                "train_line_nm": arrival.get("trainLineNm", ""),
                "station_name": arrival.get("statnNm", ""),
                "train_no": arrival.get("btrainNo", ""),
                "destination": arrival.get("bstatnNm", ""),
                "arrival_seconds": adjusted_seconds,
                "arrival_message": arrival.get("arvlMsg2", ""),
                "arrival_message_detail": arrival.get("arvlMsg3", ""),
                "arrival_code": arrival_code,
                "arrival_code_name": ARRIVAL_CODE_MAP.get(arrival_code, "알 수 없음"),
                "train_type": arrival.get("btrainSttus", "일반"),
                "is_last_train": arrival.get("lstcarAt", "0") == "1",
                "is_express": arrival.get("btrainSttus", "") in ["급행", "ITX", "특급"],
                "reception_time": reception_time,
            })
        return result

    def _parse_arrival_time(self, time_str: str) -> int:
        """도착 시간 문자열을 초 단위로 변환"""
        try:
            return int(time_str)
        except ValueError:
            return 0

    def _adjust_arrival_time(self, original_seconds: int, reception_time: str) -> int:
        """recptnDt 기준으로 도착 시간 보정"""
        if not reception_time:
            return original_seconds

        try:
            reception_dt = datetime.strptime(reception_time, "%Y-%m-%d %H:%M:%S")
            now = datetime.now()
            time_diff = (now - reception_dt).total_seconds()
            adjusted = max(0, original_seconds - int(time_diff))
            return adjusted
        except ValueError:
            return original_seconds


public_api_client = PublicAPIClient()
