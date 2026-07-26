import 'package:flutter/material.dart';

import '../config/app_colors.dart';

class StatusBadge extends StatelessWidget {
  const StatusBadge({required this.status, super.key});

  final String status;

  @override
  Widget build(BuildContext context) {
    Color backgroundColor;
    Color textColor;

    if (status == 'investigating') {
      backgroundColor = AppColors.investigatingSoft;
      textColor = AppColors.investigating;
    } else if (status == 'resolved') {
      backgroundColor = AppColors.resolvedSoft;
      textColor = AppColors.resolved;
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
        status.toUpperCase(),
        style: TextStyle(
          color: textColor,
          fontSize: 11,
          fontWeight: FontWeight.bold,
        ),
      ),
    );
  }
}
