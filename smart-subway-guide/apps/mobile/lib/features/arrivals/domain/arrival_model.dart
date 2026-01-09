/// 열차 도착 정보 모델
import 'package:flutter/material.dart';

class TrainArrival {
  final String trainId;
  final String lineName;
  final String lineColor;
  final int lineNumber;
  final String destination;
  final int arrivalSeconds;
  final String arrivalMessage;
  final String arrivalMessageDetail;
  final String currentStation;
  final String direction;
  final String trainType;
  final bool isExpress;
  final bool isLastTrain;

  TrainArrival({
    required this.trainId,
    required this.lineName,
    required this.lineColor,
    required this.lineNumber,
    required this.destination,
    required this.arrivalSeconds,
    required this.arrivalMessage,
    required this.arrivalMessageDetail,
    required this.currentStation,
    required this.direction,
    required this.trainType,
    this.isExpress = false,
    this.isLastTrain = false,
  });

  factory TrainArrival.fromJson(Map<String, dynamic> json) {
    return TrainArrival(
      trainId: json['train_id'] ?? '',
      lineName: json['line_name'] ?? '',
      lineColor: json['line_color'] ?? '#888888',
      lineNumber: json['line_number'] ?? 0,
      destination: json['destination'] ?? '',
      arrivalSeconds: json['arrival_seconds'] ?? 0,
      arrivalMessage: json['arrival_message'] ?? '',
      arrivalMessageDetail: json['arrival_message_detail'] ?? '',
      currentStation: json['current_station'] ?? '',
      direction: json['direction'] ?? '',
      trainType: json['train_type'] ?? '일반',
      isExpress: json['is_express'] ?? false,
      isLastTrain: json['is_last_train'] ?? false,
    );
  }

  /// 도착 시간을 "X분 Y초" 형식으로 변환
  String get formattedArrivalTime {
    if (arrivalSeconds <= 0) {
      return arrivalMessage.isNotEmpty ? arrivalMessage : '곧 도착';
    }
    final minutes = arrivalSeconds ~/ 60;
    final seconds = arrivalSeconds % 60;
    if (minutes > 0) {
      return '$minutes분 $seconds초';
    }
    return '$seconds초';
  }

  /// 호선 색상을 Color 객체로 변환
  Color get lineColorValue {
    try {
      return Color(int.parse(lineColor.replaceFirst('#', '0xFF')));
    } catch (e) {
      return Colors.grey;
    }
  }

  /// 열차 상태 텍스트 (혼잡도 등 - 현재는 기본값)
  String get statusText {
    if (isExpress) return '급행';
    if (isLastTrain) return '막차';
    return trainType;
  }

  /// 상태 색상
  Color get statusColor {
    if (isLastTrain) return Colors.red;
    if (isExpress) return Colors.orange;
    return Colors.green;
  }
}

class ArrivalsResponse {
  final String stationName;
  final List<TrainArrival> arrivals;
  final String updatedAt;

  ArrivalsResponse({
    required this.stationName,
    required this.arrivals,
    required this.updatedAt,
  });

  factory ArrivalsResponse.fromJson(Map<String, dynamic> json) {
    return ArrivalsResponse(
      stationName: json['station_name'] ?? '',
      arrivals: (json['arrivals'] as List<dynamic>?)
              ?.map((e) => TrainArrival.fromJson(e as Map<String, dynamic>))
              .toList() ??
          [],
      updatedAt: json['updated_at'] ?? '',
    );
  }
}
