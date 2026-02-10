"""
API module initialization.
Exposes routers from submodules for central registration in main.py.
"""

from .files import router as files_router

__all__ = ["files_router"]
