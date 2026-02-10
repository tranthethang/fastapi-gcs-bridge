"""
Tests for core components like settings and logger.
"""

import logging
import os
from unittest.mock import MagicMock, patch

from app.core.config import Settings, settings
from app.core.logger import setup_logger


def test_settings_defaults():
    """Verifies that default settings are correctly loaded."""
    assert settings.APP_NAME == "fastapi-gcs-bridge"
    assert settings.DEBUG is True
    assert settings.APP_PORT == 60060


def test_settings_custom():
    """Verifies that custom settings can be instantiated."""
    custom_settings = Settings(APP_NAME="custom-app", DEBUG=True)
    assert custom_settings.APP_NAME == "custom-app"
    assert custom_settings.DEBUG is True


import importlib
import sys


@patch("logging.handlers.TimedRotatingFileHandler")
@patch("os.makedirs")
def test_setup_logger(mock_makedirs, mock_handler):
    """Tests that the logger is correctly initialized with expected handlers."""
    mock_handler_instance = MagicMock()
    mock_handler.return_value = mock_handler_instance

    # Clear handlers to force setup_logger to run logic inside the if block
    from app.core import logger as app_logger

    app_logger.handlers = []

    # Ensure we reload the module to trigger logger setup
    if "app.core.logger" in sys.modules:
        del sys.modules["app.core.logger"]
    import app.core.logger

    importlib.reload(app.core.logger)

    assert mock_makedirs.called
    assert mock_handler.called


def test_logger_namer():
    """Tests the custom log file naming logic for rotations."""
    # Test the namer function inside setup_logger
    import app.core.logger

    # Use slice assignment to clear the actual list object from the logger instance
    app.core.logger.logger.handlers[:] = []

    # We want to capture the function assigned to .namer
    with patch("app.core.logger.TimedRotatingFileHandler") as mock_handler_cls:
        # Create a mock object to capture attributes assigned by setup_logger
        class Handler:
            def setFormatter(self, f):
                pass

        handler_instance = Handler()
        mock_handler_cls.return_value = handler_instance

        from app.core.logger import setup_logger

        setup_logger()

        # handler_instance.namer should now be the actual function assigned in setup_logger
        actual_namer = handler_instance.namer

        # Verify the namer function logic for valid and invalid date formats
        assert actual_namer("logs/app.log.2023-10-27") == os.path.join(
            "logs", "20231027.log"
        )
        assert actual_namer("app.log.invalid") == "app.log.invalid"
