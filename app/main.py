import uvicorn
from fastapi import FastAPI
from pyflow_ai_stack.schemas.models import HealthResponse

from app.api import files_router
from app.core import settings
from app.services import health_service

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

app.include_router(files_router, prefix="/v1/files", tags=["files"])


@app.get("/health", response_model=HealthResponse, response_model_exclude_none=True)
async def health_check(depends: int = 0):
    return await health_service.check_health(depends)


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app", host="0.0.0.0", port=settings.APP_PORT, reload=settings.DEBUG
    )
