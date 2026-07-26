import unittest

from backend.models.security_alert import SecurityAlert


class SecurityAlertTest(unittest.TestCase):
    def setUp(self) -> None:
        """
        Create valid test alert data before every test.
        """

        self.valid_alert_data = {
            "alertId": "alert-001",
            "title": "Brute Force Attempt Detected",
            "description": (
                "Multiple failed login attempts were detected."
            ),
            "attackType": "Brute Force",
            "severity": "high",
            "status": "new",
            "vmName": "VM1",
            "sourceIp": "192.168.1.105",
            "destinationIp": "192.168.1.10",
            "timestamp": "2026-07-11T20:30:00",
            "rawLog": {
                "event_type": "login_failure",
                "username": "root",
                "message": "Invalid password",
                "attempt_count": 5,
            },
        }

    def test_create_valid_security_alert(self) -> None:
        security_alert = SecurityAlert.from_dict(
            self.valid_alert_data
        )

        self.assertEqual(
            security_alert.alert_id,
            "alert-001",
        )

        self.assertEqual(
            security_alert.attack_type,
            "Brute Force",
        )

        self.assertEqual(
            security_alert.severity,
            "high",
        )

        self.assertEqual(
            security_alert.status,
            "new",
        )

    def test_convert_alert_to_firebase_dictionary(
        self,
    ) -> None:
        security_alert = SecurityAlert.from_dict(
            self.valid_alert_data
        )

        firebase_alert_data = security_alert.to_dict()

        self.assertEqual(
            firebase_alert_data["alertId"],
            "alert-001",
        )

        self.assertEqual(
            firebase_alert_data["attackType"],
            "Brute Force",
        )

        self.assertEqual(
            firebase_alert_data["vmName"],
            "VM1",
        )

        self.assertIn(
            "rawLog",
            firebase_alert_data,
        )

    def test_change_alert_status(self) -> None:
        security_alert = SecurityAlert.from_dict(
            self.valid_alert_data
        )

        investigating_alert = security_alert.with_status(
            "investigating"
        )

        self.assertEqual(
            security_alert.status,
            "new",
        )

        self.assertEqual(
            investigating_alert.status,
            "investigating",
        )

        self.assertEqual(
            investigating_alert.alert_id,
            security_alert.alert_id,
        )

    def test_invalid_severity_raises_error(self) -> None:
        invalid_alert_data = self.valid_alert_data.copy()

        invalid_alert_data["severity"] = "low"

        with self.assertRaises(ValueError):
            SecurityAlert.from_dict(invalid_alert_data)

    def test_invalid_status_raises_error(self) -> None:
        invalid_alert_data = self.valid_alert_data.copy()

        invalid_alert_data["status"] = "closed"

        with self.assertRaises(ValueError):
            SecurityAlert.from_dict(invalid_alert_data)

    def test_invalid_vm_name_raises_error(self) -> None:
        invalid_alert_data = self.valid_alert_data.copy()

        invalid_alert_data["vmName"] = "VM9"

        with self.assertRaises(ValueError):
            SecurityAlert.from_dict(invalid_alert_data)

    def test_invalid_raw_log_raises_error(self) -> None:
        invalid_alert_data = self.valid_alert_data.copy()

        invalid_alert_data["rawLog"] = "Invalid raw log"

        with self.assertRaises(ValueError):
            SecurityAlert.from_dict(invalid_alert_data)

    def test_invalid_new_status_raises_error(self) -> None:
        security_alert = SecurityAlert.from_dict(
            self.valid_alert_data
        )

        with self.assertRaises(ValueError):
            security_alert.with_status("closed")


if __name__ == "__main__":
    unittest.main()