"""
Schemas module initialization.
Exposes Pydantic models from submodules for easy access.
"""

from .files import UploadResponse

__all__ = ["UploadResponse"]
