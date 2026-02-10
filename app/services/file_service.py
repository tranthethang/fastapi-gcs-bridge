"""
Service layer for handling file operations.
Implements business logic for uploading files to Gemini with Redis caching.
"""

import os
import time

from fastapi import HTTPException, UploadFile

from app.core import logger, settings
from app.utils import calculate_hash


class FileService:
    """
    Service responsible for coordinating file uploads between Redis cache and Gemini API.
    """

    def __init__(self, gemini_service, redis_service):
        """
        Initialize the service with Gemini and Redis services.
        """
        self.gemini = gemini_service
        self.redis = redis_service

    async def upload_file(self, file: UploadFile, project_id: str):
        """
        Uploads a file to Gemini, checking the Redis cache first for deduplication.

        Args:
            file: The UploadFile object from FastAPI.
            project_id: The project identifier.

        Returns:
            dict: Contains upload status, URI, hash, and project ID.
        """
        content = await file.read()
        if not content:
            raise HTTPException(status_code=400, detail="File is empty")

        # Calculate SHA256 hash for deduplication
        file_hash = calculate_hash(content)

        # Check if the file has already been uploaded (using hash as key)
        cached_uri = await self.redis.get(file_hash)

        if cached_uri:
            logger.info(f"CACHE HIT: {file_hash}")
            return {"hit": True, "gemini_uri": cached_uri, "hash": file_hash}

        # Temporary file path for Gemini SDK upload
        temp_path = f"temp_{file_hash}_{file.filename}"
        try:
            # Write content to a temporary file
            with open(temp_path, "wb") as f:
                f.write(content)

            start_time = time.time()
            # Upload to Gemini File API
            gemini_file = await self.gemini.upload_file(
                temp_path, file.filename, file.content_type
            )

            # Store the Gemini URI in Redis with a TTL
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
            # Clean up the temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
