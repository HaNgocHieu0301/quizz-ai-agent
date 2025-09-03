from pydantic_settings import BaseSettings
from typing import List, Union


class Settings(BaseSettings):
    # Application
    app_name: str = "AI Learning Tools Generator"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # API
    api_v1_prefix: str = "/api/v1"
    cors_origins: Union[str, List[str]] = ["*"]
    
    # HTTPS Configuration
    use_https: bool = False
    ssl_cert_path: str = "certs/cert.pem"
    ssl_key_path: str = "certs/key.pem"
    
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
    
    @property
    def get_cors_origins(self) -> List[str]:
        """Get CORS origins as list, handling both string and list formats"""
        if isinstance(self.cors_origins, str):
            if self.cors_origins == "*":
                return ["*"]
            return [origin.strip() for origin in self.cors_origins.split(",")]
        return self.cors_origins
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()