from pathlib import Path
from app.core.config import settings
from app.core.exceptions import UnsupportedFileTypeError, FileSizeExceededError


class FileHelper:
    @staticmethod
    def validate_file_type(filename: str) -> str:
        """Validate file type and return category"""
        extension = Path(filename).suffix.lower()

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

    @staticmethod
    def validate_file_size(file_size: int) -> None:
        """Validate file size against limits"""
        if file_size > settings.max_file_size_bytes:
            raise FileSizeExceededError(
                f"File size ({file_size / 1024 / 1024:.2f}MB) exceeds "
                f"maximum allowed size ({settings.max_file_size_mb}MB)"
            )

    @staticmethod
    def get_image_mime_type(image_content: bytes) -> str:
        """Detect MIME type from image bytes"""
        # Check image format by looking at file headers
        if image_content.startswith(b'\xff\xd8\xff'):
            return "image/jpeg"
        elif image_content.startswith(b'\x89PNG\r\n\x1a\n'):
            return "image/png"
        elif image_content.startswith(b'GIF87a') or image_content.startswith(b'GIF89a'):
            return "image/gif"
        elif image_content.startswith(b'RIFF') and b'WEBP' in image_content[:12]:
            return "image/webp"
        else:
            # Default to JPEG if we can't detect
            return "image/jpeg"
