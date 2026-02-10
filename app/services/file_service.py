import os
import time

from fastapi import HTTPException, UploadFile

from app.core import logger, settings
from app.utils import calculate_hash


class FileService:
    def __init__(self, gemini_service, redis_service):
        self.gemini = gemini_service
        self.redis = redis_service

    async def upload_file(self, file: UploadFile, project_id: str):
        content = await file.read()
        if not content:
            raise HTTPException(status_code=400, detail="File is empty")

        file_hash = calculate_hash(content)
        cached_uri = await self.redis.get(file_hash)

        if cached_uri:
            logger.info(f"CACHE HIT: {file_hash}")
            return {"hit": True, "gemini_uri": cached_uri, "hash": file_hash}

        temp_path = f"temp_{file_hash}_{file.filename}"
        try:
            with open(temp_path, "wb") as f:
                f.write(content)

            start_time = time.time()
            gemini_file = await self.gemini.upload_file(
                temp_path, file.filename, file.content_type
            )

            await self.redis.set(file_hash, gemini_file.uri, expire=settings.CACHE_TTL)

            logger.info(
                f"UPLOAD SUCCESS: {gemini_file.uri} in {time.time() - start_time:.2f}s"
            )
            return {
                "hit": False,
                "gemini_uri": gemini_file.uri,
                "hash": file_hash,
                "project": project_id,
            }
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
