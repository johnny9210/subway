import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'package:smart_subway_guide/app/app.dart';

void main() {
  testWidgets('App smoke test', (WidgetTester tester) async {
    await tester.pumpWidget(
      const ProviderScope(
        child: SmartSubwayApp(),
      ),
    );

    // Verify the app title is displayed
    expect(find.text('METRO-WAY'), findsOneWidget);
  });
}
