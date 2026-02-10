"""
Integration and unit tests for the API layer.
Uses FastAPI TestClient and unittest.mock to simulate requests and service behaviors.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.main import app

# Initialize TestClient with the FastAPI app
client = TestClient(app)


def test_health_check():
    """Tests the health check endpoint returns correct status."""
    with patch(
        "app.main.health_service.check_health", new_callable=AsyncMock
    ) as mock_health:
        mock_health.return_value = {
            "status": "ok",
            "version": "1.0.0",
            "app": "fastapi-gcs-bridge",
        }
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


def test_upload_file_success():
    """Tests successful file upload via the /upload endpoint."""
    with patch(
        "app.api.files.file_service.upload_file", new_callable=AsyncMock
    ) as mock_upload:
        mock_upload.return_value = {
            "hit": False,
            "gemini_uri": "gemini://test",
            "hash": "abc",
            "project": "p1",
        }

        files = {"file": ("test.txt", b"content", "text/plain")}
        data = {"project_id": "p1"}
        response = client.post("/v1/files/upload", files=files, data=data)

        assert response.status_code == 200
        assert response.json()["gemini_uri"] == "gemini://test"


def test_upload_file_no_filename_logic():
    """Tests the error handling when an empty filename is provided."""
    import asyncio

    from fastapi import HTTPException, UploadFile

    from app.api.files import upload_file_to_gemini

    mock_file = MagicMock(spec=UploadFile)
    mock_file.filename = ""

    with pytest.raises(HTTPException) as exc:
        asyncio.run(upload_file_to_gemini(file=mock_file))

    assert exc.value.status_code == 400
    assert exc.value.detail == "Filename is empty"


def test_main_run():
    """Tests the main entry point block execution."""
    import runpy

    with patch("uvicorn.run") as mock_run:
        # Simulate running app/main.py as the main script
        runpy.run_path("app/main.py", run_name="__main__")
        mock_run.assert_called()


def test_upload_file_http_exception():
    """Tests that HTTPExceptions from the service are correctly propagated."""
    with patch(
        "app.api.files.file_service.upload_file", new_callable=AsyncMock
    ) as mock_upload:
        mock_upload.side_effect = HTTPException(
            status_code=413, detail="File too large"
        )

        files = {"file": ("test.txt", b"content", "text/plain")}
        response = client.post("/v1/files/upload", files=files)

        assert response.status_code == 413
        assert response.json()["detail"] == "File too large"


def test_upload_file_internal_error():
    """Tests that unexpected exceptions are converted to 500 Internal Server Error."""
    with patch(
        "app.api.files.file_service.upload_file", new_callable=AsyncMock
    ) as mock_upload:
        mock_upload.side_effect = Exception("Random error")

        files = {"file": ("test.txt", b"content", "text/plain")}
        response = client.post("/v1/files/upload", files=files)

        assert response.status_code == 500
        assert response.json()["detail"] == "Internal Server Error"
