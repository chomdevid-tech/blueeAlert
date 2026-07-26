import 'package:flutter/material.dart';

import '../data/alert_repository.dart';
import '../models/security_alert.dart';
import '../widgets/alert_card.dart';
import '../widgets/dashboard_stat_card.dart';
import '../widgets/empty_view.dart';
import '../widgets/error_view.dart';
import '../widgets/loading_view.dart';
import 'alert_detail_screen.dart';

class DashboardScreen extends StatelessWidget {
  const DashboardScreen({
    required this.alertRepository,
    required this.alertsStream,
    required this.onOpenPage,
    super.key,
  });

  final AlertRepository alertRepository;
  final Stream<List<SecurityAlert>> alertsStream;
  final ValueChanged<int> onOpenPage;

  void openDetails(BuildContext context, SecurityAlert alert) {
    Navigator.push(
      context,
      MaterialPageRoute<void>(
        builder: (BuildContext context) {
          return AlertDetailScreen(
            alertRepository: alertRepository,
            alertsStream: alertsStream,
            originalAlert: alert,
          );
        },
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'BlueAlert Dashboard',
          style: TextStyle(fontWeight: FontWeight.bold),
        ),
      ),
      body: StreamBuilder<List<SecurityAlert>>(
        stream: alertsStream,
        builder:
            (
              BuildContext context,
              AsyncSnapshot<List<SecurityAlert>> snapshot,
            ) {
              if (snapshot.hasError) {
                return const ErrorView(
                  message:
                      'Could not load alerts. Check Firebase and your internet.',
                );
              }

              if (!snapshot.hasData) {
                return const LoadingView();
              }

              final List<SecurityAlert> alerts = snapshot.data!;

              final int investigatingCount = alerts
                  .where(
                    (SecurityAlert alert) => alert.status == 'investigating',
                  )
                  .length;

              final int resolvedCount = alerts
                  .where((SecurityAlert alert) => alert.status == 'resolved')
                  .length;

              final List<SecurityAlert> recentAlerts = alerts.take(5).toList();

              return ListView(
                padding: const EdgeInsets.all(16),
                children: <Widget>[
                  DashboardStatCard(
                    title: 'Total alerts',
                    value: alerts.length,
                    icon: Icons.warning_amber,
                    onTap: () => onOpenPage(1),
                  ),
                  const SizedBox(height: 12),
                  DashboardStatCard(
                    title: 'Investigating',
                    value: investigatingCount,
                    icon: Icons.search,
                    onTap: () => onOpenPage(2),
                  ),
                  const SizedBox(height: 12),
                  DashboardStatCard(
                    title: 'Resolved',
                    value: resolvedCount,
                    icon: Icons.check_circle_outline,
                    onTap: () => onOpenPage(3),
                  ),
                  const SizedBox(height: 26),
                  Row(
                    children: <Widget>[
                      const Expanded(
                        child: Text(
                          'Recent alerts',
                          style: TextStyle(
                            fontSize: 21,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                      TextButton(
                        onPressed: () => onOpenPage(1),
                        child: const Text('View all'),
                      ),
                    ],
                  ),
                  const SizedBox(height: 12),
                  if (recentAlerts.isEmpty)
                    const SizedBox(
                      height: 250,
                      child: EmptyView(
                        message: 'No security alerts were found.',
                      ),
                    )
                  else
                    ...recentAlerts.map((SecurityAlert alert) {
                      return Padding(
                        padding: const EdgeInsets.only(bottom: 12),
                        child: AlertCard(
                          alert: alert,
                          onDetails: () {
                            openDetails(context, alert);
                          },
                        ),
                      );
                    }),
                ],
              );
            },
      ),
    );
  }
}
