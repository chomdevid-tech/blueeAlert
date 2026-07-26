import logging
import os
import random
import time
from pathlib import Path

from dotenv import load_dotenv

from backend.generators.log_generator import (
    SecurityLogGenerator,
)
from backend.rules.rule_engine import RuleEngine
from backend.services.alert_service import AlertService
from backend.services.firebase_service import FirebaseService
from backend.services.log_processing_service import (
    LogProcessingError,
    LogProcessingService,
)
from backend.services.log_service import LogService


BACKEND_DIRECTORY = Path(__file__).resolve().parent
ENVIRONMENT_FILE = BACKEND_DIRECTORY / ".env"
STORAGE_DIRECTORY = BACKEND_DIRECTORY / "storage"
BACKEND_LOG_FILE = STORAGE_DIRECTORY / "backend.log"

STORAGE_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True,
)

load_dotenv(ENVIRONMENT_FILE)

APPLICATION_NAME = os.getenv(
    "APP_NAME",
    "BlueAlert Backend",
)

LOG_LEVEL_NAME = os.getenv(
    "LOG_LEVEL",
    "INFO",
).upper()

LOG_LEVEL = getattr(
    logging,
    LOG_LEVEL_NAME,
    logging.INFO,
)

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(
            BACKEND_LOG_FILE,
            encoding="utf-8",
        ),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)


def process_pending_logs(
    log_service: LogService,
    processing_service: LogProcessingService,
) -> None:
    """
    Process files that were already inside raw_logs
    before the backend started.
    """

    pending_log_files = (
        log_service.list_raw_log_files()
    )

    if not pending_log_files:
        logger.info(
            "No pending raw logs were found"
        )

        return

    logger.info(
        "Found %d pending raw log(s)",
        len(pending_log_files),
    )

    for raw_log_file_path in pending_log_files:
        try:
            processing_service.process_log_file(
                raw_log_file_path
            )

        except LogProcessingError as error:
            logger.error(
                "Pending log failed: %s",
                error,
            )


def generate_and_process_log(
    log_generator: SecurityLogGenerator,
    log_service: LogService,
    processing_service: LogProcessingService,
) -> None:
    """
    Generate, save, and process one random log.
    """

    generated_log = log_generator.generate_log()

    logger.info(
        "New event generated: %s | %s | %s",
        generated_log.log_id,
        generated_log.vm_name,
        generated_log.event_type,
    )

    raw_log_file_path = (
        log_service.save_raw_log(
            generated_log
        )
    )

    generated_alert = (
        processing_service.process_log_file(
            raw_log_file_path
        )
    )

    if generated_alert is None:
        logger.info(
            "Event created no alert: %s",
            generated_log.event_type,
        )

        return

    logger.info(
        "Complete alert flow succeeded: "
        "%s | %s | %s | %s",
        generated_alert.alert_id,
        generated_alert.attack_type,
        generated_alert.severity,
        generated_alert.vm_name,
    )


def main() -> None:
    """
    Run the BlueAlert backend continuously.
    """

    logger.info(
        "%s application started",
        APPLICATION_NAME,
    )

    try:
        log_generator = SecurityLogGenerator()
        log_service = LogService()
        alert_service = AlertService()
        rule_engine = RuleEngine()
        firebase_service = FirebaseService()

        processing_service = LogProcessingService(
            log_service=log_service,
            alert_service=alert_service,
            rule_engine=rule_engine,
            firebase_service=firebase_service,
        )

        process_pending_logs(
            log_service=log_service,
            processing_service=processing_service,
        )

        logger.info(
            "Continuous monitoring started. "
            "Press Ctrl+C to stop."
        )

        while True:
            try:
                generate_and_process_log(
                    log_generator=log_generator,
                    log_service=log_service,
                    processing_service=(
                        processing_service
                    ),
                )

            except Exception:
                logger.exception(
                    "The current processing cycle failed"
                )

            interval_seconds = random.randint(
                5,
                10,
            )

            logger.info(
                "Next log will be generated in "
                "%d seconds",
                interval_seconds,
            )

            time.sleep(interval_seconds)

    except KeyboardInterrupt:
        logger.info(
            "Stop request received from the user"
        )

    except Exception:
        logger.exception(
            "BlueAlert could not start correctly"
        )

    finally:
        logger.info(
            "%s application stopped",
            APPLICATION_NAME,
        )


if __name__ == "__main__":
    main()