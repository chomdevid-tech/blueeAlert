import unittest

from backend.models.security_log import SecurityLog


class SecurityLogTest(unittest.TestCase):
    def setUp(self) -> None:
        """
        Create valid test data before every test.
        """

        self.valid_log_data = {
            "log_id": "log-001",
            "timestamp": "2026-07-11T20:30:00",
            "vm_name": "VM1",
            "event_type": "login_failure",
            "source_ip": "192.168.1.105",
            "destination_ip": "192.168.1.10",
            "username": "root",
            "message": "Invalid password",
            "attempt_count": 5,
        }

    def test_create_valid_security_log(self) -> None:
        security_log = SecurityLog.from_dict(
            self.valid_log_data
        )

        self.assertEqual(
            security_log.log_id,
            "log-001",
        )

        self.assertEqual(
            security_log.vm_name,
            "VM1",
        )

        self.assertEqual(
            security_log.attempt_count,
            5,
        )

    def test_convert_security_log_to_dictionary(self) -> None:
        security_log = SecurityLog.from_dict(
            self.valid_log_data
        )

        converted_log_data = security_log.to_dict()

        self.assertEqual(
            converted_log_data["event_type"],
            "login_failure",
        )

        self.assertEqual(
            converted_log_data["username"],
            "root",
        )

    def test_missing_required_field_raises_error(self) -> None:
        invalid_log_data = self.valid_log_data.copy()

        del invalid_log_data["source_ip"]

        with self.assertRaises(ValueError):
            SecurityLog.from_dict(invalid_log_data)

    def test_invalid_vm_name_raises_error(self) -> None:
        invalid_log_data = self.valid_log_data.copy()

        invalid_log_data["vm_name"] = "VM9"

        with self.assertRaises(ValueError):
            SecurityLog.from_dict(invalid_log_data)

    def test_invalid_ip_address_raises_error(self) -> None:
        invalid_log_data = self.valid_log_data.copy()

        invalid_log_data["source_ip"] = "not-an-ip"

        with self.assertRaises(ValueError):
            SecurityLog.from_dict(invalid_log_data)


if __name__ == "__main__":
    unittest.main()