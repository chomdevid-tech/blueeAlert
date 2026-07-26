class SecurityAlert {
  final String alertId;
  final String title;
  final String description;
  final String attackType;
  final String severity;
  final String status;
  final String vmName;
  final String sourceIp;
  final String destinationIp;
  final DateTime timestamp;
  final Map<String, dynamic> rawLog;

  const SecurityAlert({
    required this.alertId,
    required this.title,
    required this.description,
    required this.attackType,
    required this.severity,
    required this.status,
    required this.vmName,
    required this.sourceIp,
    required this.destinationIp,
    required this.timestamp,
    required this.rawLog,
  });

  factory SecurityAlert.fromJson(Map<String, dynamic> json) {
    final String timestampText = json['timestamp'].toString();

    final DateTime? parsedTimestamp = DateTime.tryParse(timestampText);

    if (parsedTimestamp == null) {
      throw const FormatException('Invalid alert timestamp.');
    }

    final dynamic rawLogValue = json['rawLog'];

    if (rawLogValue is! Map) {
      throw const FormatException('rawLog must be a JSON object.');
    }

    return SecurityAlert(
      alertId: json['alertId'].toString(),
      title: json['title'].toString(),
      description: json['description'].toString(),
      attackType: json['attackType'].toString(),
      severity: json['severity'].toString().toLowerCase(),
      status: json['status'].toString().toLowerCase(),
      vmName: json['vmName'].toString(),
      sourceIp: json['sourceIp'].toString(),
      destinationIp: json['destinationIp'].toString(),
      timestamp: parsedTimestamp,
      rawLog: Map<String, dynamic>.from(rawLogValue),
    );
  }

  Map<String, dynamic> toJson() {
    return <String, dynamic>{
      'alertId': alertId,
      'title': title,
      'description': description,
      'attackType': attackType,
      'severity': severity,
      'status': status,
      'vmName': vmName,
      'sourceIp': sourceIp,
      'destinationIp': destinationIp,
      'timestamp': timestamp.toUtc().toIso8601String(),
      'rawLog': rawLog,
    };
  }

  SecurityAlert copyWith({
    String? alertId,
    String? title,
    String? description,
    String? attackType,
    String? severity,
    String? status,
    String? vmName,
    String? sourceIp,
    String? destinationIp,
    DateTime? timestamp,
    Map<String, dynamic>? rawLog,
  }) {
    return SecurityAlert(
      alertId: alertId ?? this.alertId,
      title: title ?? this.title,
      description: description ?? this.description,
      attackType: attackType ?? this.attackType,
      severity: severity ?? this.severity,
      status: status ?? this.status,
      vmName: vmName ?? this.vmName,
      sourceIp: sourceIp ?? this.sourceIp,
      destinationIp: destinationIp ?? this.destinationIp,
      timestamp: timestamp ?? this.timestamp,
      rawLog: rawLog ?? this.rawLog,
    );
  }
}
