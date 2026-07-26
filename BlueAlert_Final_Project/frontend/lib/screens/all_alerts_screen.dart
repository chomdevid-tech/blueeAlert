import 'package:flutter/material.dart';

import '../config/app_constants.dart';
import '../data/alert_repository.dart';
import '../models/security_alert.dart';
import '../widgets/alert_card.dart';
import '../widgets/empty_view.dart';
import '../widgets/error_view.dart';
import '../widgets/filter_dropdown.dart';
import '../widgets/loading_view.dart';
import 'alert_detail_screen.dart';

class AllAlertsScreen extends StatefulWidget {
  const AllAlertsScreen({
    required this.alertRepository,
    required this.alertsStream,
    super.key,
  });

  final AlertRepository alertRepository;
  final Stream<List<SecurityAlert>> alertsStream;

  @override
  State<AllAlertsScreen> createState() {
    return _AllAlertsScreenState();
  }
}

class _AllAlertsScreenState extends State<AllAlertsScreen> {
  String selectedVm = AppConstants.allFilter;
  String selectedSeverity = AppConstants.allFilter;

  final Set<String> updatingAlertIds = <String>{};

  Future<void> updateStatus(SecurityAlert alert, String newStatus) async {
    setState(() {
      updatingAlertIds.add(alert.alertId);
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

      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text('Update failed: $error')));
    } finally {
      if (mounted) {
        setState(() {
          updatingAlertIds.remove(alert.alertId);
        });
      }
    }
  }

  void openDetails(SecurityAlert alert) {
    Navigator.push(
      context,
      MaterialPageRoute<void>(
        builder: (BuildContext context) {
          return AlertDetailScreen(
            alertRepository: widget.alertRepository,
            alertsStream: widget.alertsStream,
            originalAlert: alert,
          );
        },
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('All Alerts')),
      body: StreamBuilder<List<SecurityAlert>>(
        stream: widget.alertsStream,
        builder:
            (
              BuildContext context,
              AsyncSnapshot<List<SecurityAlert>> snapshot,
            ) {
              if (snapshot.hasError) {
                return const ErrorView(
                  message: 'Could not load security alerts.',
                );
              }

              if (!snapshot.hasData) {
                return const LoadingView();
              }

              final List<SecurityAlert> alerts = widget.alertRepository
                  .filterAlerts(
                    alerts: snapshot.data!,
                    selectedVm: selectedVm,
                    selectedSeverity: selectedSeverity,
                  );

              return Column(
                children: <Widget>[
                  Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      children: <Widget>[
                        FilterDropdown(
                          label: 'Virtual machine',
                          value: selectedVm,
                          options: AppConstants.vmOptions,
                          onChanged: (String value) {
                            setState(() {
                              selectedVm = value;
                            });
                          },
                        ),
                        const SizedBox(height: 12),
                        FilterDropdown(
                          label: 'Severity',
                          value: selectedSeverity,
                          options: AppConstants.severityOptions,
                          onChanged: (String value) {
                            setState(() {
                              selectedSeverity = value;
                            });
                          },
                        ),
                      ],
                    ),
                  ),
                  Expanded(
                    child: alerts.isEmpty
                        ? const EmptyView(message: 'No alerts were found.')
                        : ListView.separated(
                            padding: const EdgeInsets.all(16),
                            itemCount: alerts.length,
                            separatorBuilder:
                                (BuildContext context, int index) {
                                  return const SizedBox(height: 12);
                                },
                            itemBuilder: (BuildContext context, int index) {
                              final SecurityAlert alert = alerts[index];

                              return AlertCard(
                                alert: alert,
                                isUpdating: updatingAlertIds.contains(
                                  alert.alertId,
                                ),
                                onDetails: () {
                                  openDetails(alert);
                                },
                                onInvestigate: alert.status == 'new'
                                    ? () {
                                        updateStatus(alert, 'investigating');
                                      }
                                    : null,
                                onResolve: alert.status != 'resolved'
                                    ? () {
                                        updateStatus(alert, 'resolved');
                                      }
                                    : null,
                              );
                            },
                          ),
                  ),
                ],
              );
            },
      ),
    );
  }
}
