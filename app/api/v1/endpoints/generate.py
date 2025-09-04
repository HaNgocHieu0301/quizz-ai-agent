from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
import logging

from app.services.content_generator import ContentGeneratorService
from app.models.response_models import GenerateContentResponse, GenerateChoicesResponse, ErrorResponse
from app.core.exceptions import (
    UnsupportedFileTypeError,
    FileSizeExceededError,
    FileProcessingError,
    AIServiceError,
    ContentGenerationError
)
from app.core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    "/generate",
    response_model=GenerateContentResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        413: {"model": ErrorResponse, "description": "File Too Large"},
        422: {"model": ErrorResponse, "description": "Validation Error"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
    summary="Generate Learning Content",
    description="Generate flashcards and MCQs from either a file upload OR text input (one is required)"
)
async def generate_content(
    type: str = Form("knowledge", description="Content type: 'vocab' for vocabulary-focused cards, 'knowledge' for general learning content"),
    file: Optional[UploadFile] = File(None, description="File to process (.txt, .md, .pdf, .docx, .png, .jpg, .jpeg)"),
    text: Optional[str] = Form(None, description="Text content to process (alternative to file upload)"),
    num_flashcards: Optional[int] = Form(5, ge=0, le=settings.max_flashcards, description="Number of flashcards to generate"),
    num_mcqs: Optional[int] = Form(5, ge=0, le=settings.max_mcqs, description="Number of multiple choice questions to generate")
):
    """
    Generate educational content from uploaded files OR text input.
    
    Input Options (one required):
    - File Upload: Text files (.txt, .md), Documents (.pdf, .docx), Images (.png, .jpg, .jpeg)
    - Text Input: Direct text content as string
    
    Content Types:
    - vocab: Generate vocabulary-focused flashcards (word and meaning pairs)
    - knowledge: Generate general learning content (default behavior)
    
    Returns flashcards and multiple choice questions based on the content.
    """
    
    content_generator = ContentGeneratorService()
    
    try:
        # Validate type parameter
        if type not in ["vocab", "knowledge"]:
            raise HTTPException(
                status_code=400,
                detail=ErrorResponse(
                    error_type="InvalidParameterError",
                    message="Invalid type parameter",
                    details={
                        "valid_types": ["vocab", "knowledge"],
                        "provided": type
                    }
                ).model_dump()
            )
        
        # Validate that exactly one input is provided
        if not file and not text:
            raise HTTPException(
                status_code=400,
                detail=ErrorResponse(
                    error_type="MissingInputError",
                    message="Either 'file' or 'text' parameter is required",
                    details={
                        "file": "Upload a file (.txt, .md, .pdf, .docx, .png, .jpg, .jpeg)",
                        "text": "Provide text content as form parameter"
                    }
                ).model_dump()
            )
        
        if file and text:
            raise HTTPException(
                status_code=400,
                detail=ErrorResponse(
                    error_type="ConflictingInputError",
                    message="Provide either 'file' OR 'text', not both",
                    details={
                        "solution": "Choose one input method: file upload or text content"
                    }
                ).model_dump()
            )
        
        # Handle file input
        if file:
            file_content = await file.read()
            
            if not file_content:
                raise HTTPException(
                    status_code=400,
                    detail=ErrorResponse(
                        error_type="EmptyFileError",
                        message="Uploaded file is empty"
                    ).model_dump()
                )
            
            # Generate content from file
            result = await content_generator.generate_content(
                file_content=file_content,
                filename=file.filename or "unknown",
                num_flashcards=num_flashcards,
                num_mcqs=num_mcqs,
                content_type=type
            )
        
        # Handle text input
        else:
            if not text.strip():
                raise HTTPException(
                    status_code=400,
                    detail=ErrorResponse(
                        error_type="EmptyTextError",
                        message="Text content cannot be empty"
                    ).model_dump()
                )
            
            # Generate content from text
            result = await content_generator.generate_content_from_text(
                text_content=text,
                num_flashcards=num_flashcards,
                num_mcqs=num_mcqs,
                content_type=type
            )
        
        return result
        
    except UnsupportedFileTypeError as e:
        logger.warning(f"Unsupported file type: {e}")
        raise HTTPException(
            status_code=400,
            detail=ErrorResponse(
                error_type="UnsupportedFileTypeError",
                message=str(e),
                details={"supported_types": settings.all_supported_extensions}
            ).model_dump()
        )
    
    except FileSizeExceededError as e:
        logger.warning(f"File size exceeded: {e}")
        raise HTTPException(
            status_code=413,
            detail=ErrorResponse(
                error_type="FileSizeExceededError",
                message=str(e),
                details={"max_size_mb": settings.max_file_size_mb}
            ).model_dump()
        )
    
    except FileProcessingError as e:
        logger.error(f"File processing error: {e}")
        raise HTTPException(
            status_code=400,
            detail=ErrorResponse(
                error_type="FileProcessingError",
                message=str(e)
            ).model_dump()
        )
    
    except (AIServiceError, ContentGenerationError) as e:
        logger.error(f"AI service error: {e}")
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(
                error_type="AIServiceError",
                message="Failed to generate content. Please try again."
            ).model_dump()
        )
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(
                error_type="InternalServerError",
                message="An unexpected error occurred. Please try again."
            ).model_dump()
        )


@router.get("/health", summary="Health Check")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "AI Learning Tools Generator"}

@router.post(
    "/generate-choices",
    response_model=GenerateChoicesResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        422: {"model": ErrorResponse, "description": "Validation Error"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
    summary="Generate Multiple Choice Options",
    description="Generate 3 incorrect options and 1 correct choice for a given question or term"
)
async def generate_choices(
    input_text: str = Form(..., description="Question or term to generate choices for")
):
    """
    Generate multiple choice options for a given question or term.
    
    The AI agent automatically determines the appropriate content type based on the input:
    - Question: Generates answer choices (1 correct + 3 incorrect but related)
    - Term: Generates definition choices (1 correct definition + 3 incorrect but related definitions)
    - Content Type: Automatically determined as 'vocab' or 'knowledge' based on input context
    
    Returns 1 correct choice and 3 incorrect but plausible options.
    """
    
    content_generator = ContentGeneratorService()
    
    try:
        # Validate input text
        if not input_text or not input_text.strip():
            raise HTTPException(
                status_code=400,
                detail=ErrorResponse(
                    error_type="EmptyInputError",
                    message="Input text cannot be empty"
                ).model_dump()
            )
        
        # Generate choices (AI agent will determine appropriate content type)
        result = await content_generator.generate_choices(
            input_text=input_text.strip()
        )
        
        return result
        
    except (AIServiceError, ContentGenerationError) as e:
        logger.error(f"AI service error: {e}")
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(
                error_type="AIServiceError",
                message="Failed to generate choices. Please try again."
            ).model_dump()
        )
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(
                error_type="InternalServerError",
                message="An unexpected error occurred. Please try again."
            ).model_dump()
        )
