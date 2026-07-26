import 'package:final_project/models/security_alert.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  final Map<String, dynamic> alertJson = <String, dynamic>{
    'alertId': 'alert-test-001',
    'title': 'Brute Force Attempt Detected',
    'description': 'Multiple failed login attempts were detected.',
    'attackType': 'Brute Force',
    'severity': 'high',
    'status': 'new',
    'vmName': 'VM1',
    'sourceIp': '192.168.1.105',
    'destinationIp': '192.168.1.10',
    'timestamp': '2026-07-11T22:30:00Z',
    'rawLog': <String, dynamic>{
      'event_type': 'login_failure',
      'attempt_count': 7,
    },
  };

  test('fromJson creates SecurityAlert', () {
    final SecurityAlert alert = SecurityAlert.fromJson(alertJson);

    expect(alert.alertId, 'alert-test-001');
    expect(alert.severity, 'high');
    expect(alert.rawLog['attempt_count'], 7);
  });

  test('toJson creates a map', () {
    final SecurityAlert alert = SecurityAlert.fromJson(alertJson);

    final Map<String, dynamic> result = alert.toJson();

    expect(result['attackType'], 'Brute Force');
    expect(result['vmName'], 'VM1');
  });

  test('copyWith changes status', () {
    final SecurityAlert originalAlert = SecurityAlert.fromJson(alertJson);

    final SecurityAlert investigatingAlert = originalAlert.copyWith(
      status: 'investigating',
    );

    expect(originalAlert.status, 'new');
    expect(investigatingAlert.status, 'investigating');
    expect(investigatingAlert.alertId, originalAlert.alertId);
  });
}
