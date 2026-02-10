"""
Utility functions for hash calculations.
Used for file deduplication and cache keys.
"""

import hashlib


def calculate_hash(file_content: bytes) -> str:
    """
    Calculates the SHA256 hash of the given file content.

    Args:
        file_content: The binary content of the file.

    Returns:
        str: The hexadecimal representation of the SHA256 hash.
    """
    return hashlib.sha256(file_content).hexdigest()
