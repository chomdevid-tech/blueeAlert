import unittest

from backend.generators.log_generator import (
    SecurityLogGenerator,
)
from backend.models.security_log import SecurityLog


class SecurityLogGeneratorTest(unittest.TestCase):
    def setUp(self) -> None:
        """
        Create a new generator before every test.
        """

        self.log_generator = SecurityLogGenerator()

    def test_generate_all_supported_event_types(
        self,
    ) -> None:
        for event_type in (
            SecurityLogGenerator.SUPPORTED_EVENT_TYPES
        ):
            with self.subTest(event_type=event_type):
                generated_log = (
                    self.log_generator.generate_log(
                        event_type
                    )
                )

                self.assertIsInstance(
                    generated_log,
                    SecurityLog,
                )

                self.assertEqual(
                    generated_log.event_type,
                    event_type,
                )

                self.assertIn(
                    generated_log.vm_name,
                    {"VM1", "VM2", "VM3"},
                )

                self.assertTrue(
                    generated_log.log_id.startswith(
                        "log-"
                    )
                )

    def test_brute_force_log_has_five_or_more_attempts(
        self,
    ) -> None:
        generated_log = self.log_generator.generate_log(
            "login_failure"
        )

        self.assertIsNotNone(
            generated_log.attempt_count
        )

        self.assertGreaterEqual(
            generated_log.attempt_count,
            5,
        )

    def test_normal_login_does_not_have_attempt_count(
        self,
    ) -> None:
        generated_log = self.log_generator.generate_log(
            "login_success"
        )

        self.assertEqual(
            generated_log.event_type,
            "login_success",
        )

        self.assertIsNone(
            generated_log.attempt_count
        )

    def test_invalid_event_type_raises_error(
        self,
    ) -> None:
        with self.assertRaises(ValueError):
            self.log_generator.generate_log(
                "unknown_event"
            )

    def test_generated_logs_have_unique_ids(
        self,
    ) -> None:
        first_log = self.log_generator.generate_log(
            "port_scan"
        )

        second_log = self.log_generator.generate_log(
            "port_scan"
        )

        self.assertNotEqual(
            first_log.log_id,
            second_log.log_id,
        )


if __name__ == "__main__":
    unittest.main()