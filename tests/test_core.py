"""
Tests for core components like settings and logger.
"""

from unittest.mock import patch

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


def test_setup_logger():
    """Tests that the logger is correctly initialized."""
    logger = setup_logger()
    # Loguru logger should have the 'info' attribute
    assert hasattr(logger, "info")
    assert hasattr(logger, "error")
