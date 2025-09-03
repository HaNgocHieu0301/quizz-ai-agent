class AIAgentException(Exception):
    """Base exception for AI Agent application"""
    pass


class FileProcessingError(AIAgentException):
    """Raised when file processing fails"""
    pass


class UnsupportedFileTypeError(AIAgentException):
    """Raised when file type is not supported"""
    pass


class FileSizeExceededError(AIAgentException):
    """Raised when file size exceeds limits"""
    pass


class AIServiceError(AIAgentException):
    """Raised when AI service fails"""
    pass


class ContentGenerationError(AIAgentException):
    """Raised when content generation fails"""
    pass