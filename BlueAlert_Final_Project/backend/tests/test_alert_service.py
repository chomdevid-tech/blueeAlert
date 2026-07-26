import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from backend.models.security_alert import SecurityAlert
from backend.services.alert_service import (
    AlertService,
    DuplicateAlertError,
)


class AlertServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        """
        Create temporary storage and one valid alert.
        """

        self.temporary_directory = TemporaryDirectory()

        self.generated_alerts_directory = (
            Path(self.temporary_directory.name)
            / "generated_alerts"
        )

        self.alert_service = AlertService(
            generated_alerts_directory=(
                self.generated_alerts_directory
            )
        )

        self.security_alert = SecurityAlert.from_dict(
            {
                "alertId": "alert-test-001",
                "title": "Brute Force Attempt Detected",
                "description": (
                    "Multiple failed login attempts "
                    "were detected."
                ),
                "attackType": "Brute Force",
                "severity": "high",
                "status": "new",
                "vmName": "VM1",
                "sourceIp": "192.168.1.105",
                "destinationIp": "192.168.1.10",
                "timestamp": "2026-07-11T21:30:00Z",
                "rawLog": {
                    "log_id": "log-test-001",
                    "event_type": "login_failure",
                    "username": "root",
                    "message": "Invalid password",
                    "attempt_count": 5,
                },
            }
        )

    def tearDown(self) -> None:
        """
        Delete the temporary test folder.
        """

        self.temporary_directory.cleanup()

    def test_save_generated_alert(self) -> None:
        saved_alert_path = (
            self.alert_service.save_generated_alert(
                self.security_alert
            )
        )

        self.assertTrue(
            saved_alert_path.exists()
        )

        self.assertEqual(
            saved_alert_path.name,
            "alert-test-001.jsonl",
        )

    def test_saved_alert_contains_valid_json(
        self,
    ) -> None:
        saved_alert_path = (
            self.alert_service.save_generated_alert(
                self.security_alert
            )
        )

        saved_lines = (
            saved_alert_path
            .read_text(encoding="utf-8")
            .splitlines()
        )

        self.assertEqual(
            len(saved_lines),
            1,
        )

        saved_alert_data = json.loads(
            saved_lines[0]
        )

        self.assertEqual(
            saved_alert_data["alertId"],
            "alert-test-001",
        )

        self.assertEqual(
            saved_alert_data["attackType"],
            "Brute Force",
        )

        self.assertEqual(
            saved_alert_data["severity"],
            "high",
        )

        self.assertEqual(
            saved_alert_data["status"],
            "new",
        )

        self.assertEqual(
            saved_alert_data["rawLog"][
                "attempt_count"
            ],
            5,
        )

    def test_duplicate_alert_raises_error(
        self,
    ) -> None:
        self.alert_service.save_generated_alert(
            self.security_alert
        )

        with self.assertRaises(
            DuplicateAlertError
        ):
            self.alert_service.save_generated_alert(
                self.security_alert
            )


if __name__ == "__main__":
    unittest.main()