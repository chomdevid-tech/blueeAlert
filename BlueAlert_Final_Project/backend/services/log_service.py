import json
import logging
import shutil
from pathlib import Path

from backend.models.security_log import SecurityLog


logger = logging.getLogger(__name__)


class DuplicateLogError(Exception):
    """
    Raised when a log with the same filename already exists.
    """


class InvalidLogFileError(Exception):
    """
    Raised when a raw log file contains invalid JSON or fields.
    """


class LogStorageError(Exception):
    """
    Raised when a log file cannot be saved, read, or moved.
    """


class LogService:
    """
    Manages raw, processed, and failed security-log files.
    """

    def __init__(
        self,
        raw_logs_directory: Path | None = None,
        processed_logs_directory: Path | None = None,
        failed_logs_directory: Path | None = None,
    ) -> None:
        backend_directory = Path(__file__).resolve().parents[1]
        storage_directory = backend_directory / "storage"

        self.raw_logs_directory = (
            raw_logs_directory
            if raw_logs_directory is not None
            else storage_directory / "raw_logs"
        )

        self.processed_logs_directory = (
            processed_logs_directory
            if processed_logs_directory is not None
            else storage_directory / "processed_logs"
        )

        self.failed_logs_directory = (
            failed_logs_directory
            if failed_logs_directory is not None
            else storage_directory / "failed_logs"
        )

        for directory in (
            self.raw_logs_directory,
            self.processed_logs_directory,
            self.failed_logs_directory,
        ):
            directory.mkdir(
                parents=True,
                exist_ok=True,
            )

    def save_raw_log(
        self,
        security_log: SecurityLog,
    ) -> Path:
        """
        Save one SecurityLog in JSON Lines format.
        """

        if not isinstance(security_log, SecurityLog):
            raise TypeError(
                "security_log must be a SecurityLog object."
            )

        raw_log_file_path = (
            self.raw_logs_directory
            / f"{security_log.log_id}.jsonl"
        )

        json_line = json.dumps(
            security_log.to_dict(),
            ensure_ascii=False,
        )

        try:
            with raw_log_file_path.open(
                mode="x",
                encoding="utf-8",
            ) as raw_log_file:
                raw_log_file.write(json_line + "\n")

        except FileExistsError as error:
            logger.warning(
                "Duplicate security log rejected: %s",
                security_log.log_id,
            )

            raise DuplicateLogError(
                f"A raw log with ID "
                f"'{security_log.log_id}' already exists."
            ) from error

        except OSError as error:
            logger.exception(
                "Failed to save security log: %s",
                security_log.log_id,
            )

            raise LogStorageError(
                "The security log could not be saved."
            ) from error

        logger.info(
            "Raw security log saved: %s",
            raw_log_file_path,
        )

        return raw_log_file_path

    def read_raw_log_file(
        self,
        raw_log_file_path: Path,
    ) -> SecurityLog:
        """
        Read one JSON Lines file and convert it into
        a validated SecurityLog.
        """

        raw_log_file_path = Path(raw_log_file_path)

        try:
            file_content = raw_log_file_path.read_text(
                encoding="utf-8"
            )

        except OSError as error:
            raise LogStorageError(
                f"Could not read log file "
                f"'{raw_log_file_path.name}'."
            ) from error

        non_empty_lines = [
            line.strip()
            for line in file_content.splitlines()
            if line.strip()
        ]

        if len(non_empty_lines) != 1:
            raise InvalidLogFileError(
                "Each raw log file must contain exactly "
                "one non-empty JSON line."
            )

        try:
            raw_log_data = json.loads(
                non_empty_lines[0]
            )

        except json.JSONDecodeError as error:
            raise InvalidLogFileError(
                "The raw log contains invalid JSON."
            ) from error

        if not isinstance(raw_log_data, dict):
            raise InvalidLogFileError(
                "The raw log JSON must be an object."
            )

        try:
            security_log = SecurityLog.from_dict(
                raw_log_data
            )

        except ValueError as error:
            raise InvalidLogFileError(
                f"Invalid security log fields: {error}"
            ) from error

        logger.info(
            "Raw security log read successfully: %s",
            raw_log_file_path.name,
        )

        return security_log

    def list_raw_log_files(self) -> list[Path]:
        """
        Return every unprocessed .jsonl file.
        """

        return sorted(
            self.raw_logs_directory.glob("*.jsonl")
        )

    def move_to_processed(
        self,
        raw_log_file_path: Path,
    ) -> Path:
        """
        Move a successfully checked log to processed_logs.
        """

        return self._move_log_file(
            source_file_path=raw_log_file_path,
            destination_directory=(
                self.processed_logs_directory
            ),
        )

    def move_to_failed(
        self,
        raw_log_file_path: Path,
    ) -> Path:
        """
        Move an invalid or failed log to failed_logs.
        """

        return self._move_log_file(
            source_file_path=raw_log_file_path,
            destination_directory=(
                self.failed_logs_directory
            ),
        )

    def _move_log_file(
        self,
        source_file_path: Path,
        destination_directory: Path,
    ) -> Path:
        """
        Move one file without replacing an existing file.
        """

        source_file_path = Path(source_file_path)

        if not source_file_path.exists():
            raise LogStorageError(
                f"Source log file does not exist: "
                f"{source_file_path}"
            )

        destination_file_path = (
            destination_directory
            / source_file_path.name
        )

        if destination_file_path.exists():
            raise DuplicateLogError(
                f"The destination already contains "
                f"'{source_file_path.name}'."
            )

        try:
            shutil.move(
                str(source_file_path),
                str(destination_file_path),
            )

        except OSError as error:
            raise LogStorageError(
                f"Could not move log file "
                f"'{source_file_path.name}'."
            ) from error

        logger.info(
            "Security log moved to: %s",
            destination_file_path,
        )

        return destination_file_path