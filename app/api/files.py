"""
API endpoints for file operations.
Handles file uploads and interactions with the file service.
"""

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.core import logger
from app.schemas import UploadResponse
from app.services import file_service

# Define the router for file-related endpoints
router = APIRouter()


@router.post("/upload", response_model=UploadResponse)
async def upload_file_to_gemini(
    file: UploadFile = File(...), project_id: str = Form("default")
):
    """
    Endpoint to upload a file to Gemini via the file service.

    Args:
        file: The file to be uploaded.
        project_id: The ID of the project associated with the file.

    Returns:
        UploadResponse: Metadata about the uploaded file.
    """
    logger.info(f"UPLOAD REQUEST: Project='{project_id}', Filename='{file.filename}'")

    # Basic validation for filename
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is empty")

    try:
        # Delegate upload logic to the file service
        return await file_service.upload_file(file, project_id)
    except HTTPException:
        # Re-raise HTTP exceptions to be handled by FastAPI
        raise
    except Exception as e:
        # Log unexpected errors and return a 500 Internal Server Error
        logger.error(f"UPLOAD ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
