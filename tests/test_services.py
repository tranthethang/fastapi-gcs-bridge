"""
Tests for the service layer, specifically FileService.
Uses mocks for Redis and Gemini services to isolate business logic.
"""

import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import HTTPException, UploadFile

from app.services.file_service import FileService


@pytest.fixture(autouse=True)
def mock_logger():
    """Fixture to mock the logger to avoid actual logging during tests."""
    # Patch the logger in app.core, which is what file_service uses
    with patch("app.core.logger.logger.info") as mock_info, patch(
        "app.core.logger.logger.error"
    ) as mock_error, patch("app.core.logger.logger.warning") as mock_warning:
        yield {"info": mock_info, "error": mock_error, "warning": mock_warning}


@pytest.fixture
def mock_gemini():
    """Fixture for a mocked Gemini service."""
    return AsyncMock()


@pytest.fixture
def mock_redis():
    """Fixture for a mocked Redis service."""
    return AsyncMock()


@pytest.fixture
def file_service(mock_gemini, mock_redis):
    """Fixture to provide a FileService instance with mocked dependencies."""
    return FileService(mock_gemini, mock_redis)


@pytest.mark.asyncio
async def test_upload_file_empty(file_service):
    """Verifies that uploading an empty file raises a 400 HTTPException."""
    mock_file = AsyncMock(spec=UploadFile)
    mock_file.read.return_value = b""

    with pytest.raises(HTTPException) as excinfo:
        await file_service.upload_file(mock_file, "test_project")

    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "File is empty"


@pytest.mark.asyncio
async def test_upload_file_cache_hit(file_service, mock_redis):
    """Verifies that a cache hit returns the cached URI without re-uploading."""
    mock_file = AsyncMock(spec=UploadFile)
    mock_file.read.return_value = b"test content"
    mock_redis.get.return_value = "gemini://cached_uri"

    result = await file_service.upload_file(mock_file, "test_project")

    assert result["hit"] is True
    assert result["gemini_uri"] == "gemini://cached_uri"
    mock_redis.get.assert_called_once()


@pytest.mark.asyncio
async def test_upload_file_cache_miss(file_service, mock_gemini, mock_redis):
    """Verifies that a cache miss triggers a file upload to Gemini and caches the result."""
    mock_file = AsyncMock(spec=UploadFile)
    mock_file.read.return_value = b"new content"
    mock_file.filename = "test.txt"
    mock_file.content_type = "text/plain"

    mock_redis.get.return_value = None

    mock_gemini_file = MagicMock()
    mock_gemini_file.uri = "gemini://new_uri"
    mock_gemini.upload_file.return_value = mock_gemini_file

    with patch("builtins.open", MagicMock()):
        result = await file_service.upload_file(mock_file, "test_project")

    assert result["hit"] is False
    assert result["gemini_uri"] == "gemini://new_uri"
    assert result["project"] == "test_project"

    mock_gemini.upload_file.assert_called_once()
    mock_redis.set.assert_called_once()


@pytest.mark.asyncio
async def test_upload_file_cleanup_on_error(file_service, mock_gemini, mock_redis):
    """Verifies that temporary files are cleaned up even if the upload fails."""
    mock_file = AsyncMock(spec=UploadFile)
    mock_file.read.return_value = b"content for error"
    mock_file.filename = "error.txt"
    mock_file.content_type = "text/plain"

    mock_redis.get.return_value = None
    mock_gemini.upload_file.side_effect = Exception("Upload failed")

    with patch("os.remove") as mock_remove, patch(
        "os.path.exists", return_value=True
    ), patch("builtins.open", MagicMock()):
        with pytest.raises(Exception):
            await file_service.upload_file(mock_file, "test_project")

        mock_remove.assert_called()
