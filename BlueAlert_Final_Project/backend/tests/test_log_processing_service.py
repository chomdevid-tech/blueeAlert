import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock

from backend.models.security_log import SecurityLog
from backend.rules.rule_engine import RuleEngine
from backend.services.alert_service import AlertService
from backend.services.firebase_service import (
    FirebaseService,
    FirebaseServiceError,
)
from backend.services.log_processing_service import (
    LogProcessingError,
    LogProcessingService,
)
from backend.services.log_service import LogService


class LogProcessingServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        """
        Create temporary storage folders before every test.
        """

        self.temporary_directory = TemporaryDirectory()

        storage_directory = Path(
            self.temporary_directory.name
        )

        self.raw_logs_directory = (
            storage_directory / "raw_logs"
        )

        self.processed_logs_directory = (
            storage_directory / "processed_logs"
        )

        self.failed_logs_directory = (
            storage_directory / "failed_logs"
        )

        self.generated_alerts_directory = (
            storage_directory / "generated_alerts"
        )

        self.log_service = LogService(
            raw_logs_directory=(
                self.raw_logs_directory
            ),
            processed_logs_directory=(
                self.processed_logs_directory
            ),
            failed_logs_directory=(
                self.failed_logs_directory
            ),
        )

        self.alert_service = AlertService(
            generated_alerts_directory=(
                self.generated_alerts_directory
            )
        )

        self.processing_service = LogProcessingService(
            log_service=self.log_service,
            alert_service=self.alert_service,
            rule_engine=RuleEngine(),
        )

    def tearDown(self) -> None:
        """
        Delete all temporary test files.
        """

        self.temporary_directory.cleanup()

    def create_security_log(
        self,
        event_type: str,
        attempt_count: int | None = None,
    ) -> SecurityLog:
        """
        Create a valid SecurityLog for testing.
        """

        log_data = {
            "log_id": f"log-test-{event_type}",
            "timestamp": "2026-07-11T22:00:00Z",
            "vm_name": "VM1",
            "event_type": event_type,
            "source_ip": "192.168.1.105",
            "destination_ip": "192.168.1.10",
            "message": f"Test event: {event_type}",
            "username": "root",
        }

        if attempt_count is not None:
            log_data["attempt_count"] = attempt_count

        return SecurityLog.from_dict(log_data)

    def test_matching_log_creates_alert(
        self,
    ) -> None:
        """
        A brute-force log should create and save an alert.
        """

        security_log = self.create_security_log(
            event_type="login_failure",
            attempt_count=5,
        )

        raw_log_path = self.log_service.save_raw_log(
            security_log
        )

        generated_alert = (
            self.processing_service.process_log_file(
                raw_log_path
            )
        )

        self.assertIsNotNone(generated_alert)

        self.assertFalse(
            raw_log_path.exists()
        )

        processed_log_path = (
            self.processed_logs_directory
            / raw_log_path.name
        )

        self.assertTrue(
            processed_log_path.exists()
        )

        saved_alert_files = list(
            self.generated_alerts_directory.glob(
                "*.jsonl"
            )
        )

        self.assertEqual(
            len(saved_alert_files),
            1,
        )

        saved_alert_data = json.loads(
            saved_alert_files[0].read_text(
                encoding="utf-8"
            )
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

    def test_normal_login_creates_no_alert(
        self,
    ) -> None:
        """
        A normal login should be processed without an alert.
        """

        security_log = self.create_security_log(
            event_type="login_success"
        )

        raw_log_path = self.log_service.save_raw_log(
            security_log
        )

        generated_alert = (
            self.processing_service.process_log_file(
                raw_log_path
            )
        )

        self.assertIsNone(generated_alert)

        self.assertFalse(
            raw_log_path.exists()
        )

        processed_log_path = (
            self.processed_logs_directory
            / raw_log_path.name
        )

        self.assertTrue(
            processed_log_path.exists()
        )

        saved_alert_files = list(
            self.generated_alerts_directory.glob(
                "*.jsonl"
            )
        )

        self.assertEqual(
            len(saved_alert_files),
            0,
        )

    def test_invalid_json_moves_log_to_failed(
        self,
    ) -> None:
        """
        Invalid JSON should move into failed_logs.
        """

        invalid_log_path = (
            self.raw_logs_directory
            / "invalid-json.jsonl"
        )

        invalid_log_path.write_text(
            "{this is not valid json}\n",
            encoding="utf-8",
        )

        with self.assertRaises(
            LogProcessingError
        ):
            self.processing_service.process_log_file(
                invalid_log_path
            )

        self.assertFalse(
            invalid_log_path.exists()
        )

        failed_log_path = (
            self.failed_logs_directory
            / invalid_log_path.name
        )

        self.assertTrue(
            failed_log_path.exists()
        )

    def test_missing_field_moves_log_to_failed(
        self,
    ) -> None:
        """
        A log with a missing required field should fail.
        """

        incomplete_log_path = (
            self.raw_logs_directory
            / "missing-field.jsonl"
        )

        incomplete_log_data = {
            "log_id": "log-missing-field",
            "timestamp": "2026-07-11T22:00:00Z",
            "vm_name": "VM1",
            "event_type": "port_scan",
            "destination_ip": "192.168.1.10",
            "message": "Port scan detected",
        }

        incomplete_log_path.write_text(
            json.dumps(incomplete_log_data) + "\n",
            encoding="utf-8",
        )

        with self.assertRaises(
            LogProcessingError
        ):
            self.processing_service.process_log_file(
                incomplete_log_path
            )

        self.assertFalse(
            incomplete_log_path.exists()
        )

        failed_log_path = (
            self.failed_logs_directory
            / incomplete_log_path.name
        )

        self.assertTrue(
            failed_log_path.exists()
        )

    def test_matching_alert_uploads_to_firebase(
        self,
    ) -> None:
        """
        A generated alert should be sent to Firebase.
        """

        fake_firebase_service = Mock(
            spec=FirebaseService
        )

        processing_service = LogProcessingService(
            log_service=self.log_service,
            alert_service=self.alert_service,
            rule_engine=RuleEngine(),
            firebase_service=fake_firebase_service,
        )

        security_log = self.create_security_log(
            event_type="login_failure",
            attempt_count=5,
        )

        raw_log_path = self.log_service.save_raw_log(
            security_log
        )

        generated_alert = (
            processing_service.process_log_file(
                raw_log_path
            )
        )

        self.assertIsNotNone(
            generated_alert
        )

        fake_firebase_service.upload_alert.assert_called_once_with(
            generated_alert
        )

        processed_log_path = (
            self.processed_logs_directory
            / raw_log_path.name
        )

        self.assertTrue(
            processed_log_path.exists()
        )

    def test_normal_login_does_not_upload_to_firebase(
        self,
    ) -> None:
        """
        A harmless log should not call Firebase upload.
        """

        fake_firebase_service = Mock(
            spec=FirebaseService
        )

        processing_service = LogProcessingService(
            log_service=self.log_service,
            alert_service=self.alert_service,
            rule_engine=RuleEngine(),
            firebase_service=fake_firebase_service,
        )

        security_log = self.create_security_log(
            event_type="login_success"
        )

        raw_log_path = self.log_service.save_raw_log(
            security_log
        )

        generated_alert = (
            processing_service.process_log_file(
                raw_log_path
            )
        )

        self.assertIsNone(
            generated_alert
        )

        fake_firebase_service.upload_alert.assert_not_called()

    def test_firebase_failure_moves_log_to_failed(
        self,
    ) -> None:
        """
        A Firebase upload failure should move the log
        into failed_logs.
        """

        fake_firebase_service = Mock(
            spec=FirebaseService
        )

        fake_firebase_service.upload_alert.side_effect = (
            FirebaseServiceError(
                "Simulated Firebase failure"
            )
        )

        processing_service = LogProcessingService(
            log_service=self.log_service,
            alert_service=self.alert_service,
            rule_engine=RuleEngine(),
            firebase_service=fake_firebase_service,
        )

        security_log = self.create_security_log(
            event_type="malware_detected"
        )

        raw_log_path = self.log_service.save_raw_log(
            security_log
        )

        with self.assertRaises(
            LogProcessingError
        ):
            processing_service.process_log_file(
                raw_log_path
            )

        failed_log_path = (
            self.failed_logs_directory
            / raw_log_path.name
        )

        processed_log_path = (
            self.processed_logs_directory
            / raw_log_path.name
        )

        self.assertFalse(
            raw_log_path.exists()
        )

        self.assertTrue(
            failed_log_path.exists()
        )

        self.assertFalse(
            processed_log_path.exists()
        )

        fake_firebase_service.upload_alert.assert_called_once()


if __name__ == "__main__":
    unittest.main()