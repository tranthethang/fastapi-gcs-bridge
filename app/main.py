import uvicorn
from fastapi import FastAPI
from pyflow_ai_stack.schemas.models import HealthResponse

from app.api.files import router as files_router
from app.core.config import settings
from app.services import health_service

app = FastAPI(title="FastAPI Gemini Bridge")

# Include routers
app.include_router(files_router, prefix="/v1/files", tags=["files"])


@app.get("/health", response_model=HealthResponse, response_model_exclude_none=True)
async def health_check(depends: int = 0):
    """
    Check the health of the application and its dependencies.

    Args:
        depends (int): Whether to check external dependencies (Redis, Gemini, S3).
                       If 1, check dependencies; otherwise, only check app status.

    Returns:
        dict: A dictionary containing the health status of the application and its dependencies.
    """
    return await health_service.check_health(depends)


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app", host="0.0.0.0", port=settings.APP_PORT, reload=settings.DEBUG
    )
