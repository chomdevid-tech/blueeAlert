import 'package:firebase_database/firebase_database.dart';
import 'package:flutter/foundation.dart';

import '../config/app_constants.dart';
import '../models/security_alert.dart';

class FirebaseAlertService {
  FirebaseAlertService()
    : _alertsReference = FirebaseDatabase.instance.ref(AppConstants.alertsPath);

  final DatabaseReference _alertsReference;

  Stream<List<SecurityAlert>> watchAlerts() {
    // DatabaseEvent is package from firefox 
    // snapshot picture the latest data 
    // data inside 
    return _alertsReference.onValue.map((DatabaseEvent event) {
      // value is watch everything inside event
      final Object? firebaseValue = event.snapshot.value;

      if (firebaseValue == null) {
        return <SecurityAlert>[];
      }

      if (firebaseValue is! Map) {
        throw const FormatException('Firebase alerts must be an object.');
      }

      final List<SecurityAlert> alerts = <SecurityAlert>[];
     
      for (final MapEntry<dynamic, dynamic> entry in firebaseValue.entries) {
        if (entry.value is! Map) {
          continue; // make sure it not stop 
        }

        try {
          final Map<String, dynamic> alertJson = _convertMap(
            entry.value as Map,
          );

          alertJson['alertId'] ??= entry.key.toString();

          final SecurityAlert alert = SecurityAlert.fromJson(alertJson);

          alerts.add(alert);
        } catch (error) {
          debugPrint('Invalid alert ${entry.key}: $error');
        }
      }
     // show alert by compare time 
      alerts.sort((SecurityAlert firstAlert, SecurityAlert secondAlert) {
        return secondAlert.timestamp.compareTo(firstAlert.timestamp);
      });

      return alerts;
    });
  }

  Future<void> updateAlertStatus(String alertId, String newStatus) async {
    final String cleanedStatus = newStatus.trim().toLowerCase();

    if (!AppConstants.allowedStatuses.contains(cleanedStatus)) {
      throw ArgumentError('Invalid status: $cleanedStatus');
    }

    await _alertsReference.child(alertId).child('status').set(cleanedStatus);  // child is use for like /id/status/
  }

  static Map<String, dynamic> _convertMap(Map<dynamic, dynamic> originalMap) {
    final Map<String, dynamic> convertedMap = <String, dynamic>{};

    for (final MapEntry<dynamic, dynamic> entry in originalMap.entries) {
      convertedMap[entry.key.toString()] = _convertValue(entry.value);
    }

    return convertedMap;
  }

  static dynamic _convertValue(dynamic value) {
    if (value is Map) {
      return _convertMap(value);
    }

    if (value is List) {
      return value.map<dynamic>(_convertValue).toList();
    }

    return value;
  }
}
