import 'package:flutter/material.dart';

import '../config/app_colors.dart';

class SeverityBadge extends StatelessWidget {
  const SeverityBadge({required this.severity, super.key});

  final String severity;

  @override
  Widget build(BuildContext context) {
    Color backgroundColor;
    Color textColor;

    if (severity == 'critical') {
      backgroundColor = AppColors.criticalSoft;
      textColor = AppColors.critical;
    } else if (severity == 'high') {
      backgroundColor = AppColors.highSoft;
      textColor = AppColors.high;
    } else if (severity == 'medium') {
      backgroundColor = AppColors.mediumSoft;
      textColor = AppColors.medium;
    } else {
      backgroundColor = AppColors.newStatusSoft;
      textColor = AppColors.newStatus;
    }

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
      decoration: BoxDecoration(
        color: backgroundColor,
        borderRadius: BorderRadius.circular(20),
      ),
      child: Text(
        severity.toUpperCase(),
        style: TextStyle(
          color: textColor,
          fontSize: 11,
          fontWeight: FontWeight.bold,
        ),
      ),
    );
  }
}
