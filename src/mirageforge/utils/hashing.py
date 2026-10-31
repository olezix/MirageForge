"""
Hashing utilities for checksums and deterministic identifiers.

Provides SHA256 hashing for files and data to ensure reproducibility
and integrity of stimuli and artifacts.
"""

import hashlib
from pathlib import Path
from typing import Any


def hash_file(file_path: str | Path) -> str:
    """
    Calculate SHA256 hash of a file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Hexadecimal SHA256 hash string
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256_hash.update(chunk)
    
    return sha256_hash.hexdigest()


def hash_bytes(data: bytes) -> str:
    """
    Calculate SHA256 hash of bytes.
    
    Args:
        data: Bytes to hash
        
    Returns:
        Hexadecimal SHA256 hash string
    """
    return hashlib.sha256(data).hexdigest()


def hash_dict(data: dict[str, Any]) -> str:
    """
    Calculate SHA256 hash of a dictionary.
    
    Dictionary is serialized to a canonical JSON string before hashing.
    
    Args:
        data: Dictionary to hash
        
    Returns:
        Hexadecimal SHA256 hash string
    """
    import json
    
    # Sort keys for deterministic serialization
    canonical = json.dumps(data, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def hash_string(text: str) -> str:
    """
    Calculate SHA256 hash of a string.
    
    Args:
        text: String to hash
        
    Returns:
        Hexadecimal SHA256 hash string
    """
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def generate_uuid_from_seed(seed: int) -> str:
    """
    Generate a deterministic UUID-like string from a seed.
    
    Not a real UUID, but provides deterministic identifiers for testing.
    
    Args:
        seed: Integer seed
        
    Returns:
        UUID-like string (8-4-4-4-12 format)
    """
    hash_str = hash_string(str(seed))
    # Format as UUID-like string
    return f"{hash_str[:8]}-{hash_str[8:12]}-{hash_str[12:16]}-{hash_str[16:20]}-{hash_str[20:32]}"
