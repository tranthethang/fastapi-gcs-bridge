"""
Logging configuration for the application.
Provides a logger instance with both console and rotating file handlers.
"""

import logging
import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

from app.core.config import settings


def setup_logger():
    """
    Configures and returns the application logger.
    Sets up a TimedRotatingFileHandler that rotates daily and a StreamHandler for console output.
    """
    log_dir = "logs"
    # Ensure log directory exists
    os.makedirs(log_dir, exist_ok=True)

    # Generate log filename based on current date
    log_filename = os.path.join(log_dir, f"{datetime.now().strftime('%Y%m%d')}.log")

    logger = logging.getLogger(settings.APP_NAME)
    logger.setLevel(logging.INFO)

    # Avoid adding multiple handlers if the logger is already configured
    if not logger.handlers:
        # Define log format: Timestamp - Level - Message
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        # Configure file handler with daily rotation at midnight
        handler = TimedRotatingFileHandler(
            log_filename, when="midnight", interval=1, backupCount=30, encoding="utf-8"
        )
        handler.setFormatter(formatter)

        def namer(default_name):
            """Custom naming logic for rotated log files."""
            base_dir = os.path.dirname(default_name)
            try:
                # Expecting format from TimedRotatingFileHandler: filename.YYYY-MM-DD
                date_str = default_name.split(".")[-1]
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                return os.path.join(base_dir, f"{date_obj.strftime('%Y%m%d')}.log")
            except Exception:
                return default_name

        handler.namer = namer
        logger.addHandler(handler)

        # Configure console handler
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)

    return logger


# Global logger instance
logger = setup_logger()
