"""Kakao Local API Client - 지하철역 검색"""
import httpx
from typing import List, Optional
from .models import NearbyStation
from ...config import settings


KAKAO_CATEGORY_URL = "https://dapi.kakao.com/v2/local/search/category.json"
SUBWAY_CATEGORY_CODE = "SW8"  # 카카오 카테고리: 지하철역


async def search_nearby_subway_stations(
    latitude: float,
    longitude: float,
    radius: int = 2000,
    limit: int = 5
) -> Optional[List[NearbyStation]]:
    """
    카카오 API를 사용하여 주변 지하철역 검색

    Args:
        latitude: 현재 위도
        longitude: 현재 경도
        radius: 검색 반경 (미터, 최대 20000)
        limit: 반환할 역 개수

    Returns:
        NearbyStation 리스트 또는 None (API 실패시)
    """
    api_key = settings.KAKAO_REST_API_KEY
    if not api_key:
        return None

    headers = {
        "Authorization": f"KakaoAK {api_key}"
    }

    params = {
        "category_group_code": SUBWAY_CATEGORY_CODE,
        "x": str(longitude),  # 카카오 API는 x=경도, y=위도
        "y": str(latitude),
        "radius": radius,
        "sort": "distance",
        "size": min(limit, 15)  # 카카오 API 최대 15개
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                KAKAO_CATEGORY_URL,
                headers=headers,
                params=params,
                timeout=10.0
            )
            response.raise_for_status()
            data = response.json()

            stations = []

            for place in data.get("documents", []):
                # 카카오 응답에서 역 정보 추출
                station_name = place.get("place_name", "")

                # 호선 정보 추출 (예: "강남역 2호선" -> "2")
                line = extract_line_from_name(station_name)

                # 역명 정리 (호선 정보 제거)
                clean_name = clean_station_name(station_name)

                # 역명 + 호선 표시 (예: "군자역 5호선")
                display_name = f"{clean_name} {line}호선" if line.isdigit() else f"{clean_name} {line}"

                station = NearbyStation(
                    station_id=place.get("id", ""),
                    station_name=display_name,
                    line=line,
                    latitude=float(place.get("y", 0)),
                    longitude=float(place.get("x", 0)),
                    distance_meters=float(place.get("distance", 0)),
                    distance_text=format_distance(float(place.get("distance", 0)))
                )
                stations.append(station)

            return stations[:limit]

    except Exception as e:
        print(f"Kakao API error: {e}")
        return None


def extract_line_from_name(name: str) -> str:
    """
    역 이름에서 호선 정보 추출
    예: "강남역 2호선" -> "2"
        "서울역 1호선" -> "1"
        "왕십리역 5호선" -> "5"
    """
    import re

    # 숫자호선 패턴
    match = re.search(r'(\d+)호선', name)
    if match:
        return match.group(1)

    # 특수 노선 처리
    line_mapping = {
        "경의중앙선": "경의중앙",
        "분당선": "분당",
        "신분당선": "신분당",
        "경춘선": "경춘",
        "공항철도": "공항",
        "수인분당선": "수인분당",
        "우이신설선": "우이신설",
        "서해선": "서해",
        "김포골드라인": "김포골드",
        "에버라인": "에버라인",
        "의정부경전철": "의정부",
        "인천1호선": "인천1",
        "인천2호선": "인천2",
    }

    for key, value in line_mapping.items():
        if key in name:
            return value

    return "1"  # 기본값


def clean_station_name(name: str) -> str:
    """
    역 이름에서 호선 정보 등 불필요한 부분 제거
    예: "강남역 2호선" -> "강남역"
        "서울역 1호선 경의중앙선" -> "서울역"
    """
    import re

    # 호선 정보 및 괄호 내용 제거
    cleaned = re.sub(r'\s*\d+호선.*$', '', name)
    cleaned = re.sub(r'\s*경의중앙선.*$', '', cleaned)
    cleaned = re.sub(r'\s*분당선.*$', '', cleaned)
    cleaned = re.sub(r'\s*신분당선.*$', '', cleaned)
    cleaned = re.sub(r'\s*\(.*\).*$', '', cleaned)

    return cleaned.strip()


def format_distance(meters: float) -> str:
    """거리를 사람이 읽기 좋은 형식으로 변환"""
    if meters < 1000:
        return f"{int(meters)}m"
    else:
        return f"{meters / 1000:.1f}km"
