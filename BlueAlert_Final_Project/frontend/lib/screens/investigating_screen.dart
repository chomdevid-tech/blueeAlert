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

class InvestigatingScreen extends StatefulWidget {
  const InvestigatingScreen({
    required this.alertRepository,
    required this.alertsStream,
    super.key,
  });

  final AlertRepository alertRepository;
  final Stream<List<SecurityAlert>> alertsStream;

  @override
  State<InvestigatingScreen> createState() {
    return _InvestigatingScreenState();
  }
}

class _InvestigatingScreenState extends State<InvestigatingScreen> {
  String selectedVm = AppConstants.allFilter;

  final Set<String> updatingAlertIds = <String>{};

  Future<void> resolveAlert(SecurityAlert alert) async {
    setState(() {
      updatingAlertIds.add(alert.alertId);
    });

    try {
      await widget.alertRepository.updateStatus(alert.alertId, 'resolved');

      if (!mounted) {
        return;
      }

      ScaffoldMessenger.of(
        context,
      ).showSnackBar(const SnackBar(content: Text('Alert resolved.')));
    } catch (error) {
      if (!mounted) {
        return;
      }

      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text('Resolve failed: $error')));
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
            alertRepository: widget.alertRepository, // pass the repo
            alertsStream: widget.alertsStream, // reciveve live change
            originalAlert: alert,// select which alert display 
          );
        },
      ),
    );
  }
// Use widget. inside the State class of a StatefulWidget when the value was declared in the widget class.
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Investigating')),
      body: StreamBuilder<List<SecurityAlert>>(
        stream: widget.alertsStream,
        builder:
            (
              BuildContext context,
              AsyncSnapshot<List<SecurityAlert>> snapshot,
            ) {
              if (snapshot.hasError) {
                return const ErrorView(
                  message: 'Could not load investigating alerts.',
                );
              }

              if (!snapshot.hasData) {
                return const LoadingView();
              }

              final List<SecurityAlert> alerts = widget.alertRepository
                  .filterAlerts(
                    alerts: snapshot.data!,
                    selectedVm: selectedVm,
                    requiredStatus: 'investigating',
                  );

              return Column(
                children: <Widget>[
                  Padding(
                    padding: const EdgeInsets.all(16),
                    child: FilterDropdown(
                      label: 'Virtual machine',
                      value: selectedVm,
                      options: AppConstants.vmOptions,
                      onChanged: (String value) {
                        setState(() {
                          selectedVm = value;
                        });
                      },
                    ),
                  ),
                  Expanded(
                    child: alerts.isEmpty
                        ? const EmptyView(message: 'No investigating alerts.')
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
                                onResolve: () {
                                  resolveAlert(alert);
                                },
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
