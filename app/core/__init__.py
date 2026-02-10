"""
Core module initialization.
Exposes foundational components like settings and logger.
"""

from .config import settings
from .logger import logger

__all__ = ["settings", "logger"]
