import uvicorn
from fastapi import FastAPI

from app.api.files import router as files_router
from app.config import Config

app = FastAPI(title="FastAPI Gemini Bridge")

# Include routers
app.include_router(files_router, prefix="/v1/files", tags=["files"])

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=Config.APP_PORT, reload=True)
