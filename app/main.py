"""
Main entry point for the FastAPI application.
This module initializes the FastAPI app, includes routers, and defines the health check endpoint.
"""

import uvicorn
from fastapi import FastAPI
from pyflow_ai_stack.schemas.models import HealthResponse

from app.api import files_router
from app.core import settings
from app.services import health_service

# Initialize FastAPI application with settings
app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

# Register API routers
app.include_router(files_router, prefix="/v1/files", tags=["files"])


@app.get("/health", response_model=HealthResponse, response_model_exclude_none=True)
async def health_check(depends: int = 0):
    """
    Health check endpoint to verify the service status.

    Args:
        depends: Optional flag to include dependency health checks.

    Returns:
        HealthResponse object containing service status.
    """
    return await health_service.check_health(depends)


if __name__ == "__main__":
    # Start uvicorn server when executed directly
    uvicorn.run(
        "app.main:app", host="0.0.0.0", port=settings.APP_PORT, reload=settings.DEBUG
    )
