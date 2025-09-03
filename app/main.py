from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import sys

from app.core.config import settings
from app.api.v1.endpoints import generate
from app.models.response_models import ErrorResponse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API for generating educational content (flashcards and MCQs) from various file formats using AI",
    debug=settings.debug,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    generate.router,
    prefix=settings.api_v1_prefix,
    tags=["Content Generation"]
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled exceptions"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error_type="InternalServerError",
            message="An unexpected error occurred"
        ).model_dump()
    )

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with basic information"""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "docs_url": "/docs",
        "health_check": f"{settings.api_v1_prefix}/health"
    }

# Health check at root level
@app.get("/health", tags=["Health"])
async def health_check():
    """Application health check"""
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version
    }

if __name__ == "__main__":
    import uvicorn
    import os
    
    # Configure SSL if enabled
    ssl_config = {}
    if settings.use_https:
        if os.path.exists(settings.ssl_cert_path) and os.path.exists(settings.ssl_key_path):
            ssl_config = {
                "ssl_certfile": settings.ssl_cert_path,
                "ssl_keyfile": settings.ssl_key_path
            }
            logger.info("HTTPS enabled with SSL certificates")
        else:
            logger.warning("HTTPS enabled but SSL certificates not found. Running with HTTP.")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info",
        **ssl_config
    )