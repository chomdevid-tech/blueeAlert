import 'dart:convert';

import 'package:flutter/material.dart';

import '../config/app_colors.dart';
import '../data/alert_repository.dart';
import '../models/security_alert.dart';
import '../utils/date_formatter.dart';
import '../widgets/severity_badge.dart';
import '../widgets/status_badge.dart';

class AlertDetailScreen extends StatefulWidget {
  const AlertDetailScreen({
    required this.alertRepository,
    required this.alertsStream,
    required this.originalAlert,
    super.key,
  });

  final AlertRepository alertRepository;
  final Stream<List<SecurityAlert>> alertsStream;
  final SecurityAlert originalAlert;

  @override
  State<AlertDetailScreen> createState() => _AlertDetailScreenState();
}

class _AlertDetailScreenState extends State<AlertDetailScreen> {
  bool isUpdating = false;

  Future<void> updateStatus(SecurityAlert alert, String newStatus) async {
    setState(() {
      isUpdating = true;
    });

    try {
      await widget.alertRepository.updateStatus(alert.alertId, newStatus);

      if (!mounted) {
        return;
      }

      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text('Alert changed to $newStatus.')));
    } catch (error) {
      if (!mounted) {
        return;
      }

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Could not update alert status.')),
      );
    } finally {
      if (mounted) {
        setState(() {
          isUpdating = false;
        });
      }
    }
  }

  SecurityAlert findCurrentAlert(List<SecurityAlert> alerts) {
    for (final SecurityAlert alert in alerts) {
      if (alert.alertId == widget.originalAlert.alertId) {
        return alert;
      }
    }

    return widget.originalAlert;
  }

  @override
  Widget build(BuildContext context) {
    return StreamBuilder<List<SecurityAlert>>(
      stream: widget.alertsStream,
      initialData: <SecurityAlert>[widget.originalAlert],
      builder:
          (BuildContext context, AsyncSnapshot<List<SecurityAlert>> snapshot) {
            final List<SecurityAlert> alerts =
                snapshot.data ?? <SecurityAlert>[widget.originalAlert];

            final SecurityAlert alert = findCurrentAlert(alerts);

            final String rawJson = const JsonEncoder.withIndent(
              '  ',
            ).convert(alert.rawLog);

            return Scaffold(
              appBar: AppBar(title: const Text('Alert Details')),
              body: ListView(
                padding: const EdgeInsets.all(16),
                children: <Widget>[
                  Text(
                    alert.title,
                    style: const TextStyle(
                      color: AppColors.textPrimary,
                      fontSize: 25,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 12),
                  Wrap(
                    spacing: 8,
                    runSpacing: 8,
                    children: <Widget>[
                      SeverityBadge(severity: alert.severity),
                      StatusBadge(status: alert.status),
                    ],
                  ),
                  const SizedBox(height: 22),
                  _DetailRow(label: 'Attack type', value: alert.attackType),
                  _DetailRow(label: 'VM', value: alert.vmName),
                  _DetailRow(label: 'Source IP', value: alert.sourceIp),
                  _DetailRow(
                    label: 'Destination IP',
                    value: alert.destinationIp,
                  ),
                  _DetailRow(
                    label: 'Timestamp',
                    value: DateFormatter.format(alert.timestamp),
                  ),
                  const SizedBox(height: 12),
                  const Text(
                    'Description',
                    style: TextStyle(fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 6),
                  Text(alert.description),
                  const SizedBox(height: 22),
                  const Text(
                    'Raw security log',
                    style: TextStyle(fontSize: 19, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 10),
                  Container(
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: AppColors.primaryPale,
                      border: Border.all(color: AppColors.border),
                      borderRadius: BorderRadius.circular(14),
                    ),
                    child: SelectableText(
                      rawJson,
                      style: const TextStyle(
                        color: AppColors.textPrimary,
                        fontFamily: 'monospace',
                      ),
                    ),
                  ),
                  if (isUpdating) ...<Widget>[
                    const SizedBox(height: 16),
                    const LinearProgressIndicator(),
                  ],
                  if (alert.status == 'new') ...<Widget>[
                    const SizedBox(height: 16),
                    OutlinedButton(
                      onPressed: isUpdating
                          ? null
                          : () => updateStatus(alert, 'investigating'),
                      child: const Text('Add to Investigating'),
                    ),
                  ],
                  if (alert.status != 'resolved') ...<Widget>[
                    const SizedBox(height: 10),
                    FilledButton(
                      onPressed: isUpdating
                          ? null
                          : () => updateStatus(alert, 'resolved'),
                      child: const Text('Add to Resolved'),
                    ),
                  ],
                ],
              ),
            );
          },
    );
  }
}

class _DetailRow extends StatelessWidget {
  const _DetailRow({required this.label, required this.value});

  final String label;
  final String value;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 10),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: <Widget>[
          SizedBox(
            width: 120,
            child: Text(
              label,
              style: const TextStyle(color: AppColors.textSecondary),
            ),
          ),
          Expanded(
            child: Text(
              value,
              style: const TextStyle(fontWeight: FontWeight.w600),
            ),
          ),
        ],
      ),
    );
  }
}
