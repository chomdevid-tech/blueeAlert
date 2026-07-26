class AppConstants {
  AppConstants._();

  static const String alertsPath = 'alerts';
  static const String allFilter = 'All';

  static const List<String> vmOptions = <String>['All', 'VM1', 'VM2', 'VM3'];

  static const List<String> severityOptions = <String>[
    'All',
    'medium',
    'high',
    'critical',
  ];

  static const List<String> allowedStatuses = <String>[
    'new',
    'investigating',
    'resolved',
  ];
}
