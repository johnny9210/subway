/// 열차 도착 정보 레포지토리 - API 호출 담당
import 'dart:convert';
import 'package:http/http.dart' as http;
import '../domain/arrival_model.dart';

class ArrivalRepository {
  // 백엔드 URL (로컬 개발용)
  static const String _baseUrl = 'http://localhost:8001/api/v1';

  /// 역 이름에서 "역" 접미사 제거 (API 호출용)
  static String _cleanStationName(String stationName) {
    return stationName.replaceAll('역', '').trim();
  }

  /// 특정 역의 실시간 열차 도착 정보 가져오기
  static Future<ArrivalsResponse> fetchArrivals({
    required String stationName,
    String? lineId,
  }) async {
    // API 호출 시 "역" 제거
    final cleanName = _cleanStationName(stationName);
    String url = '$_baseUrl/stations/$cleanName/arrivals';
    if (lineId != null) {
      url += '?line_id=$lineId';
    }

    final uri = Uri.parse(url);

    try {
      final response = await http.get(uri).timeout(
        const Duration(seconds: 10),
      );

      if (response.statusCode == 200) {
        final json = jsonDecode(response.body) as Map<String, dynamic>;
        return ArrivalsResponse.fromJson(json);
      } else {
        throw Exception('도착 정보를 가져올 수 없습니다: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('네트워크 오류: $e');
    }
  }

  /// 방향별 열차 도착 정보 가져오기
  static Future<ArrivalsResponse> fetchArrivalsByDirection({
    required String stationName,
    required String direction,
    String? lineId,
  }) async {
    // API 호출 시 "역" 제거
    final cleanName = _cleanStationName(stationName);
    String url = '$_baseUrl/stations/$cleanName/arrivals/$direction';
    if (lineId != null) {
      url += '?line_id=$lineId';
    }

    final uri = Uri.parse(url);

    try {
      final response = await http.get(uri).timeout(
        const Duration(seconds: 10),
      );

      if (response.statusCode == 200) {
        final json = jsonDecode(response.body) as Map<String, dynamic>;
        return ArrivalsResponse.fromJson(json);
      } else {
        throw Exception('도착 정보를 가져올 수 없습니다: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('네트워크 오류: $e');
    }
  }
}
