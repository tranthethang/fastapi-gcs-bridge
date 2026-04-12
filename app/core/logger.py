"""
Logging configuration for the application using loguru.

- stderr: visible in ``docker logs`` (container stdout/stderr stream).
- ``logs/gcs_bridge_YYYY-MM-DD.log``: daily file under the service working directory
  (with repo bind-mount ``.:/app`` this appears as ``services/gcs-bridge/logs/`` on the host).

Unlike batch-executor's former stdlib + pyflow ``NullHandler`` setup, loguru sinks are
actually attached, so application logs are not swallowed.
"""

import os
import sys
from pathlib import Path

from loguru import logger


def setup_logger():
    """
    Configures loguru: stderr for containers and a rotating daily file for inspection.
    """
    logger.remove()
    level = os.getenv("LOG_LEVEL", "INFO")
    fmt = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"

    logger.add(sys.stderr, format=fmt, level=level)

    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    logger.add(
        str(log_dir / "gcs_bridge_{time:YYYY-MM-DD}.log"),
        format=fmt,
        level=level,
        rotation="00:00",
        retention="30 days",
        compression="gz",
        encoding="utf-8",
    )

    return logger


# Global logger instance
logger = setup_logger()
