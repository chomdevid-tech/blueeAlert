from dataclasses import dataclass, replace
from datetime import datetime
from ipaddress import ip_address
from typing import Any


ALLOWED_SEVERITIES = {
    "medium",
    "high",
    "critical",
}

ALLOWED_STATUSES = {
    "new",
    "investigating",
    "resolved",
}

ALLOWED_VM_NAMES = {
    "VM1",
    "VM2",
    "VM3",
}


@dataclass(frozen=True)
class SecurityAlert:
    """
    Represents one security alert created by the rule engine.
    """

    alert_id: str
    title: str
    description: str
    attack_type: str
    severity: str
    status: str
    vm_name: str
    source_ip: str
    destination_ip: str
    timestamp: str
    raw_log: dict[str, Any]

    @classmethod
    def from_dict(
        cls,
        alert_data: dict[str, Any],
    ) -> "SecurityAlert":
        """
        Validate Firebase-style dictionary data and convert it
        into a SecurityAlert object.
        """

        if not isinstance(alert_data, dict):
            raise ValueError(
                "Security alert must be a dictionary."
            )

        alert_id = cls._read_required_text(
            alert_data,
            "alertId",
        )

        title = cls._read_required_text(
            alert_data,
            "title",
        )

        description = cls._read_required_text(
            alert_data,
            "description",
        )

        attack_type = cls._read_required_text(
            alert_data,
            "attackType",
        )

        severity = cls._read_required_text(
            alert_data,
            "severity",
        )

        status = cls._read_required_text(
            alert_data,
            "status",
        )

        vm_name = cls._read_required_text(
            alert_data,
            "vmName",
        )

        source_ip = cls._read_required_text(
            alert_data,
            "sourceIp",
        )

        destination_ip = cls._read_required_text(
            alert_data,
            "destinationIp",
        )

        timestamp = cls._read_required_text(
            alert_data,
            "timestamp",
        )

        raw_log_value = alert_data.get("rawLog")

        if not isinstance(raw_log_value, dict):
            raise ValueError(
                "rawLog must be a dictionary."
            )

        cls._validate_severity(severity)
        cls._validate_status(status)
        cls._validate_vm_name(vm_name)
        cls._validate_timestamp(timestamp)

        cls._validate_ip_address(
            source_ip,
            "sourceIp",
        )

        cls._validate_ip_address(
            destination_ip,
            "destinationIp",
        )

        return cls(
            alert_id=alert_id,
            title=title,
            description=description,
            attack_type=attack_type,
            severity=severity,
            status=status,
            vm_name=vm_name,
            source_ip=source_ip,
            destination_ip=destination_ip,
            timestamp=timestamp,
            raw_log=dict(raw_log_value),
        )

    def to_dict(self) -> dict[str, Any]:
        """
        Convert this object into the exact dictionary structure
        required by Firebase and Flutter.
        """

        return {
            "alertId": self.alert_id,
            "title": self.title,
            "description": self.description,
            "attackType": self.attack_type,
            "severity": self.severity,
            "status": self.status,
            "vmName": self.vm_name,
            "sourceIp": self.source_ip,
            "destinationIp": self.destination_ip,
            "timestamp": self.timestamp,
            "rawLog": dict(self.raw_log),
        }

    def with_status(
        self,
        new_status: str,
    ) -> "SecurityAlert":
        """
        Create a new SecurityAlert with a different status.

        The original object is not changed.
        """

        cleaned_status = new_status.strip()

        self._validate_status(cleaned_status)

        return replace(
            self,
            status=cleaned_status,
        )

    @staticmethod
    def _read_required_text(
        alert_data: dict[str, Any],
        field_name: str,
    ) -> str:
        """
        Read and validate one required text field.
        """

        field_value = alert_data.get(field_name)

        if not isinstance(field_value, str):
            raise ValueError(
                f"{field_name} must be a string."
            )

        cleaned_value = field_value.strip()

        if not cleaned_value:
            raise ValueError(
                f"{field_name} is required and cannot be empty."
            )

        return cleaned_value

    @staticmethod
    def _validate_severity(severity: str) -> None:
        """
        Confirm that severity uses an allowed value.
        """

        if severity not in ALLOWED_SEVERITIES:
            raise ValueError(
                f"Invalid severity '{severity}'. "
                f"Allowed values: "
                f"{sorted(ALLOWED_SEVERITIES)}"
            )

    @staticmethod
    def _validate_status(status: str) -> None:
        """
        Confirm that status uses an allowed value.
        """

        if status not in ALLOWED_STATUSES:
            raise ValueError(
                f"Invalid status '{status}'. "
                f"Allowed values: "
                f"{sorted(ALLOWED_STATUSES)}"
            )

    @staticmethod
    def _validate_vm_name(vm_name: str) -> None:
        """
        Confirm that the VM name is valid.
        """

        if vm_name not in ALLOWED_VM_NAMES:
            raise ValueError(
                f"Invalid vmName '{vm_name}'. "
                f"Allowed values: "
                f"{sorted(ALLOWED_VM_NAMES)}"
            )

    @staticmethod
    def _validate_timestamp(timestamp: str) -> None:
        """
        Confirm that timestamp uses ISO 8601 format.
        """

        normalized_timestamp = timestamp.replace(
            "Z",
            "+00:00",
        )

        try:
            datetime.fromisoformat(normalized_timestamp)
        except ValueError as error:
            raise ValueError(
                "timestamp must use ISO 8601 format. "
                "Example: 2026-07-11T20:30:00"
            ) from error

    @staticmethod
    def _validate_ip_address(
        ip_value: str,
        field_name: str,
    ) -> None:
        """
        Confirm that a value is a valid IPv4 or IPv6 address.
        """

        try:
            ip_address(ip_value)
        except ValueError as error:
            raise ValueError(
                f"{field_name} must be a valid IP address."
            ) from error