import time

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.config import Config
from app.logger import logger
from app.schemas.files import UploadResponse
from app.services.gemini_service import gemini_service
from app.services.redis_service import redis_service
from app.utils.hash import calculate_hash

router = APIRouter()


@router.post("/upload", response_model=UploadResponse)
async def upload_file_to_gemini(
    file: UploadFile = File(...), project_id: str = Form("default")
):
    logger.info(f"RECEIVED REQUEST: Project='{project_id}', Filename='{file.filename}'")
    if not file.filename:
        logger.error("VALIDATION ERROR: Filename is empty")
        raise HTTPException(status_code=400, detail="Filename is empty")

    try:
        content = await file.read()
        if not content:
            logger.error("VALIDATION ERROR: File is empty")
            raise HTTPException(status_code=400, detail="File is empty")

        file_hash = calculate_hash(content)

        cached_uri = await redis_service.get(file_hash)
        if cached_uri:
            logger.info(f"CACHE HIT: File hash {file_hash} already exists.")
            return {"hit": True, "gemini_uri": cached_uri, "hash": file_hash}

        temp_path = f"temp_{file_hash}_{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(content)

        start_time = time.time()
        gemini_file = await gemini_service.upload_file(
            temp_path, file.filename, file.content_type
        )

        await redis_service.set(file_hash, gemini_file.uri, expire=Config.CACHE_TTL)

        duration = time.time() - start_time
        logger.info(f"UPLOAD SUCCESS: URI={gemini_file.uri} in {duration:.2f}s")

        return {
            "hit": False,
            "gemini_uri": gemini_file.uri,
            "hash": file_hash,
            "project": project_id,
        }
    except Exception as e:
        logger.error(f"PROCESS ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
