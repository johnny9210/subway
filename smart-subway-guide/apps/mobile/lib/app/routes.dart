import 'package:flutter/material.dart';

import '../features/boarding/presentation/screens/arrival_complete_screen.dart';
import '../features/boarding/presentation/screens/boarding_screen.dart';
import '../features/boarding/presentation/screens/home_screen.dart';
import '../features/boarding/presentation/screens/train_arrival_screen.dart';
import '../features/settings/presentation/screens/settings_screen.dart';

class AppRoutes {
  static const String home = '/';
  static const String trainArrival = '/train-arrival';
  static const String boarding = '/boarding';
  static const String arrivalComplete = '/arrival-complete';
  static const String settings = '/settings';

  static Route<dynamic> generateRoute(RouteSettings settings) {
    switch (settings.name) {
      case home:
        return MaterialPageRoute(
          builder: (_) => const HomeScreen(),
        );
      case trainArrival:
        final args = settings.arguments as Map<String, dynamic>?;
        return MaterialPageRoute(
          builder: (_) => TrainArrivalScreen(
            stationName: args?['stationName'] as String?,
          ),
        );
      case boarding:
        return MaterialPageRoute(
          builder: (_) => const BoardingScreen(),
        );
      case arrivalComplete:
        final args = settings.arguments as Map<String, dynamic>?;
        return MaterialPageRoute(
          builder: (_) => ArrivalCompleteScreen(
            stationName: args?['stationName'] as String?,
            actualTime: args?['actualTime'] as String?,
            predictedTime: args?['predictedTime'] as String?,
          ),
        );
      case AppRoutes.settings:
        return MaterialPageRoute(
          builder: (_) => const SettingsScreen(),
        );
      default:
        return MaterialPageRoute(
          builder: (_) => Scaffold(
            body: Center(
              child: Text('Route not found: ${settings.name}'),
            ),
          ),
        );
    }
  }
}
