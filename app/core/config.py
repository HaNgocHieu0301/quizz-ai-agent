from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Application
    app_name: str = "AI Learning Tools Generator"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # API
    api_v1_prefix: str = "/api/v1"
    cors_origins: List[str] = ["*"]
    
    # Google Gemini
    gemini_api_key: str
    gemini_model: str = "gemini-2.0-flash"
    
    # File Processing
    max_file_size_mb: int = 10
    max_flashcards: int = 20
    max_mcqs: int = 20
    
    # Supported file types
    supported_text_extensions: List[str] = [".txt", ".md"]
    supported_doc_extensions: List[str] = [".pdf", ".docx"]
    supported_image_extensions: List[str] = [".png", ".jpg", ".jpeg"]
    
    @property
    def max_file_size_bytes(self) -> int:
        return self.max_file_size_mb * 1024 * 1024
    
    @property
    def all_supported_extensions(self) -> List[str]:
        return (
            self.supported_text_extensions + 
            self.supported_doc_extensions + 
            self.supported_image_extensions
        )
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()