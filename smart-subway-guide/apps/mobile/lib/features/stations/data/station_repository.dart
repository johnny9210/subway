/// 역 데이터 레포지토리 - API 호출 담당
import 'dart:convert';
import 'package:http/http.dart' as http;
import '../domain/station_model.dart';

class StationRepository {
  // TODO: 실제 백엔드 URL로 변경
  static const String _baseUrl = 'http://localhost:8001/api/v1';

  /// API에서 가까운 역 목록 가져오기 (카카오 API 사용)
  static Future<List<NearbyStation>> fetchNearbyStations({
    required double latitude,
    required double longitude,
    int limit = 5,
    int radius = 2000,
  }) async {
    final uri = Uri.parse(
      '$_baseUrl/stations/nearby/?lat=$latitude&lng=$longitude&limit=$limit&radius=$radius',
    );

    final response = await http.get(uri).timeout(
      const Duration(seconds: 10),
    );

    if (response.statusCode == 200) {
      final List<dynamic> jsonList = json.decode(response.body);
      return jsonList.map((json) => NearbyStation.fromJson(json)).toList();
    } else {
      throw Exception('가까운 역을 찾을 수 없습니다: ${response.statusCode}');
    }
  }
}
