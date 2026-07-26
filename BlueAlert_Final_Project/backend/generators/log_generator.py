import json
import logging
import random
from datetime import datetime, timezone
from typing import Any

from backend.models.security_log import SecurityLog


logger = logging.getLogger(__name__)


class SecurityLogGenerator:
    """
    Generates fake security logs for the BlueAlert demonstration.
    """

    SUPPORTED_EVENT_TYPES = (
        "login_failure",
        "unauthorized_access",
        "malware_detected",
        "port_scan",
        "sql_injection",
        "login_success",
    )

    EVENT_FILE_NAMES = {
        "login_failure": "brute-force",
        "unauthorized_access": "unauthorized-access",
        "malware_detected": "malware-detected",
        "port_scan": "port-scan",
        "sql_injection": "sql-injection",
        "login_success": "normal-login",
    }

    VM_NAMES = (
        "VM1",
        "VM2",
        "VM3",
    )

    VM_DESTINATION_IPS = {
        "VM1": "192.168.1.10",
        "VM2": "192.168.1.20",
        "VM3": "192.168.1.30",
    }

    SOURCE_IPS = (
        "192.168.1.105",
        "192.168.1.106",
        "10.0.20.15",
        "172.16.0.50",
    )

    USERNAMES = (
        "root",
        "admin",
        "analyst",
        "guest",
    )

    def generate_log(
        self,
        event_type: str | None = None,
    ) -> SecurityLog:
        """
        Generate and validate one fake security log.
        """

        selected_event_type = (
            event_type
            if event_type is not None
            else random.choice(
                self.SUPPORTED_EVENT_TYPES
            )
        )

        if selected_event_type not in self.SUPPORTED_EVENT_TYPES:
            raise ValueError(
                f"Unsupported event type: {selected_event_type}"
            )

        selected_vm = random.choice(
            self.VM_NAMES
        )

        selected_source_ip = random.choice(
            self.SOURCE_IPS
        )

        destination_ip = (
            self.VM_DESTINATION_IPS[selected_vm]
        )

        event_details = self._create_event_details(
            selected_event_type
        )

        current_time = datetime.now(
            timezone.utc
        )

        timestamp = current_time.isoformat().replace(
            "+00:00",
            "Z",
        )

        readable_time = current_time.strftime(
            "%Y%m%d-%H%M%S-%f"
        )

        event_title = self.EVENT_FILE_NAMES[
            selected_event_type
        ]

        log_id = (
            f"log-{readable_time}-{event_title}"
        )

        security_log_data: dict[str, Any] = {
            "log_id": log_id,
            "timestamp": timestamp,
            "vm_name": selected_vm,
            "event_type": selected_event_type,
            "source_ip": selected_source_ip,
            "destination_ip": destination_ip,
            **event_details,
        }

        generated_log = SecurityLog.from_dict(
            security_log_data
        )

        logger.info(
            "Security log generated: %s | %s | %s",
            generated_log.log_id,
            generated_log.vm_name,
            generated_log.event_type,
        )

        return generated_log

    def _create_event_details(
        self,
        event_type: str,
    ) -> dict[str, Any]:
        """
        Create information for a specific event type.
        """

        if event_type == "login_failure":
            return {
                "username": random.choice(
                    self.USERNAMES
                ),
                "message": (
                    "Multiple invalid password "
                    "attempts detected"
                ),
                "attempt_count": random.randint(
                    5,
                    12,
                ),
            }

        if event_type == "unauthorized_access":
            return {
                "username": "guest",
                "message": (
                    "User attempted to access "
                    "a restricted resource"
                ),
            }

        if event_type == "malware_detected":
            return {
                "message": (
                    "Malware signature detected "
                    "on the virtual machine"
                ),
            }

        if event_type == "port_scan":
            return {
                "message": (
                    "Multiple destination ports "
                    "were scanned"
                ),
            }

        if event_type == "sql_injection":
            return {
                "message": (
                    "SQL injection pattern detected "
                    "in a web request"
                ),
            }

        if event_type == "login_success":
            return {
                "username": random.choice(
                    self.USERNAMES
                ),
                "message": (
                    "User login completed successfully"
                ),
            }

        raise ValueError(
            f"No sample data exists for: {event_type}"
        )


def main() -> None:
    """
    Generate and display one random security log.
    """

    log_generator = SecurityLogGenerator()
    generated_log = log_generator.generate_log()

    print(
        json.dumps(
            generated_log.to_dict(),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
