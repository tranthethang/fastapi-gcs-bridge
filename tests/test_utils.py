"""
Unit tests for utility functions.
"""

from app.utils.hash import calculate_hash


def test_calculate_hash():
    """Verifies SHA256 hash calculation for a standard string."""
    content = b"hello world"
    expected_hash = "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"
    assert calculate_hash(content) == expected_hash


def test_calculate_hash_empty():
    """Verifies SHA256 hash calculation for empty content."""
    content = b""
    expected_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    assert calculate_hash(content) == expected_hash
