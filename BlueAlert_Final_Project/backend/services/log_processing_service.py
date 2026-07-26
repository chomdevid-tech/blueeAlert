import logging
from pathlib import Path

from backend.models.security_alert import SecurityAlert
from backend.rules.rule_engine import RuleEngine
from backend.services.alert_service import AlertService
from backend.services.firebase_service import FirebaseService
from backend.services.log_service import LogService


logger = logging.getLogger(__name__)


class LogProcessingError(Exception):
    """
    Raised when a raw security log cannot be processed.
    """


class LogProcessingService:
    """
    Reads raw logs, checks security rules, saves alerts,
    uploads alerts to Firebase, and organizes log files.
    """

    def __init__(
        self,
        log_service: LogService,
        alert_service: AlertService,
        rule_engine: RuleEngine,
        firebase_service: FirebaseService | None = None,
    ) -> None:
        self.log_service = log_service
        self.alert_service = alert_service
        self.rule_engine = rule_engine
        self.firebase_service = firebase_service

    def process_log_file(
        self,
        raw_log_file_path: Path,
    ) -> SecurityAlert | None:
        """
        Process one raw security-log file.

        Return a SecurityAlert when a rule matches.
        Return None when the log is valid but harmless.
        """

        raw_log_file_path = Path(raw_log_file_path)

        try:
            security_log = (
                self.log_service.read_raw_log_file(
                    raw_log_file_path
                )
            )

            generated_alert = (
                self.rule_engine.create_alert(
                    security_log
                )
            )

            if generated_alert is not None:
                # Keep a local alert copy first.
                self.alert_service.save_generated_alert(
                    generated_alert
                )

                logger.info(
                    "Alert saved locally for log: %s",
                    security_log.log_id,
                )

                # Upload only when a Firebase service
                # was provided to this processing service.
                if self.firebase_service is not None:
                    self.firebase_service.upload_alert(
                        generated_alert
                    )

                    
            else:
                logger.info(
                    "Log processed with no alert: %s",
                    security_log.log_id,
                )

            self.log_service.move_to_processed(
                raw_log_file_path
            )

            logger.info(
                "Security log processed successfully: %s",
                security_log.log_id,
            )

            return generated_alert

        except Exception as error:
            logger.exception(
                "Error processing raw log: %s",
                raw_log_file_path.name,
            )

            # A failed log should not remain in raw_logs.
            if raw_log_file_path.exists():
                try:
                    self.log_service.move_to_failed(
                        raw_log_file_path
                    )

                    logger.info(
                        "Failed log moved to failed_logs: %s",
                        raw_log_file_path.name,
                    )

                except Exception:
                    logger.exception(
                        "Could not move failed log: %s",
                        raw_log_file_path.name,
                    )

            raise LogProcessingError(
                f"Could not process "
                f"'{raw_log_file_path.name}'."
            ) from error