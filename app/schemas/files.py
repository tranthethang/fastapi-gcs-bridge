"""
Pydantic schemas for file-related operations.
Defines the structure of request and response models.
"""

from typing import Optional

from pydantic import BaseModel


class UploadResponse(BaseModel):
    """
    Response model for file upload operations.
    """

    # Indicates if the file was found in cache (hit=True) or uploaded to Gemini (hit=False)
    hit: bool
    # The URI assigned to the file by Gemini
    gemini_uri: str
    # The SHA256 hash of the uploaded file
    hash: str
    # The project ID associated with the upload
    project: Optional[str] = None
