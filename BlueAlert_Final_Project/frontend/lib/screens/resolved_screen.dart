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

class ResolvedScreen extends StatefulWidget {
  const ResolvedScreen({
    required this.alertRepository,
    required this.alertsStream,
    super.key,
  });

  final AlertRepository alertRepository;
  final Stream<List<SecurityAlert>> alertsStream;

  @override
  State<ResolvedScreen> createState() {
    return _ResolvedScreenState();
  }
}

class _ResolvedScreenState extends State<ResolvedScreen> {
  String selectedVm = AppConstants.allFilter;

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
      appBar: AppBar(title: const Text('Resolved')),
      body: StreamBuilder<List<SecurityAlert>>(
        stream: widget.alertsStream,
        builder:
            (
              BuildContext context,
              AsyncSnapshot<List<SecurityAlert>> snapshot,
            ) {
              if (snapshot.hasError) {
                return const ErrorView(
                  message: 'Could not load resolved alerts.',
                );
              }

              if (!snapshot.hasData) {
                return const LoadingView();
              }

              final List<SecurityAlert> alerts = widget.alertRepository
                  .filterAlerts(
                    alerts: snapshot.data!,
                    selectedVm: selectedVm,
                    requiredStatus: 'resolved',
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
                        ? const EmptyView(message: 'No resolved alerts.')
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
                                onDetails: () {
                                  openDetails(alert);
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
