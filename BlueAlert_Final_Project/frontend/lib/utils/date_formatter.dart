class DateFormatter {
  DateFormatter._();

  static String format(DateTime dateTime) {
    final DateTime localDateTime = dateTime.toLocal();

    final String year = localDateTime.year.toString();
    final String month = localDateTime.month.toString().padLeft(2, '0');
    final String day = localDateTime.day.toString().padLeft(2, '0');
    final String hour = localDateTime.hour.toString().padLeft(2, '0');
    final String minute = localDateTime.minute.toString().padLeft(2, '0');

    return '$year-$month-$day $hour:$minute';
  }
}
