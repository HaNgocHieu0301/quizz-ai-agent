import time
from typing import Dict, Any

from app.services.file_processor import FileProcessor
from app.services.ai_service import AIService
from app.models.response_models import (
    GenerateContentResponse, 
    GeneratedContent, 
    ResponseMetadata,
    Flashcard,
    MultipleChoiceQuestion
)
from app.core.config import settings


class ContentGeneratorService:
    """Main service to orchestrate content generation"""
    
    def __init__(self):
        self.file_processor = FileProcessor()
        self.ai_service = AIService()
    
    async def generate_content(
        self, 
        file_content: bytes, 
        filename: str, 
        num_flashcards: int = 5, 
        num_mcqs: int = 5
    ) -> GenerateContentResponse:
        """
        Main method to generate learning content from uploaded file
        
        Args:
            file_content: Raw file bytes
            filename: Original filename
            num_flashcards: Number of flashcards to generate
            num_mcqs: Number of MCQs to generate
            
        Returns:
            GenerateContentResponse with generated content
        """
        start_time = time.time()
        
        # Process the file
        processed_data = await self.file_processor.process_file(file_content, filename)
        
        # Generate content using AI
        ai_response = await self.ai_service.generate_learning_content(
            processed_data, num_flashcards, num_mcqs
        )
        
        # Convert to response models
        flashcards = [
            Flashcard(front=fc["front"], back=fc["back"])
            for fc in ai_response["flashcards"]
        ]
        
        mcqs = [
            MultipleChoiceQuestion(
                question=mcq["question"],
                options=mcq["options"],
                correct_answer=mcq["correct_answer"]
            )
            for mcq in ai_response["multiple_choice_questions"]
        ]
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Build response
        return GenerateContentResponse(
            status="success",
            metadata=ResponseMetadata(
                original_filename=filename,
                ai_model=settings.gemini_model,
                processing_time_seconds=round(processing_time, 2)
            ),
            data=GeneratedContent(
                flashcards=flashcards,
                multiple_choice_questions=mcqs
            )
        )
    
    async def generate_content_from_text(
        self, 
        text_content: str, 
        num_flashcards: int = 5, 
        num_mcqs: int = 5
    ) -> GenerateContentResponse:
        """
        Generate learning content directly from text input
        
        Args:
            text_content: Raw text content
            num_flashcards: Number of flashcards to generate
            num_mcqs: Number of MCQs to generate
            
        Returns:
            GenerateContentResponse with generated content
        """
        start_time = time.time()
        
        # Create processed data structure for text input
        processed_data = {
            "type": "text",
            "content": text_content,
            "filename": "text_input"
        }
        
        # Generate content using AI
        ai_response = await self.ai_service.generate_learning_content(
            processed_data, num_flashcards, num_mcqs
        )
        
        # Convert to response models
        flashcards = [
            Flashcard(front=fc["front"], back=fc["back"])
            for fc in ai_response["flashcards"]
        ]
        
        mcqs = [
            MultipleChoiceQuestion(
                question=mcq["question"],
                options=mcq["options"],
                correct_answer=mcq["correct_answer"]
            )
            for mcq in ai_response["multiple_choice_questions"]
        ]
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Build response
        return GenerateContentResponse(
            status="success",
            metadata=ResponseMetadata(
                original_filename="text_input",
                ai_model=settings.gemini_model,
                processing_time_seconds=round(processing_time, 2)
            ),
            data=GeneratedContent(
                flashcards=flashcards,
                multiple_choice_questions=mcqs
            )
        )