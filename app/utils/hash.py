import hashlib


def calculate_hash(file_content: bytes) -> str:
    """Calculate SHA256 to uniquely identify files."""
    return hashlib.sha256(file_content).hexdigest()
