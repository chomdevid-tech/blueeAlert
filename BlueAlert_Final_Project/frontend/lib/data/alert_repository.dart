import '../config/app_constants.dart';
import '../models/security_alert.dart';
import 'firebase_alert_service.dart';

class AlertRepository {
  const AlertRepository(this._firebaseAlertService);

  final FirebaseAlertService _firebaseAlertService;

  Stream<List<SecurityAlert>> watchAlerts() {
    return _firebaseAlertService.watchAlerts();
  }

  Future<void> updateStatus(String alertId, String newStatus) {
    return _firebaseAlertService.updateAlertStatus(alertId, newStatus);
  }

  List<SecurityAlert> filterAlerts({
    required List<SecurityAlert> alerts,
    String selectedVm = AppConstants.allFilter,
    String selectedSeverity = AppConstants.allFilter,
    String? requiredStatus,
  }) {
    return alerts.where((SecurityAlert alert) {
      final bool matchesVm =
          selectedVm == AppConstants.allFilter || alert.vmName == selectedVm;

      final bool matchesSeverity =
          selectedSeverity == AppConstants.allFilter ||
          alert.severity == selectedSeverity;

      final bool matchesStatus =
          requiredStatus == null || alert.status == requiredStatus;

      return matchesVm && matchesSeverity && matchesStatus;
    }).toList();
  }
}
