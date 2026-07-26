import logging

import firebase_admin
from firebase_admin import credentials

from backend.config.settings import load_settings


logger = logging.getLogger(__name__)


class FirebaseInitializationError(Exception):
    """
    Raised when Firebase Admin cannot be initialized.
    """


def initialize_firebase() -> firebase_admin.App:
    """
    Initialize Firebase Admin only once.
    """

    try:
        # Return the existing app when Firebase
        # has already been initialized.
        existing_firebase_app = firebase_admin.get_app()

        return existing_firebase_app

    except ValueError:
        # No Firebase application exists yet.
        pass

    settings = load_settings()

    try:
        firebase_credentials = credentials.Certificate(
            str(settings.firebase_credentials_path)
        )

        firebase_app = firebase_admin.initialize_app(
            firebase_credentials,
            {
                "databaseURL": (
                    settings.firebase_database_url
                )
            },
        )

    except Exception as error:
        logger.exception(
            "Firebase initialization failed"
        )

        raise FirebaseInitializationError(
            "Could not initialize Firebase Admin."
        ) from error

    logger.info(
        "Firebase Admin initialized successfully"
    )

    return firebase_app