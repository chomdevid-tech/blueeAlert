import unittest

from backend.models.security_log import SecurityLog
from backend.rules.rule_engine import RuleEngine


class RuleEngineTest(unittest.TestCase):
    def setUp(self) -> None:
        """
        Create a rule engine before every test.
        """

        self.rule_engine = RuleEngine()

    def create_test_log(
        self,
        event_type: str,
        attempt_count: int | None = None,
    ) -> SecurityLog:
        """
        Create a valid log for rule-engine testing.
        """

        log_data = {
            "log_id": f"log-test-{event_type}",
            "timestamp": "2026-07-11T21:30:00Z",
            "vm_name": "VM1",
            "event_type": event_type,
            "source_ip": "192.168.1.105",
            "destination_ip": "192.168.1.10",
            "username": "root",
            "message": f"Test event: {event_type}",
        }

        if attempt_count is not None:
            log_data["attempt_count"] = attempt_count

        return SecurityLog.from_dict(log_data)

    def test_brute_force_rule_creates_alert(
        self,
    ) -> None:
        security_log = self.create_test_log(
            event_type="login_failure",
            attempt_count=5,
        )

        generated_alert = (
            self.rule_engine.create_alert(
                security_log
            )
        )

        self.assertIsNotNone(generated_alert)

        assert generated_alert is not None

        self.assertEqual(
            generated_alert.attack_type,
            "Brute Force",
        )

        self.assertEqual(
            generated_alert.severity,
            "high",
        )

        self.assertEqual(
            generated_alert.status,
            "new",
        )

    def test_login_failure_below_threshold_creates_no_alert(
        self,
    ) -> None:
        security_log = self.create_test_log(
            event_type="login_failure",
            attempt_count=4,
        )

        generated_alert = (
            self.rule_engine.create_alert(
                security_log
            )
        )

        self.assertIsNone(generated_alert)

    def test_normal_login_creates_no_alert(
        self,
    ) -> None:
        security_log = self.create_test_log(
            event_type="login_success"
        )

        generated_alert = (
            self.rule_engine.create_alert(
                security_log
            )
        )

        self.assertIsNone(generated_alert)

    def test_other_security_rules_create_alerts(
        self,
    ) -> None:
        expected_results = {
            "unauthorized_access": (
                "Unauthorized Access",
                "high",
            ),
            "malware_detected": (
                "Malware",
                "critical",
            ),
            "port_scan": (
                "Port Scan",
                "medium",
            ),
            "sql_injection": (
                "SQL Injection",
                "critical",
            ),
        }

        for (
            event_type,
            expected_result,
        ) in expected_results.items():
            with self.subTest(event_type=event_type):
                security_log = self.create_test_log(
                    event_type=event_type
                )

                generated_alert = (
                    self.rule_engine.create_alert(
                        security_log
                    )
                )

                self.assertIsNotNone(
                    generated_alert
                )

                assert generated_alert is not None

                expected_attack_type = (
                    expected_result[0]
                )

                expected_severity = (
                    expected_result[1]
                )

                self.assertEqual(
                    generated_alert.attack_type,
                    expected_attack_type,
                )

                self.assertEqual(
                    generated_alert.severity,
                    expected_severity,
                )

    def test_alert_contains_original_raw_log(
        self,
    ) -> None:
        security_log = self.create_test_log(
            event_type="login_failure",
            attempt_count=7,
        )

        generated_alert = (
            self.rule_engine.create_alert(
                security_log
            )
        )

        self.assertIsNotNone(generated_alert)

        assert generated_alert is not None

        self.assertEqual(
            generated_alert.raw_log["log_id"],
            security_log.log_id,
        )

        self.assertEqual(
            generated_alert.raw_log[
                "attempt_count"
            ],
            7,
        )


if __name__ == "__main__":
    unittest.main()