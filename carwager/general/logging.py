import logging
import os

from general.logging_context import request_id_var


class ContextFilter(logging.Filter):
    """
    Adds common contextual fields to every log record.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        record.service = os.getenv(
            "SERVICE_NAME",
            "django",
        )

        record.environment = os.getenv(
            "ENVIRONMENT",
            "development",
        )

        record.request_id = request_id_var.get()

        return True
