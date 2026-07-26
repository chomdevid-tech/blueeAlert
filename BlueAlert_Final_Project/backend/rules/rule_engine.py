import logging

from backend.models.security_alert import SecurityAlert
from backend.models.security_log import SecurityLog
from backend.rules.alert_rules import (
    ALERT_RULES,
    AlertRule,
)


logger = logging.getLogger(__name__)


class RuleEngine:
    """
    Compares security logs with BlueAlert detection rules.
    """

    def __init__(
        self,
        alert_rules: tuple[AlertRule, ...] = ALERT_RULES,
    ) -> None:
        self.alert_rules = alert_rules

    def find_matching_rule(
        self,
        security_log: SecurityLog,
    ) -> AlertRule | None:
        """
        Return the first rule that matches the log.

        Return None when no rule matches.
        """

        if not isinstance(security_log, SecurityLog):
            raise TypeError(
                "security_log must be a SecurityLog object."
            )

        for alert_rule in self.alert_rules:
            if alert_rule.matches(security_log):
                logger.info(
                    "Security rule matched: %s | %s",
                    alert_rule.attack_type,
                    security_log.log_id,
                )

                return alert_rule

        logger.info(
            "No security rule matched: %s | %s",
            security_log.event_type,
            security_log.log_id,
        )

        return None

    def create_alert(
        self,
        security_log: SecurityLog,
    ) -> SecurityAlert | None:
        """
        Create a SecurityAlert when a rule matches.

        Return None when the log does not match a rule.
        """

        matching_rule = self.find_matching_rule(
            security_log
        )

        if matching_rule is None:
            return None

        # Example:
        # log-abc123 becomes abc123.
        alert_identifier = (
            security_log.log_id.removeprefix("log-")
        )

        alert_data = {
            "alertId": f"alert-{alert_identifier}",
            "title": matching_rule.title,
            "description": matching_rule.description,
            "attackType": matching_rule.attack_type,
            "severity": matching_rule.severity,
            "status": "new",
            "vmName": security_log.vm_name,
            "sourceIp": security_log.source_ip,
            "destinationIp": security_log.destination_ip,
            "timestamp": security_log.timestamp,
            "rawLog": security_log.to_dict(),
        }

        generated_alert = SecurityAlert.from_dict(
            alert_data
        )

        logger.info(
            "Security alert created: %s | %s | %s",
            generated_alert.alert_id,
            generated_alert.attack_type,
            generated_alert.severity,
        )

        return generated_alert