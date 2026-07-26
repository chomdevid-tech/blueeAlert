import logging

from firebase_admin import db

from backend.config.firebase_config import (
    initialize_firebase,
)
from backend.models.security_alert import SecurityAlert


logger = logging.getLogger(__name__)


class FirebaseServiceError(Exception):
    """
    Raised when a Firebase database operation fails.
    """


class FirebaseService:
    """
    Uploads and reads BlueAlert security alerts
    from Firebase Realtime Database.
    """

    def __init__(self) -> None:
        """
        Initialize Firebase and prepare the alerts path.
        """

        initialize_firebase()

        self.alerts_reference = db.reference(
            "alerts"
        )

    def upload_alert(
        self,
        security_alert: SecurityAlert,
    ) -> None:
        """
        Upload one SecurityAlert to Firebase.

        Firebase path:
        alerts/{alertId}
        """

        if not isinstance(
            security_alert,
            SecurityAlert,
        ):
            raise TypeError(
                "security_alert must be a "
                "SecurityAlert object."
            )

        try:
            alert_reference = (
                self.alerts_reference.child(
                    security_alert.alert_id
                )
            )

            alert_reference.set(
                security_alert.to_dict()
            )

        except Exception as error:
            logger.exception(
                "Failed to upload alert to Firebase: %s",
                security_alert.alert_id,
            )

            raise FirebaseServiceError(
                "The alert could not be uploaded "
                "to Firebase."
            ) from error

        logger.info(
            "Alert uploaded to Firebase: %s",
            security_alert.alert_id,
        )

    def get_alert_by_id(
        self,
        alert_id: str,
    ) -> SecurityAlert | None:
        """
        Read one alert from Firebase.

        Return None if the alert does not exist.
        """

        if not isinstance(alert_id, str):
            raise TypeError(
                "alert_id must be a string."
            )

        cleaned_alert_id = alert_id.strip()

        if not cleaned_alert_id:
            raise ValueError(
                "alert_id cannot be empty."
            )

        try:
            alert_data = (
                self.alerts_reference
                .child(cleaned_alert_id)
                .get()
            )

        except Exception as error:
            logger.exception(
                "Failed to read Firebase alert: %s",
                cleaned_alert_id,
            )

            raise FirebaseServiceError(
                "The alert could not be read "
                "from Firebase."
            ) from error

        if alert_data is None:
            return None

        if not isinstance(alert_data, dict):
            raise FirebaseServiceError(
                "Firebase returned invalid alert data."
            )

        try:
            security_alert = SecurityAlert.from_dict(
                alert_data
            )

        except ValueError as error:
            raise FirebaseServiceError(
                "Firebase alert data failed validation."
            ) from error

        logger.info(
            "Alert downloaded from Firebase: %s",
            cleaned_alert_id,
        )

        return security_alert