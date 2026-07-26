import 'package:final_project/models/security_alert.dart';
import 'package:final_project/utils/date_formatter.dart';
import 'package:final_project/widgets/severity_badge.dart';
import 'package:final_project/widgets/status_badge.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  group('SecurityAlert model tests', () {
    final Map<String, dynamic> alertJson = <String, dynamic>{
      'alertId': 'alert-test-001',
      'title': 'SQL Injection Detected',
      'description': 'A possible SQL injection attack was detected.',
      'attackType': 'SQL Injection',
      'severity': 'critical',
      'status': 'new',
      'vmName': 'VM1',
      'sourceIp': '192.168.1.50',
      'destinationIp': '192.168.1.10',
      'timestamp': '2026-07-14T16:47:00Z',
      'rawLog': <String, dynamic>{
        'event_type': 'sql_injection',
        'request_path': '/login',
      },
    };

    test('fromJson creates a SecurityAlert object', () {
      final SecurityAlert alert = SecurityAlert.fromJson(alertJson);

      expect(alert.alertId, 'alert-test-001');
      expect(alert.title, 'SQL Injection Detected');
      expect(alert.severity, 'critical');
      expect(alert.status, 'new');
      expect(alert.vmName, 'VM1');
      expect(alert.rawLog['event_type'], 'sql_injection');
    });

    test('toJson converts SecurityAlert to a map', () {
      final SecurityAlert alert = SecurityAlert.fromJson(alertJson);

      final Map<String, dynamic> result = alert.toJson();

      expect(result['alertId'], 'alert-test-001');
      expect(result['attackType'], 'SQL Injection');
      expect(result['severity'], 'critical');
      expect(result['vmName'], 'VM1');
    });

    test('copyWith changes only selected values', () {
      final SecurityAlert originalAlert = SecurityAlert.fromJson(alertJson);

      final SecurityAlert updatedAlert = originalAlert.copyWith(
        status: 'investigating',
      );

      expect(originalAlert.status, 'new');
      expect(updatedAlert.status, 'investigating');

      expect(updatedAlert.alertId, originalAlert.alertId);

      expect(updatedAlert.title, originalAlert.title);
    });

    test('fromJson throws error for invalid timestamp', () {
      final Map<String, dynamic> invalidJson = Map<String, dynamic>.from(
        alertJson,
      );

      invalidJson['timestamp'] = 'not-a-date';

      expect(
        () => SecurityAlert.fromJson(invalidJson),
        throwsA(isA<FormatException>()),
      );
    });
  });

  group('Date formatter tests', () {
    test('formats date and time correctly', () {
      final DateTime dateTime = DateTime(2026, 7, 14, 16, 47);

      final String result = DateFormatter.format(dateTime);

      expect(result, '2026-07-14 16:47');
    });
  });

  group('Badge widget tests', () {
    testWidgets('SeverityBadge displays critical severity', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(body: SeverityBadge(severity: 'critical')),
        ),
      );

      expect(find.text('CRITICAL'), findsOneWidget);
    });

    testWidgets('StatusBadge displays investigating status', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(body: StatusBadge(status: 'investigating')),
        ),
      );

      expect(find.text('INVESTIGATING'), findsOneWidget);
    });
  });
}
