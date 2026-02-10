from pydantic_settings import SettingsConfigDict
from pyflow_ai_stack.core.config import Settings as BaseSettings


class Settings(BaseSettings):
    """
    Application settings class inheriting from pyflow_ai_stack.
    """

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    APP_NAME: str = "fastapi-gemini-bridge"
    DEBUG: bool = False
    APP_PORT: int = 80
    CACHE_TTL: int = 169200  # 47 hours


settings = Settings()
