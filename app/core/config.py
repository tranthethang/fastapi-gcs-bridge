"""
Configuration management module for the FastAPI application.

This module uses Pydantic Settings to load configuration from environment variables
and .env files. It provides structured access to application, Gemini, Redis, and S3 settings.
"""

from typing import Optional

from pydantic_settings import SettingsConfigDict
from pyflow_ai_stack.core.config import Settings as BaseSettings


class Settings(BaseSettings):
    """
    Application settings class using Pydantic Settings.

    Attributes:
        APP_NAME (str): Name of the application.
        DEBUG (bool): Debug mode flag.
        APP_PORT (int): Port number for the application.
        CACHE_TTL (int): Cache TTL for Redis.
    """

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    APP_NAME: str = "fastapi-boilerplate"
    DEBUG: bool = False
    APP_PORT: int = 80
    CACHE_TTL: int = 169200  # 47 hours


# Create a singleton instance
settings = Settings()


# Maintain backward compatibility for existing code during transition
class Config:
    """
    Legacy configuration class for backward compatibility.

    Provides static access to settings loaded from the Settings instance.
    """

    APP_NAME = settings.APP_NAME
    DEBUG = settings.DEBUG
    APP_PORT = settings.APP_PORT
    GEMINI_API_KEY = settings.GEMINI_API_KEY
    GEMINI_MODEL = settings.GEMINI_MODEL
    AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
    AWS_REGION = settings.AWS_REGION
    S3_BUCKET_NAME = settings.S3_BUCKET_NAME
    S3_ENDPOINT_URL = settings.S3_ENDPOINT_URL
    REDIS_HOST = settings.REDIS_HOST
    REDIS_PORT = settings.REDIS_PORT
    REDIS_PASSWORD = settings.REDIS_PASSWORD
    REDIS_DB = settings.REDIS_DB
    CONCURRENCY_LIMIT = settings.CONCURRENCY_LIMIT
    CACHE_TTL = settings.CACHE_TTL
