import 'package:flutter/material.dart';

import '../models/security_alert.dart';
import '../utils/date_formatter.dart';
import 'severity_badge.dart';
import 'status_badge.dart';

class AlertCard extends StatelessWidget {
  const AlertCard({required this.alert, super.key});

  final SecurityAlert alert;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        border: Border.all(color: const Color(0xFFD4D4D4)),
        borderRadius: BorderRadius.circular(16),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: <Widget>[
          Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: <Widget>[
              Expanded(
                child: Text(
                  alert.title,
                  style: const TextStyle(
                    fontSize: 17,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
              const SizedBox(width: 8),
              SeverityBadge(severity: alert.severity),
            ],
          ),
          const SizedBox(height: 10),
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: <Widget>[
              StatusBadge(status: alert.status),
              Chip(label: Text(alert.vmName)),
              Chip(label: Text(alert.attackType)),
            ],
          ),
          const SizedBox(height: 10),
          Text('Source IP: ${alert.sourceIp}'),
          const SizedBox(height: 4),
          Text('Destination IP: ${alert.destinationIp}'),
          const SizedBox(height: 4),
          Text(
            DateFormatter.format(alert.timestamp),
            style: const TextStyle(color: Colors.grey, fontSize: 13),
          ),
        ],
      ),
    );
  }
}
