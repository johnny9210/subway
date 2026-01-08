/// 역 관련 모델 정의

/// 가까운 역 정보
class NearbyStation {
  final String stationId;
  final String stationName;
  final String line;
  final double latitude;
  final double longitude;
  final double distanceMeters;
  final String distanceText;

  NearbyStation({
    required this.stationId,
    required this.stationName,
    required this.line,
    required this.latitude,
    required this.longitude,
    required this.distanceMeters,
    required this.distanceText,
  });

  factory NearbyStation.fromJson(Map<String, dynamic> json) {
    return NearbyStation(
      stationId: json['station_id'] as String,
      stationName: json['station_name'] as String,
      line: json['line'] as String,
      latitude: (json['latitude'] as num).toDouble(),
      longitude: (json['longitude'] as num).toDouble(),
      distanceMeters: (json['distance_meters'] as num).toDouble(),
      distanceText: json['distance_text'] as String,
    );
  }

  /// 호선 번호를 색상으로 변환
  int get lineColor {
    switch (line) {
      case '1':
        return 0xFF0052A4; // 파랑
      case '2':
        return 0xFF00A84D; // 초록
      case '3':
        return 0xFFEF7C1C; // 주황
      case '4':
        return 0xFF00A5DE; // 하늘
      case '5':
        return 0xFF996CAC; // 보라
      case '6':
        return 0xFFCD7C2F; // 갈색
      case '7':
        return 0xFF747F00; // 올리브
      case '8':
        return 0xFFE6186C; // 분홍
      case '9':
        return 0xFFBDB092; // 금색
      default:
        return 0xFF6B7280; // 회색
    }
  }

  /// 표시용 역 이름 (호선 포함)
  String get displayName => '$stationName ($line호선)';
}
