import os
import mimetypes
from typing import Optional, Tuple
from pathlib import Path

from app.core.config import settings
from app.core.exceptions import UnsupportedFileTypeError, FileSizeExceededError


def get_file_extension(filename: str) -> str:
    """Get file extension from filename"""
    return Path(filename).suffix.lower()


def validate_file_type(filename: str) -> str:
    """Validate file type and return category"""
    extension = get_file_extension(filename)
    
    if extension in settings.supported_text_extensions:
        return "text"
    elif extension in settings.supported_doc_extensions:
        return "document"
    elif extension in settings.supported_image_extensions:
        return "image"
    else:
        raise UnsupportedFileTypeError(
            f"File type '{extension}' is not supported. "
            f"Supported types: {settings.all_supported_extensions}"
        )


def validate_file_size(file_size: int) -> None:
    """Validate file size against limits"""
    if file_size > settings.max_file_size_bytes:
        raise FileSizeExceededError(
            f"File size ({file_size / 1024 / 1024:.2f}MB) exceeds "
            f"maximum allowed size ({settings.max_file_size_mb}MB)"
        )


def get_mime_type(filename: str) -> Optional[str]:
    """Get MIME type from filename"""
    mime_type, _ = mimetypes.guess_type(filename)
    return mime_type