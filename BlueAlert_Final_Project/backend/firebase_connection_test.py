from firebase_admin import db

from backend.config.firebase_config import (
    initialize_firebase,
)


def main() -> None:
    """
    Write test data to Firebase and read it back.
    """

    initialize_firebase()

    connection_test_reference = db.reference(
        "connection_test"
    )

    test_data = {
        "application": "BlueAlert Backend",
        "status": "connected",
        "message": (
            "Python successfully connected "
            "to Firebase Realtime Database."
        ),
    }

    connection_test_reference.set(
        test_data
    )

    downloaded_test_data = (
        connection_test_reference.get()
    )

    print("Firebase connection successful.")
    print(downloaded_test_data)


if __name__ == "__main__":
    main()