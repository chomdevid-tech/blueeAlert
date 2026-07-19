import 'package:flutter/material.dart';

class SeverityBadge extends StatelessWidget {
  const SeverityBadge({required this.severity, super.key});

  final String severity;

  @override
  Widget build(BuildContext context) {
    Color backgroundColor;

    if (severity == 'critical') {
      backgroundColor = const Color(0xFF7F1D1D);
    } else if (severity == 'high') {
      backgroundColor = const Color(0xFFDC2626);
    } else if (severity == 'medium') {
      backgroundColor = const Color(0xFFF59E0B);
    } else {
      backgroundColor = Colors.grey;
    }

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
      decoration: BoxDecoration(
        color: backgroundColor,
        borderRadius: BorderRadius.circular(20),
      ),
      child: Text(
        severity.toUpperCase(),
        style: const TextStyle(
          color: Colors.white,
          fontSize: 11,
          fontWeight: FontWeight.bold,
        ),
      ),
    );
  }
}
