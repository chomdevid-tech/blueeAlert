import json

from backend.models.security_log import SecurityLog
from backend.rules.rule_engine import RuleEngine
from backend.services.firebase_service import (
    FirebaseService,
)


def main() -> None:
    """
    Create an alert using the rule engine,
    upload it, and read it back.
    """

    security_log = SecurityLog.from_dict(
        {
            "log_id": "log-firebase-rule-test-001",
            "timestamp": "2026-07-11T22:30:00Z",
            "vm_name": "VM1",
            "event_type": "login_failure",
            "source_ip": "192.168.1.105",
            "destination_ip": "192.168.1.10",
            "username": "root",
            "message": (
                "Multiple invalid password "
                "attempts detected"
            ),
            "attempt_count": 7,
        }
    )

    rule_engine = RuleEngine()

    generated_alert = rule_engine.create_alert(
        security_log
    )

    if generated_alert is None:
        raise RuntimeError(
            "The security log did not create an alert."
        )

    firebase_service = FirebaseService()

    firebase_service.upload_alert(
        generated_alert
    )

    downloaded_alert = (
        firebase_service.get_alert_by_id(
            generated_alert.alert_id
        )
    )

    if downloaded_alert is None:
        raise RuntimeError(
            "The alert was uploaded but could "
            "not be downloaded."
        )

    if (
        downloaded_alert.alert_id
        != generated_alert.alert_id
    ):
        raise RuntimeError(
            "The downloaded alert ID does not match."
        )

    print(
        "Rule-generated alert uploaded successfully."
    )

    print()

    print(
        json.dumps(
            downloaded_alert.to_dict(),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()