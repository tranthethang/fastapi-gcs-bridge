from typing import Optional

from pydantic import BaseModel


class UploadResponse(BaseModel):
    hit: bool
    gemini_uri: str
    hash: str
    project: Optional[str] = None
