"""
Configuration settings for the application.
Uses pydantic-settings to manage environment variables.
"""

from pathlib import Path

from pydantic import AliasChoices, Field
from pydantic_settings import SettingsConfigDict
from pyflow_ai_stack.core.config import Settings as BaseSettings
from pyflow_ai_stack.services.configs import S3Config

_REPO_ROOT = Path(__file__).resolve().parents[4]
_SERVICE_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """
    Application settings class inheriting from pyflow_ai_stack BaseSettings.
    Automatically loads variables from .env file.
    """

    model_config = SettingsConfigDict(
        env_file=(
            _SERVICE_ROOT / ".env",
            _REPO_ROOT / ".env",
            ".env",
        ),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # General Application Settings
    APP_NAME: str = "fastapi-gcs-bridge"
    DEBUG: bool = False
    APP_PORT: int = 80

    # Cache configuration (Redis)
    # Default TTL is set to 47 hours to comply with Gemini File API limits
    CACHE_TTL: int = 169200  # 47 hours

    # Same S3 env names as gemini-pipeline (pyflow defaults to AWS_* / S3_ENDPOINT_URL).
    AWS_ACCESS_KEY_ID: str | None = Field(
        default="minioadmin",
        validation_alias=AliasChoices("AWS_ACCESS_KEY_ID", "S3_ACCESS_KEY"),
    )
    AWS_SECRET_ACCESS_KEY: str | None = Field(
        default="minioadmin123",
        validation_alias=AliasChoices("AWS_SECRET_ACCESS_KEY", "S3_SECRET_KEY"),
    )
    S3_BUCKET_NAME: str | None = Field(
        default="gemini-pipeline",
        validation_alias=AliasChoices("S3_BUCKET_NAME", "S3_BUCKET"),
    )
    S3_ENDPOINT_URL: str | None = Field(
        default="http://localhost:9000",
        validation_alias=AliasChoices("S3_ENDPOINT_URL", "S3_ENDPOINT"),
    )

    @property
    def s3(self) -> S3Config:
        """S3/MinIO config; path-style addressing for custom endpoints (MinIO)."""
        endpoint = self.S3_ENDPOINT_URL
        return S3Config(
            access_key_id=self.AWS_ACCESS_KEY_ID,
            secret_access_key=self.AWS_SECRET_ACCESS_KEY,
            region=self.AWS_REGION,
            bucket_name=self.S3_BUCKET_NAME,
            endpoint_url=endpoint,
            with_path_style=bool(endpoint),
        )


# Global settings instance
settings = Settings()
