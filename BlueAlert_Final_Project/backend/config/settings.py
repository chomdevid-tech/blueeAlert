import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


# The main backend folder.
BACKEND_DIRECTORY = Path(__file__).resolve().parents[1]

# The real environment file.
ENVIRONMENT_FILE = BACKEND_DIRECTORY / ".env"


@dataclass(frozen=True)
class Settings:
    """
    Stores validated BlueAlert backend settings.
    """

    firebase_database_url: str
    firebase_credentials_path: Path


def load_settings() -> Settings:
    """
    Read and validate Firebase settings from backend/.env.
    """

    load_dotenv(ENVIRONMENT_FILE)

    firebase_database_url = os.getenv(
        "FIREBASE_DATABASE_URL",
        "",
    ).strip()

    credentials_path_value = os.getenv(
        "FIREBASE_CREDENTIALS_PATH",
        "",
    ).strip()

    if not firebase_database_url:
        raise ValueError(
            "FIREBASE_DATABASE_URL is missing "
            "from backend/.env."
        )

    if not credentials_path_value:
        raise ValueError(
            "FIREBASE_CREDENTIALS_PATH is missing "
            "from backend/.env."
        )

    firebase_credentials_path = Path(
        credentials_path_value
    )

    # Convert a relative path into a complete path.
    if not firebase_credentials_path.is_absolute():
        firebase_credentials_path = (
            BACKEND_DIRECTORY
            / firebase_credentials_path
        )

    firebase_credentials_path = (
        firebase_credentials_path.resolve()
    )

    if not firebase_credentials_path.exists():
        raise FileNotFoundError(
            "Firebase service-account file "
            f"was not found: {firebase_credentials_path}"
        )

    if (
        firebase_credentials_path.suffix.lower()
        != ".json"
    ):
        raise ValueError(
            "Firebase credentials must be a JSON file."
        )

    return Settings(
        firebase_database_url=(
            firebase_database_url.rstrip("/")
        ),
        firebase_credentials_path=(
            firebase_credentials_path
        ),
    )