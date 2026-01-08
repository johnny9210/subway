"""Station Service - 거리 계산 및 추천 로직"""
import math
from typing import List, Optional
from .models import StationLocation, NearbyStation
from .data import get_all_stations
from .kakao_api import search_nearby_subway_stations


async def find_nearby_stations_with_kakao(
    latitude: float,
    longitude: float,
    limit: int = 5,
    radius: int = 2000
) -> List[NearbyStation]:
    """
    카카오 API를 사용하여 주변 지하철역 검색

    Args:
        latitude: 현재 위도
        longitude: 현재 경도
        limit: 반환할 역 개수
        radius: 검색 반경 (미터)

    Returns:
        거리순으로 정렬된 NearbyStation 리스트
    """
    result = await search_nearby_subway_stations(
        latitude=latitude,
        longitude=longitude,
        radius=radius,
        limit=limit
    )
    return result if result else []


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    두 좌표 간의 거리 계산 (Haversine 공식)

    Args:
        lat1, lon1: 첫 번째 좌표 (위도, 경도)
        lat2, lon2: 두 번째 좌표 (위도, 경도)

    Returns:
        거리 (미터)
    """
    R = 6371000  # 지구 반지름 (미터)

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (math.sin(delta_phi / 2) ** 2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def format_distance(meters: float) -> str:
    """거리를 사람이 읽기 좋은 형식으로 변환"""
    if meters < 1000:
        return f"{int(meters)}m"
    else:
        return f"{meters / 1000:.1f}km"


def find_nearby_stations(
    latitude: float,
    longitude: float,
    limit: int = 5,
    max_distance: float = None
) -> List[NearbyStation]:
    """
    현재 위치에서 가장 가까운 역들을 찾아 반환

    Args:
        latitude: 현재 위도
        longitude: 현재 경도
        limit: 반환할 역 개수 (기본 5개)
        max_distance: 최대 거리 필터 (미터, None이면 제한 없음)

    Returns:
        거리순으로 정렬된 NearbyStation 리스트
    """
    stations = get_all_stations()
    nearby_list = []

    for station in stations:
        distance = haversine_distance(
            latitude, longitude,
            station.latitude, station.longitude
        )

        # 최대 거리 필터 적용
        if max_distance is not None and distance > max_distance:
            continue

        nearby_list.append(NearbyStation(
            station_id=station.station_id,
            station_name=station.station_name,
            line=station.line,
            latitude=station.latitude,
            longitude=station.longitude,
            distance_meters=distance,
            distance_text=format_distance(distance)
        ))

    # 거리순 정렬
    nearby_list.sort(key=lambda x: x.distance_meters)

    return nearby_list[:limit]
