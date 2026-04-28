"""
Tests for core components like settings and logger.
"""

import pytest

from app.core.config import Settings, settings
from app.core.logger import setup_logger


def test_settings_defaults(monkeypatch: pytest.MonkeyPatch):
    """Verifies that class defaults apply when env is not set."""
    monkeypatch.delenv("DEBUG", raising=False)
    monkeypatch.delenv("APP_PORT", raising=False)
    monkeypatch.delenv("APP_NAME", raising=False)

    default_settings = Settings(_env_file=None)
    assert default_settings.APP_NAME == "fastapi-gcs-bridge"
    assert default_settings.DEBUG is False
    assert default_settings.APP_PORT == 80


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
