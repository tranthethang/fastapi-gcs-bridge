"""
Configuration settings for the application.
Uses pydantic-settings to manage environment variables.
"""

from pydantic_settings import SettingsConfigDict
from pyflow_ai_stack.core.config import Settings as BaseSettings


class Settings(BaseSettings):
    """
    Application settings class inheriting from pyflow_ai_stack BaseSettings.
    Automatically loads variables from .env file.
    """

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # General Application Settings
    APP_NAME: str = "fastapi-gemini-bridge"
    DEBUG: bool = False
    APP_PORT: int = 80

    # Cache configuration (Redis)
    # Default TTL is set to 47 hours to comply with Gemini File API limits
    CACHE_TTL: int = 169200  # 47 hours


# Global settings instance
settings = Settings()
