from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.core import logger
from app.schemas import UploadResponse
from app.services import file_service

router = APIRouter()


@router.post("/upload", response_model=UploadResponse)
async def upload_file_to_gemini(
    file: UploadFile = File(...), project_id: str = Form("default")
):
    logger.info(f"UPLOAD REQUEST: Project='{project_id}', Filename='{file.filename}'")

    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is empty")

    try:
        return await file_service.upload_file(file, project_id)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"UPLOAD ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
