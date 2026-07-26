import json
import logging
from pathlib import Path

from backend.models.security_alert import SecurityAlert


logger = logging.getLogger(__name__)


class DuplicateAlertError(Exception):
    """
    Raised when an alert with the same ID already exists.
    """


class AlertStorageError(Exception):
    """
    Raised when a generated alert cannot be saved.
    """


class AlertService:
    """
    Saves local copies of generated BlueAlert alerts.
    """

    def __init__(
        self,
        generated_alerts_directory: Path | None = None,
    ) -> None:
        """
        Prepare the folder used to store generated alerts.
        """

        backend_directory = (
            Path(__file__).resolve().parents[1]
        )

        default_alerts_directory = (
            backend_directory
            / "storage"
            / "generated_alerts"
        )

        self.generated_alerts_directory = (
            generated_alerts_directory
            if generated_alerts_directory is not None
            else default_alerts_directory
        )

        self.generated_alerts_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def save_generated_alert(
        self,
        security_alert: SecurityAlert,
    ) -> Path:
        """
        Save one SecurityAlert in JSON Lines format.

        Return the path of the new alert file.
        """

        if not isinstance(
            security_alert,
            SecurityAlert,
        ):
            raise TypeError(
                "security_alert must be a "
                "SecurityAlert object."
            )

        alert_file_path = (
            self.generated_alerts_directory
            / f"{security_alert.alert_id}.jsonl"
        )

        alert_json_line = json.dumps(
            security_alert.to_dict(),
            ensure_ascii=False,
        )

        try:
            with alert_file_path.open(
                mode="x",
                encoding="utf-8",
            ) as alert_file:
                alert_file.write(
                    alert_json_line + "\n"
                )

        except FileExistsError as error:
            logger.warning(
                "Duplicate alert rejected: %s",
                security_alert.alert_id,
            )

            raise DuplicateAlertError(
                "An alert with ID "
                f"'{security_alert.alert_id}' "
                "already exists."
            ) from error

        except OSError as error:
            logger.exception(
                "Failed to save generated alert: %s",
                security_alert.alert_id,
            )

            raise AlertStorageError(
                "The generated alert could not be saved."
            ) from error

        logger.info(
            "Generated alert saved locally: %s",
            alert_file_path,
        )

        return alert_file_path