import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from backend.models.security_log import SecurityLog
from backend.services.log_service import (
    DuplicateLogError,
    LogService,
)


class LogServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        """
        Create a temporary storage folder before every test.
        """

        self.temporary_directory = TemporaryDirectory()

        self.raw_logs_directory = (
            Path(self.temporary_directory.name)
            / "raw_logs"
        )

        self.log_service = LogService(
            raw_logs_directory=self.raw_logs_directory
        )

        self.security_log = SecurityLog.from_dict(
            {
                "log_id": "log-test-001",
                "timestamp": "2026-07-11T21:00:00Z",
                "vm_name": "VM1",
                "event_type": "login_failure",
                "source_ip": "192.168.1.105",
                "destination_ip": "192.168.1.10",
                "username": "root",
                "message": "Invalid password",
                "attempt_count": 5,
            }
        )

    def tearDown(self) -> None:
        """
        Delete the temporary test folder.
        """

        self.temporary_directory.cleanup()

    def test_save_raw_security_log(self) -> None:
        saved_file_path = (
            self.log_service.save_raw_log(
                self.security_log
            )
        )

        self.assertTrue(
            saved_file_path.exists()
        )

        self.assertEqual(
            saved_file_path.suffix,
            ".jsonl",
        )

    def test_saved_file_contains_valid_json_line(
        self,
    ) -> None:
        saved_file_path = (
            self.log_service.save_raw_log(
                self.security_log
            )
        )

        saved_lines = (
            saved_file_path
            .read_text(encoding="utf-8")
            .splitlines()
        )

        self.assertEqual(
            len(saved_lines),
            1,
        )

        saved_log_data = json.loads(
            saved_lines[0]
        )

        self.assertEqual(
            saved_log_data["log_id"],
            "log-test-001",
        )

        self.assertEqual(
            saved_log_data["event_type"],
            "login_failure",
        )

        self.assertEqual(
            saved_log_data["attempt_count"],
            5,
        )

    def test_duplicate_log_raises_error(
        self,
    ) -> None:
        self.log_service.save_raw_log(
            self.security_log
        )

        with self.assertRaises(
            DuplicateLogError
        ):
            self.log_service.save_raw_log(
                self.security_log
            )


if __name__ == "__main__":
    unittest.main()