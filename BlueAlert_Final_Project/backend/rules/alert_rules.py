from dataclasses import dataclass

from backend.models.security_log import SecurityLog


@dataclass(frozen=True)
class AlertRule:
    """
    Defines one security detection rule.
    """

    event_type: str
    title: str
    description: str
    attack_type: str
    severity: str
    minimum_attempt_count: int | None = None

    def matches(
        self,
        security_log: SecurityLog,
    ) -> bool:
        """
        Check whether a SecurityLog matches this rule.
        """

        if security_log.event_type != self.event_type:
            return False

        if self.minimum_attempt_count is not None:
            if security_log.attempt_count is None:
                return False

            return (
                security_log.attempt_count
                >= self.minimum_attempt_count
            )

        return True


ALERT_RULES: tuple[AlertRule, ...] = (
    AlertRule(
        event_type="login_failure",
        title="Brute Force Attempt Detected",
        description=(
            "Multiple failed login attempts were detected."
        ),
        attack_type="Brute Force",
        severity="high",
        minimum_attempt_count=5,
    ),
    AlertRule(
        event_type="unauthorized_access",
        title="Unauthorized Access Detected",
        description=(
            "A user attempted to access a restricted resource."
        ),
        attack_type="Unauthorized Access",
        severity="high",
    ),
    AlertRule(
        event_type="malware_detected",
        title="Malware Detected",
        description=(
            "A malware signature was detected on the system."
        ),
        attack_type="Malware",
        severity="critical",
    ),
    AlertRule(
        event_type="port_scan",
        title="Port Scan Detected",
        description=(
            "Multiple destination ports were scanned."
        ),
        attack_type="Port Scan",
        severity="medium",
    ),
    AlertRule(
        event_type="sql_injection",
        title="SQL Injection Attempt Detected",
        description=(
            "A SQL injection pattern was detected "
            "in a web request."
        ),
        attack_type="SQL Injection",
        severity="critical",
    ),
)