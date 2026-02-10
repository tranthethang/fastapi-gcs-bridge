"""
Services initialization module.
This module instantiates the core service singletons used throughout the application.
"""

from pyflow_ai_stack.services.gemini_service import GeminiService
from pyflow_ai_stack.services.health_service import HealthService
from pyflow_ai_stack.services.redis_service import RedisService
from pyflow_ai_stack.services.s3_service import S3Service

from app.core.config import settings
from app.services.file_service import FileService

# Initialize core singleton instances using application settings
gemini_service = GeminiService(settings.gemini)
s3_service = S3Service(settings.s3)
redis_service = RedisService(settings.redis)

# Initialize the file service with Gemini and Redis dependencies
file_service = FileService(gemini_service, redis_service)

# Initialize the health service to monitor dependencies
health_service = HealthService(
    redis_service=redis_service,
    gemini_service=gemini_service,
    s3_service=s3_service,
    app_name=settings.APP_NAME,
)

# Exported service instances
__all__ = [
    "gemini_service",
    "s3_service",
    "redis_service",
    "file_service",
    "health_service",
]
