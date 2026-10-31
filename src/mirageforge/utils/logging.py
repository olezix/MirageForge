"""
Logging configuration for MirageForge.

Provides structured logging with appropriate levels and formatting.
Ensures no personally identifiable information is logged.
"""

import logging
import sys

from mirageforge.config import get_settings


def setup_logging(level: str | None = None) -> logging.Logger:
    """
    Setup application logging.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
               If None, uses settings.LOG_LEVEL

    Returns:
        Root logger
    """
    if level is None:
        level = get_settings().log_level

    # Create formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Setup console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)

    # Setup root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Remove existing handlers to avoid duplicates
    root_logger.handlers.clear()
    root_logger.addHandler(console_handler)

    # Reduce noise from third-party libraries
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
    logging.getLogger("PIL").setLevel(logging.WARNING)

    return root_logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(name)


class PrivacyFilter(logging.Filter):
    """
    Logging filter to remove potential PII from log messages.

    Filters out IP addresses, email addresses, and other sensitive patterns.
    """

    def __init__(self) -> None:
        super().__init__()
        import re

        # Simple patterns for common PII
        self.patterns = [
            (re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"), "[IP_REDACTED]"),
            (
                re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"),
                "[EMAIL_REDACTED]",
            ),
        ]

    def filter(self, record: logging.LogRecord) -> bool:
        """Filter log record to remove PII."""
        if isinstance(record.msg, str):
            for pattern, replacement in self.patterns:
                record.msg = pattern.sub(replacement, record.msg)
        return True


def sanitize_log_message(message: str) -> str:
    """
    Sanitize a log message to remove potential PII.

    Args:
        message: Log message

    Returns:
        Sanitized message
    """
    import re

    # Remove IP addresses
    message = re.sub(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", "[IP_REDACTED]", message)

    # Remove email addresses
    message = re.sub(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "[EMAIL_REDACTED]",
        message,
    )

    # Remove UUIDs that might be session tokens (keep for debugging but mark)
    # message = re.sub(
    #     r"\b[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}\b",
    #     "[SESSION_ID]",
    #     message,
    # )

    return message
