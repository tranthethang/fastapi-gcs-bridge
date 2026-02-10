import logging
import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

from app.core.config import settings


def setup_logger():
    """Configure and return the application logger."""
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_filename = os.path.join(log_dir, f"{datetime.now().strftime('%Y%m%d')}.log")

    logger = logging.getLogger(settings.APP_NAME)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler = TimedRotatingFileHandler(
            log_filename, when="midnight", interval=1, backupCount=30, encoding="utf-8"
        )
        handler.setFormatter(formatter)

        def namer(default_name):
            base_dir = os.path.dirname(default_name)
            try:
                date_str = default_name.split(".")[-1]
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                return os.path.join(base_dir, f"{date_obj.strftime('%Y%m%d')}.log")
            except Exception:
                return default_name

        handler.namer = namer
        logger.addHandler(handler)

        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)

    return logger


logger = setup_logger()
