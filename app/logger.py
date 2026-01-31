import logging
import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler


def setup_logger():
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_filename = os.path.join(log_dir, f"{datetime.now().strftime('%Y%m%d')}.log")

    logger = logging.getLogger("gemini-bridge")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = TimedRotatingFileHandler(
            log_filename, when="midnight", interval=1, backupCount=30
        )
        handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        logger.addHandler(handler)
        logger.addHandler(logging.StreamHandler())

    return logger


logger = setup_logger()
