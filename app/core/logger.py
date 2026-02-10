"""
Logging configuration for the application using loguru.
"""

import sys

from loguru import logger


def setup_logger():
    """
    Configures and returns the application logger.
    Outputs to stderr with a custom format suitable for container logs.
    """
    # Remove default handler
    logger.remove()

    # Add custom handler for stderr
    logger.add(
        sys.stderr,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        level="INFO",
    )

    return logger


# Global logger instance
logger = setup_logger()
