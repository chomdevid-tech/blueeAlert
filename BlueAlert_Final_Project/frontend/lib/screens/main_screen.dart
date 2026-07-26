import 'package:flutter/material.dart';

import '../data/alert_repository.dart';
import '../models/security_alert.dart';
import '../services/authentication_service.dart';
import 'all_alerts_screen.dart';
import 'dashboard_screen.dart';
import 'investigating_screen.dart';
import 'resolved_screen.dart';

class MainScreen extends StatefulWidget {
  const MainScreen({
    required this.alertRepository,
    required this.authenticationService,
    super.key,
  });

  final AlertRepository alertRepository;

  final AuthenticationService authenticationService;

  @override
  State<MainScreen> createState() {
    return _MainScreenState();
  }
}

class _MainScreenState extends State<MainScreen> {
  int selectedPageIndex = 0;

  late final Stream<List<SecurityAlert>> alertsStream;
  //Create the variable now, assign it later once, and never replace it afterward.

  @override
  void initState() {
    super.initState();
    // .asBroadcastStream() allows multiple screens to listen to the same stream
    alertsStream = widget.alertRepository.watchAlerts().asBroadcastStream();
  }
 
  Future<void> selectDestination(int pageIndex) async {
    if (pageIndex == 4) {
      await confirmLogout();
      return;
    }

    setState(() {
      selectedPageIndex = pageIndex;
    });
  }

  Future<void> confirmLogout() async {
    final bool? shouldLogout = await showDialog<bool>(
      context: context,
      builder: (BuildContext dialogContext) {
        return AlertDialog(
          title: const Text('Logout'),
          content: const Text('Are you sure you want to log out?'),
          actions: <Widget>[
            TextButton(
              onPressed: () {
                Navigator.pop(dialogContext, false);
              },
              child: const Text('Cancel'),
            ),
            FilledButton(
              onPressed: () {
                Navigator.pop(dialogContext, true);
              },
              child: const Text('Logout'),
            ),
          ],
        );
      },
    );

    if (shouldLogout == true) {
      await widget.authenticationService.logout();
    }
  }

  void openPage(int pageIndex) {
    setState(() {
      selectedPageIndex = pageIndex;
    });
  }

  @override
  Widget build(BuildContext context) {
    final List<Widget> pages = <Widget>[
      DashboardScreen(
        alertRepository: widget.alertRepository,
        alertsStream: alertsStream,
        onOpenPage: openPage,
      ),
      AllAlertsScreen(
        alertRepository: widget.alertRepository,
        alertsStream: alertsStream,
      ),
      InvestigatingScreen(
        alertRepository: widget.alertRepository,
        alertsStream: alertsStream,
      ),
      ResolvedScreen(
        alertRepository: widget.alertRepository,
        alertsStream: alertsStream,
      ),
    ];

    return Scaffold(
      body: IndexedStack(index: selectedPageIndex, children: pages),
      bottomNavigationBar: NavigationBar(
        selectedIndex: selectedPageIndex,
        onDestinationSelected: selectDestination,
        destinations: const <NavigationDestination>[
          NavigationDestination(
            icon: Icon(Icons.dashboard_outlined),
            selectedIcon: Icon(Icons.dashboard),
            label: 'Dashboard',
          ),
          NavigationDestination(
            icon: Icon(Icons.warning_amber_outlined),
            selectedIcon: Icon(Icons.warning),
            label: 'All Alerts',
          ),
          NavigationDestination(
            icon: Icon(Icons.search_outlined),
            selectedIcon: Icon(Icons.search),
            label: 'Investigating',
          ),
          NavigationDestination(
            icon: Icon(Icons.check_circle_outline),
            selectedIcon: Icon(Icons.check_circle),
            label: 'Resolved',
          ),
          NavigationDestination(icon: Icon(Icons.logout), label: 'Logout'),
        ],
      ),
    );
  }
}
