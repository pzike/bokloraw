// This is a basic Flutter widget test.
//
// To perform an interaction with a widget in your test, use the WidgetTester
// utility in the flutter_test package. For example, you can send tap and scroll
// gestures. You can also use WidgetTester to find child widgets in the widget
// tree, read text, and verify that the values of widget properties are correct.

import 'package:flutter_test/flutter_test.dart';

import 'package:lora_drainage_monitor/main.dart';

void main() {
  testWidgets('Drainage monitor preview renders', (WidgetTester tester) async {
    await tester.pumpWidget(const DrainageApp());

    expect(find.text('Drainage monitor'), findsOneWidget);
    expect(find.text('Water level'), findsOneWidget);
    expect(find.text('All normal'), findsNothing);
  });
}
